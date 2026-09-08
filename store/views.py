from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import transaction

from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Wishlist,
    UserProfile,
    Order,
    OrderItem,
    InventoryTransaction,
)


def home(request):
    categories = Category.objects.all()

    best_sellers = Product.objects.filter(
        stock__gt=0
    ).order_by("-rating", "-created_at")[:8]

    new_arrivals = Product.objects.filter(
        stock__gt=0
    ).order_by("-created_at")[:8]

    featured_products = Product.objects.filter(
        stock__gt=0
    ).order_by("-discount", "-rating")[:4]

    wishlist_product_ids = set()

    if request.user.is_authenticated:
        wishlist_product_ids = set(
            Wishlist.objects.filter(
                user=request.user
            ).values_list(
                "product_id",
                flat=True
            )
        )

    context = {
        "categories": categories,
        "best_sellers": best_sellers,
        "new_arrivals": new_arrivals,
        "featured_products": featured_products,
        "wishlist_product_ids": wishlist_product_ids,
    }

    return render(
        request,
        "store/home.html",
        context
    )


def shop(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    sort = request.GET.get("sort", "")

    if search:
        products = (
            products.filter(name__icontains=search)
            | products.filter(brand__icontains=search)
        )

    if category:
        products = products.filter(
            category__slug=category
        )

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "rating":
        products = products.order_by("-rating")

    else:
        products = products.order_by("-created_at")

    wishlist_product_ids = set()

    if request.user.is_authenticated:
        wishlist_product_ids = set(
            Wishlist.objects.filter(
                user=request.user
            ).values_list(
                "product_id",
                flat=True
            )
        )

    context = {
        "products": products,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "selected_sort": sort,
        "wishlist_product_ids": wishlist_product_ids,
    }

    return render(
        request,
        "store/shop.html",
        context
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug
    )

    is_wishlisted = False

    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "is_wishlisted": is_wishlisted,
        }
    )


@login_required(login_url="/login/")
def add_to_cart(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug
    )

    if product.stock <= 0:
        messages.error(
            request,
            "This product is out of stock."
        )

        return redirect(
            request.META.get(
                "HTTP_REFERER",
                "/shop/"
            )
        )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        cart_item.quantity = 1

    else:
        if cart_item.quantity >= product.stock:
            messages.warning(
                request,
                f"Only {product.stock} item(s) available."
            )

            return redirect(
                request.META.get(
                    "HTTP_REFERER",
                    "/shop/"
                )
            )

        cart_item.quantity += 1

    cart_item.save()

    messages.success(
        request,
        f"{product.name} added to your bag!"
    )

    return redirect("cart")


@login_required(login_url="/login/")
def cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = cart.items.select_related(
        "product"
    ).all()

    total_amount = cart.total_amount

    return render(
        request,
        "store/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total_amount": total_amount,
        }
    )


@login_required(login_url="/login/")
def increase_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()

    else:
        messages.warning(
            request,
            f"Only {cart_item.product.stock} item(s) available."
        )

    return redirect("cart")


@login_required(login_url="/login/")
def decrease_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect("cart")


@login_required(login_url="/login/")
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    messages.success(
        request,
        "Product removed from your bag."
    )

    return redirect("cart")


@login_required(login_url="/login/")
def empty_cart(request):
    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if cart:
        cart.items.all().delete()

    messages.success(
        request,
        "Your bag has been emptied."
    )

    return redirect("cart")


@login_required(login_url="/login/")
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related("product")

    return render(
        request,
        "store/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


@login_required(login_url="/login/")
def add_to_wishlist(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(
        request,
        f"{product.name} added to your wishlist!"
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/shop/"
        )
    )


@login_required(login_url="/login/")
def remove_from_wishlist(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug
    )

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    messages.success(
        request,
        f"{product.name} removed from your wishlist."
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "/wishlist/"
        )
    )


@login_required(login_url="/login/")
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        if "profile_picture" in request.FILES:

            profile.profile_picture = request.FILES["profile_picture"]
            profile.save()

            messages.success(
                request,
                "Profile picture updated successfully."
            )

        return redirect("/profile/")

    orders = request.user.orders.order_by(
        "-created_at"
    )

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        "store/profile.html",
        {
            "user": request.user,
            "profile": profile,
            "orders": orders,
            "wishlist_count": wishlist_count,
        }
    )


# ================= CHECKOUT =================

@login_required(login_url="/login/")
def checkout(request):

    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        messages.warning(
            request,
            "Your bag is empty."
        )
        return redirect("cart")

    cart_items = cart.items.select_related(
        "product"
    ).all()

    if not cart_items.exists():
        messages.warning(
            request,
            "Your bag is empty."
        )
        return redirect("cart")

    total_amount = cart.total_amount

    return render(
        request,
        "store/checkout.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "total_amount": total_amount,
        }
    )


# ================= PLACE ORDER =================

@login_required(login_url="/login/")
def place_order(request):

    if request.method != "POST":
        return redirect("checkout")

    cart = Cart.objects.filter(
        user=request.user
    ).first()

    if not cart:
        messages.error(
            request,
            "Your bag is empty."
        )
        return redirect("cart")

    cart_items = list(
        cart.items.select_related(
            "product"
        ).all()
    )

    if not cart_items:
        messages.error(
            request,
            "Your bag is empty."
        )
        return redirect("cart")

    full_name = request.POST.get(
        "full_name",
        ""
    ).strip()

    email = request.POST.get(
        "email",
        ""
    ).strip()

    phone = request.POST.get(
        "phone",
        ""
    ).strip()

    address = request.POST.get(
        "address",
        ""
    ).strip()

    city = request.POST.get(
        "city",
        ""
    ).strip()

    state = request.POST.get(
        "state",
        ""
    ).strip()

    pincode = request.POST.get(
        "pincode",
        ""
    ).strip()

    payment_method = request.POST.get(
        "payment_method",
        "COD"
    )

    if not all([
        full_name,
        email,
        phone,
        address,
        city,
        state,
        pincode,
    ]):

        messages.error(
            request,
            "Please fill all delivery details."
        )

        return redirect("checkout")

    if payment_method not in [
        "COD",
        "ONLINE"
    ]:
        payment_method = "COD"

    try:

        with transaction.atomic():

            total_amount = 0

            # Check stock first
            for cart_item in cart_items:

                product = Product.objects.select_for_update().get(
                    id=cart_item.product.id
                )

                if product.stock < cart_item.quantity:

                    raise ValueError(
                        f"Only {product.stock} item(s) of "
                        f"{product.name} are available."
                    )

                total_amount += (
                    product.discounted_price
                    * cart_item.quantity
                )

            # Create Order
            order = Order.objects.create(

                user=request.user,

                full_name=full_name,

                email=email,

                phone=phone,

                address=address,

                city=city,

                state=state,

                pincode=pincode,

                payment_method=payment_method,

                status="Pending",

                total_amount=total_amount,
            )

            # Create Order Items
            for cart_item in cart_items:

                product = Product.objects.select_for_update().get(
                    id=cart_item.product.id
                )

                OrderItem.objects.create(

                    order=order,

                    product=product,

                    quantity=cart_item.quantity,

                    price=product.discounted_price,
                )

                # Reduce stock
                product.stock -= cart_item.quantity

                product.save(
                    update_fields=[
                        "stock",
                        "updated_at"
                    ]
                )

                # Inventory transaction
                InventoryTransaction.objects.create(

                    product=product,

                    transaction_type="OUT",

                    quantity=cart_item.quantity,

                    note=f"Order #{order.id}",
                )

            # Empty cart
            cart.items.all().delete()

        messages.success(
            request,
            f"Order #{order.id} placed successfully!"
        )

        return redirect(
            "order_confirmation",
            order_id=order.id
        )

    except ValueError as e:

        messages.error(
            request,
            str(e)
        )

        return redirect("cart")


# ================= ORDER CONFIRMATION =================

@login_required(login_url="/login/")
def order_confirmation(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "store/order_confirmation.html",
        {
            "order": order,
        }
    )


# ================= ORDER DETAIL =================

@login_required(login_url="/login/")
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order_items = order.items.select_related(
        "product"
    ).all()

    return render(
        request,
        "store/order_detail.html",
        {
            "order": order,
            "order_items": order_items,
        }
    )


# ================= REGISTER =================

def register(request):

    if request.user.is_authenticated:
        return redirect("/profile/")

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Account created successfully! Please login."
            )

            return redirect("/login/")

    else:

        form = UserCreationForm()

    return render(
        request,
        "store/register.html",
        {
            "form": form
        }
    )


# ================= LOGOUT =================

def logout_view(request):

    if request.method == "POST":
        logout(request)

    return redirect("/")
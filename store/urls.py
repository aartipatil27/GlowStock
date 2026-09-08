from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Shop
    path(
        "shop/",
        views.shop,
        name="shop"
    ),

    # Product Detail
    path(
        "shop/<slug:slug>/",
        views.product_detail,
        name="product_detail"
    ),

    # Add to Bag
    path(
        "cart/add/<slug:slug>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # Cart
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # Increase Quantity
    path(
        "cart/increase/<int:item_id>/",
        views.increase_cart,
        name="increase_cart"
    ),

    # Decrease Quantity
    path(
        "cart/decrease/<int:item_id>/",
        views.decrease_cart,
        name="decrease_cart"
    ),

    # Remove Product
    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # Empty Cart
    path(
        "cart/empty/",
        views.empty_cart,
        name="empty_cart"
    ),

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Place Order
    path(
        "place-order/",
        views.place_order,
        name="place_order"
    ),

    # Order Confirmation
    path(
        "order-confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order_confirmation"
    ),

    # Order Detail
    path(
        "order/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),

    # Wishlist
    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),

    # Add to Wishlist
    path(
        "wishlist/add/<slug:slug>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    # Remove from Wishlist
    path(
        "wishlist/remove/<slug:slug>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),

    # Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    # Logout
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Login
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="store/login.html",
            next_page="/profile/"
        ),
        name="login"
    ),

    # Register
    path(
        "register/",
        views.register,
        name="register"
    ),
]
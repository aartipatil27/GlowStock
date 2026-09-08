from django.contrib import admin
from .models import (
    Category,
    Product,
    Wishlist,
    Cart,
    CartItem,
    Order,
    OrderItem,
    InventoryTransaction,
    UserProfile,
)


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


# =========================================================
# PRODUCT
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "price",
        "discount",
        "stock",
        "minimum_stock",
        "rating",
        "expiry_date",
    )

    list_filter = (
        "category",
        "brand",
        "discount",
    )

    search_fields = (
        "name",
        "brand",
        "description",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_editable = (
        "price",
        "discount",
        "stock",
        "minimum_stock",
    )


# =========================================================
# WISHLIST
# =========================================================

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "created_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )


# =========================================================
# CART ITEM INLINE
# =========================================================

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# =========================================================
# CART
# =========================================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    inlines = [
        CartItemInline,
    ]


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# =========================================================
# ORDER
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "total_amount",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
        "user__username",
    )

    list_editable = (
        "status",
    )

    inlines = [
        OrderItemInline,
    ]


# =========================================================
# ORDER ITEM
# =========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "product__name",
    )


# =========================================================
# INVENTORY TRANSACTION
# =========================================================

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "transaction_type",
        "quantity",
        "note",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "created_at",
    )

    search_fields = (
        "product__name",
        "note",
    )


# =========================================================
# USER PROFILE
# =========================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "profile_picture",
    )

    search_fields = (
        "user__username",
        "user__email",
    )
from django.db import models 
from django.contrib.auth.models import User 
from django.utils.text import slugify 
 
 
class Category(models.Model): 
    name = models.CharField(max_length=100, unique=True) 
    slug = models.SlugField(unique=True, blank=True) 
    description = models.TextField(blank=True) 
    image = models.ImageField( 
        upload_to="categories/", 
        blank=True, 
        null=True 
    ) 
 
    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = slugify(self.name) 
        super().save(*args, **kwargs) 
 
    def __str__(self): 
        return self.name 
 
 
class Product(models.Model): 
    category = models.ForeignKey( 
        Category, 
        on_delete=models.CASCADE, 
        related_name="products" 
    ) 
 
    name = models.CharField(max_length=200) 
    slug = models.SlugField(unique=True, blank=True) 
    brand = models.CharField(max_length=100) 
 
    description = models.TextField() 
    ingredients = models.TextField(blank=True) 
 
    price = models.DecimalField( 
        max_digits=10, 
        decimal_places=2 
    ) 
 
    discount = models.PositiveIntegerField(default=0) 
 
    stock = models.PositiveIntegerField(default=0) 
    minimum_stock = models.PositiveIntegerField(default=5) 
 
    expiry_date = models.DateField( 
        blank=True, 
        null=True 
    ) 
 
    rating = models.DecimalField( 
        max_digits=2, 
        decimal_places=1, 
        default=4.0 
    ) 
 
    image = models.ImageField( 
        upload_to="products/", 
        blank=True, 
        null=True 
    ) 
 
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
 
    updated_at = models.DateTimeField( 
        auto_now=True 
    ) 
 
    def save(self, *args, **kwargs): 
        if not self.slug: 
            self.slug = slugify(self.name) 
 
        super().save(*args, **kwargs) 
 
    @property 
    def discounted_price(self): 
        return self.price - ( 
            self.price * self.discount / 100 
        ) 
 
    @property 
    def is_low_stock(self): 
        return self.stock <= self.minimum_stock 
 
    @property 
    def is_out_of_stock(self): 
        return self.stock == 0 
 
    def __str__(self): 
        return self.name 
 
 
# ========================================================= 
# WISHLIST 
# ========================================================= 
 
class Wishlist(models.Model): 
    user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name="wishlist_items" 
    ) 
 
    product = models.ForeignKey( 
        Product, 
        on_delete=models.CASCADE, 
        related_name="wishlisted_by" 
    ) 
 
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
 
    class Meta: 
        unique_together = ("user", "product") 
 
    def __str__(self): 
        return f"{self.user.username} - {self.product.name}" 
 
 
# ========================================================= 
# CART 
# ========================================================= 
 
class Cart(models.Model): 
    user = models.OneToOneField( 
        User, 
        on_delete=models.CASCADE, 
        related_name="cart" 
    ) 
 
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
 
    updated_at = models.DateTimeField( 
        auto_now=True 
    ) 
 
    def __str__(self): 
        return f"Cart - {self.user.username}" 
 
    @property 
    def total_amount(self): 
        return sum( 
            item.subtotal 
            for item in self.items.all() 
        ) 
 
    @property 
    def total_items(self): 
        return sum( 
            item.quantity 
            for item in self.items.all() 
        ) 
 
 
class CartItem(models.Model): 
    cart = models.ForeignKey( 
        Cart, 
        on_delete=models.CASCADE, 
        related_name="items" 
    ) 
 
    product = models.ForeignKey( 
        Product, 
        on_delete=models.CASCADE 
    ) 
 
    quantity = models.PositiveIntegerField( 
        default=1 
    ) 
 
    class Meta: 
        unique_together = ("cart", "product") 
 
    @property 
    def subtotal(self): 
        return ( 
            self.product.discounted_price 
            * self.quantity 
        ) 
 
    def __str__(self): 
        return f"{self.product.name} x {self.quantity}" 
 
 
# ========================================================= 
# ORDER 
# ========================================================= 
 
class Order(models.Model): 
 
    STATUS_CHOICES = [ 
        ("Pending", "Pending"), 
        ("Confirmed", "Confirmed"), 
        ("Packed", "Packed"), 
        ("Shipped", "Shipped"), 
        ("Delivered", "Delivered"), 
        ("Cancelled", "Cancelled"), 
    ] 
 
    PAYMENT_CHOICES = [ 
        ("COD", "Cash on Delivery"), 
        ("ONLINE", "Demo Online Payment"), 
    ] 
 
    user = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        related_name="orders" 
    ) 
 
    full_name = models.CharField( 
        max_length=150 
    ) 
 
    email = models.EmailField() 
 
    phone = models.CharField( 
        max_length=20 
    ) 
 
    address = models.TextField() 
 
    city = models.CharField( 
        max_length=100 
    ) 
 
    state = models.CharField( 
        max_length=100 
    ) 
 
    pincode = models.CharField( 
        max_length=10 
    ) 
 
    payment_method = models.CharField( 
        max_length=20, 
        choices=PAYMENT_CHOICES 
    ) 
 
    status = models.CharField( 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="Pending" 
    ) 
 
    total_amount = models.DecimalField( 
        max_digits=12, 
        decimal_places=2 
    ) 
 
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
 
    def __str__(self): 
        return f"Order #{self.id} - {self.user.username}" 
 
 
# ========================================================= 
# ORDER ITEM 
# ========================================================= 
 
class OrderItem(models.Model): 
 
    order = models.ForeignKey( 
        Order, 
        on_delete=models.CASCADE, 
        related_name="items" 
    ) 
 
    product = models.ForeignKey( 
        Product, 
        on_delete=models.CASCADE 
    ) 
 
    quantity = models.PositiveIntegerField( 
        default=1 
    ) 
 
    price = models.DecimalField( 
        max_digits=10, 
        decimal_places=2 
    ) 
 
    @property 
    def subtotal(self): 
        return self.price * self.quantity 
 
    def __str__(self): 
        return f"{self.product.name} x {self.quantity}" 
 
 
# ========================================================= 
# INVENTORY TRANSACTION 
# ========================================================= 
 
class InventoryTransaction(models.Model): 
 
    TRANSACTION_CHOICES = [ 
        ("IN", "Stock In"), 
        ("OUT", "Stock Out"), 
    ] 
 
    product = models.ForeignKey( 
        Product, 
        on_delete=models.CASCADE, 
        related_name="inventory_transactions" 
    ) 
 
    transaction_type = models.CharField( 
        max_length=10, 
        choices=TRANSACTION_CHOICES 
    ) 
 
    quantity = models.PositiveIntegerField() 
 
    note = models.CharField( 
        max_length=255, 
        blank=True 
    ) 
 
    created_at = models.DateTimeField( 
        auto_now_add=True 
    ) 
 
    def __str__(self): 
        return f"{self.product.name} - {self.transaction_type}"


# =========================================================
# USER PROFILE
# =========================================================

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username
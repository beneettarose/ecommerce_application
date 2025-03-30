from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('common', 'Common'),
        ('women', 'Women'),
        ('accessories', 'Accessories'),
        ('new_arrival', 'New Arrival')
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_name_display()  

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlisted_by')

    def __str__(self):
        return f"Wishlist of {self.user.username}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username

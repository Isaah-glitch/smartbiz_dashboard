from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# -----------------------------
# PRODUCT MODEL
# -----------------------------
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.stock} in stock)"


# -----------------------------
# ORDER MODEL
# -----------------------------
class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(default=timezone.now)
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_created')

    class Meta:
        ordering = ['-ordered_at']
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.customer_name} - {self.product.name} ({self.quantity})"


# -----------------------------
# OPTIONAL: EXTENDED USER PROFILE
# -----------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

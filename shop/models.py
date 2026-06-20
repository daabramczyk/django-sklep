from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


class Brand(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ("MEN", "Męskie"),
        ("WOMEN", "Damskie"),
        ("UNISEX", "Unisex"),
        ("KIDS", "Dziecięce"),
    ]

    name = models.CharField(max_length=128)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField()
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, default="UNISEX")
    material = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    @property
    def average_rating(self):
        value = self.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(value, 2) if value else None

    @property
    def reviews_count(self):
        return self.reviews.count()

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]

    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES)
    color = models.CharField(max_length=32)
    sku = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        return self.price

    @property
    def is_on_sale(self):
        return self.sale_price is not None and self.sale_price < self.price

    def __str__(self):
        return f"{self.product} | {self.color} | {self.size}"


class Coupon(models.Model):
    code = models.CharField(max_length=32, unique=True)
    discount_percent = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(90),
        ]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"


class Order(models.Model):
    STATUS_CHOICES = [
        ("NEW", "Nowe"),
        ("PAID", "Opłacone"),
        ("SHIPPED", "Wysłane"),
        ("DELIVERED", "Dostarczone"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    order_number = models.CharField(max_length=32, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    tracking_number = models.CharField(max_length=100, blank=True)

    coupon_code = models.CharField(max_length=32, blank=True)
    total_before_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def save(self, *args, **kwargs):
        old_status = None

        if self.pk:
            old_order = Order.objects.get(pk=self.pk)
            old_status = old_order.status

        super().save(*args, **kwargs)

        if not self.order_number:
            self.order_number = f"ORD-{self.created_at.year}-{self.id:06d}"
            super().save(update_fields=["order_number"])

        if old_status != self.status:
            OrderStatusHistory.objects.create(
                order=self,
                status=self.status
            )

            AuditLog.objects.create(
                actor=None,
                action="ORDER_STATUS_CHANGED",
                object_type="Order",
                object_id=str(self.id),
                description=f"Status zamówienia {self.order_number}: {old_status} -> {self.status}",
            )

    def __str__(self):
        return self.order_number or f"Zamówienie #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant} x {self.quantity}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.product} - {self.rating}/5 - {self.user}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("CUSTOMER", "Klient"),
        ("WAREHOUSE", "Magazynier"),
        ("MANAGER", "Manager"),
        ("ADMIN", "Administrator"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="CUSTOMER"
    )

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name="status_history", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.get_status_display()} - {self.created_at}"


class AuditLog(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    action = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        actor_name = self.actor.username if self.actor else "SYSTEM"
        return f"{self.created_at} | {actor_name} | {self.action}"

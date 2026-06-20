from django.db import models
from django.conf import settings


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
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product} | {self.color} | {self.size}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("NEW", "Nowe"),
        ("PAID", "Opłacone"),
        ("SHIPPED", "Wysłane"),
        ("DELIVERED", "Dostarczone"),
        ("CANCELLED", "Anulowane"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="NEW"
    )

    order_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True
    )

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

    def __str__(self):
        return self.order_number or f"Zamówienie #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant} x {self.quantity}"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name="status_history", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.get_status_display()} - {self.created_at}"

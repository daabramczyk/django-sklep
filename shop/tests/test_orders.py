from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import Brand, Category, Product, ProductVariant, Order, OrderItem


class OrderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="customer",
            password="Test123456"
        )

        self.brand = Brand.objects.create(name="Nike")
        self.category = Category.objects.create(name="Koszulki")

        self.product = Product.objects.create(
            name="Air Tee",
            brand=self.brand,
            category=self.category,
            description="Koszulka testowa",
            gender="UNISEX",
        )

        self.variant = ProductVariant.objects.create(
            product=self.product,
            size="M",
            color="Czarny",
            sku="NIKE-AIR-TEE-M-BLK",
            price=Decimal("99.99"),
            stock=10,
        )

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            total_before_discount=Decimal("99.99"),
            total_after_discount=Decimal("99.99"),
        )

        self.assertIsNotNone(order.id)
        self.assertTrue(order.order_number.startswith("ORD-"))

    def test_create_order_item(self):
        order = Order.objects.create(
            user=self.user,
            total_before_discount=Decimal("99.99"),
            total_after_discount=Decimal("99.99"),
        )

        item = OrderItem.objects.create(
            order=order,
            variant=self.variant,
            quantity=1,
            price_at_order=self.variant.price,
        )

        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.price_at_order, Decimal("99.99"))

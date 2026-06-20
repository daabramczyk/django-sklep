from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import (
    Brand,
    Category,
    Product,
    ProductVariant,
    UserProfile,
)


class CheckoutTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="customer",
            password="Test123456"
        )

        UserProfile.objects.create(
            user=self.user,
            role="CUSTOMER",
            phone="123123123",
            street="Testowa 1",
            postal_code="20-001",
            city="Lublin",
        )

        self.brand = Brand.objects.create(
            name="Nike"
        )

        self.category = Category.objects.create(
            name="Koszulki"
        )

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
            sku="TEST-SKU-001",
            price=Decimal("100.00"),
            stock=10,
        )

    def test_checkout_requires_login(self):
        response = self.client.post(
            "/checkout/"
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_checkout_empty_cart(self):
        self.client.login(
            username="customer",
            password="Test123456"
        )

        response = self.client.post(
            "/checkout/"
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_add_product_to_session_cart(self):
        session = self.client.session

        session["cart"] = {
            str(self.variant.id): 2
        }

        session.save()

        self.assertEqual(
            session["cart"][str(self.variant.id)],
            2
        )

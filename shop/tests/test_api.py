from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from shop.models import (
    Brand,
    Category,
    Product,
    ProductVariant,
    Order,
    UserProfile,
)


class ApiTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser",
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
            sku="API-SKU-001",
            price=Decimal("100.00"),
            stock=10,
        )

        self.order = Order.objects.create(
            user=self.user,
            total_before_discount=Decimal("100.00"),
            total_after_discount=Decimal("100.00"),
        )

    def test_api_brands_list(self):
        response = self.client.get("/api/brands/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Nike")

    def test_api_categories_list(self):
        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Koszulki")

    def test_api_products_list(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Air Tee")

    def test_api_product_detail(self):
        response = self.client.get(
            f"/api/products/{self.product.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Air Tee")

    def test_api_orders_requires_authentication(self):
        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 401)

    def test_api_orders_with_jwt(self):
        token_response = self.client.post(
            "/api/token/",
            {
                "username": "apiuser",
                "password": "Test123456"
            },
            format="json"
        )

        access_token = token_response.data["access"]

        response = self.client.get(
            "/api/orders/",
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_number"], self.order.order_number)

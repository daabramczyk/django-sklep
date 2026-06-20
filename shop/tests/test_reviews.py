from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import Brand, Category, Product, Review


class ReviewTest(TestCase):

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

    def test_create_review(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Super produkt."
        )

        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Super produkt.")

    def test_product_average_rating(self):
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="OK"
        )

        self.assertEqual(self.product.average_rating, 4)
        self.assertEqual(self.product.reviews_count, 1)

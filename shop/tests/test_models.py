from django.test import TestCase

from shop.models import Brand


class BrandModelTest(TestCase):

    def test_create_brand(self):
        brand = Brand.objects.create(
            name="Nike"
        )

        self.assertEqual(
            brand.name,
            "Nike"
        )

    def test_brand_str(self):
        brand = Brand.objects.create(
            name="Adidas"
        )

        self.assertEqual(
            str(brand),
            "Adidas"
        )

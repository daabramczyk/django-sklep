from django.test import TestCase

from shop.models import Coupon


class CouponTest(TestCase):

    def test_create_coupon(self):
        coupon = Coupon.objects.create(
            code="SALE10",
            discount_percent=10,
            is_active=True
        )

        self.assertEqual(coupon.code, "SALE10")
        self.assertEqual(coupon.discount_percent, 10)
        self.assertTrue(coupon.is_active)

    def test_coupon_str(self):
        coupon = Coupon.objects.create(
            code="SALE20",
            discount_percent=20,
            is_active=True
        )

        self.assertEqual(str(coupon), "SALE20 - 20%")

from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import UserProfile


class PermissionTest(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer",
            password="Test123456"
        )

        self.manager = User.objects.create_user(
            username="manager",
            password="Test123456"
        )

        UserProfile.objects.create(
            user=self.customer,
            role="CUSTOMER"
        )

        UserProfile.objects.create(
            user=self.manager,
            role="MANAGER"
        )

    def test_customer_cannot_access_dashboard(self):
        self.client.login(
            username="customer",
            password="Test123456"
        )

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 302)

    def test_manager_can_access_dashboard(self):
        self.client.login(
            username="manager",
            password="Test123456"
        )

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)

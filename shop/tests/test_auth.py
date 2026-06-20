from django.contrib.auth.models import User
from django.test import TestCase


class AuthTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            password="Test123456"
        )

        self.assertEqual(
            user.username,
            "testuser"
        )

    def test_login(self):
        User.objects.create_user(
            username="testuser",
            password="Test123456"
        )

        logged = self.client.login(
            username="testuser",
            password="Test123456"
        )

        self.assertTrue(logged)

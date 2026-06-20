from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class JwtTest(APITestCase):

    def setUp(self):
        User.objects.create_user(
            username="apiuser",
            password="Test123456"
        )

    def test_get_jwt_token(self):
        response = self.client.post(
            "/api/token/",
            {
                "username": "apiuser",
                "password": "Test123456"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            "access",
            response.data
        )

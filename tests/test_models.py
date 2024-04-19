import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from d_jwt_auth.models import UserAuth

User = get_user_model()


class TestUserAuthModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="alireza",
            password="password",
            email="alirezafeyze44@gmail.com")

    def test_user_auth_create(self):
        UserAuth.objects.create(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())
        self.assertEqual(UserAuth.objects.count(), 1)

    def test_ordering_user_auth(self):
        for i in range(10):
            UserAuth.objects.create(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())

        self.assertEqual(UserAuth.objects.first().id, 10)

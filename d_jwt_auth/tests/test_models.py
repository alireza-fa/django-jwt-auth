import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import UserAuth

User = get_user_model()


class TestUserAuthModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="alireza",
            password="password",
            email="alirezafeyze44@gmail.com")

    def test_user_auth_create(self):
        UserAuth.objects.create(user=self.user, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())
        self.assertEqual(UserAuth.objects.count(), 1)

    def test_ordering_user_auth(self):
        for i in range(10):
            UserAuth.objects.create(user=self.user, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())

        self.assertEqual(UserAuth.objects.first().id, 10)

    def test_user_auth_query_num(self):
        for i in range(100):
            UserAuth.objects.create(user=self.user, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())

        with self.assertNumQueries(1):
            [user_auth.user for user_auth in UserAuth.objects.all()]

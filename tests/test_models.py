import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import UserRole
from d_jwt_auth.models import UserAuth

User = get_user_model()


class TestUserAuthModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            fullname="alireza",
            national_code="1111111111",
            phone_number="09309806535",
            password="password",
            email="alirezafeyze44@gmail.com")

    def test_user_auth_create(self):
        UserAuth.objects.create(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())
        self.assertEqual(UserAuth.objects.count(), 1)

    def test_ordering_user_auth(self):
        for i in range(10):
            UserAuth.objects.create(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid=uuid.uuid4())

        self.assertEqual(UserAuth.objects.first().id, 10)

    def test_user_role_create(self):
        self.user.roles.create(role=UserRole.DEFAULT)
        self.user.roles.create(role=UserRole.DOCTOR)
        self.assertEqual(self.user.roles.count(), 2)

    def test_user_role_conflict(self):
        self.user.roles.create(role=UserRole.DEFAULT)
        with self.assertRaises(Exception):
            self.user.roles.create(role=UserRole.DEFAULT)

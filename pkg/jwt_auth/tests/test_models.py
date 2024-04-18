from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserAuthModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user()
import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import override_settings

from d_jwt_auth.services import create_user_auth, get_user_auth_uuid, ACCESS_UUID_CACHE_KEY, \
    REFRESH_UUID_CACHE_KEY, update_user_auth_uuid, get_user_auth
from d_jwt_auth.models import UserAuth
from d_jwt_auth.cache import get_cache, clear_all_cache
from d_jwt_auth.app_settings import app_setting


User = get_user_model()


class TestServices(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            fullname="alireza",
            national_code="1111111111",
            phone_number="09309806535",
            password="password",
            email="alirezafeyze44@gmail.com")

    def test_user_auth_cache_key(self):
        access_key = ACCESS_UUID_CACHE_KEY.format(user_id=1)
        self.assertEqual("user:1:access:uuid", access_key)
        refresh_key = REFRESH_UUID_CACHE_KEY.format(user_id=1)
        self.assertEqual("user:1:refresh:uuid", refresh_key)

    def test_create_user_auth(self):
        create_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(UserAuth.objects.count(), 1)

    def test_create_user_auth_for_many_users(self):
        for i in range(10):
            user = User.objects.create_user(
                fullname="user%d" % i,
                national_code="1111111111",
                phone_number="0912912111%d" % i,
                password="password",
                email="email%d@gmail.com" % i)
            create_user_auth(user_id=user.id, token_type=UserAuth.ACCESS_TOKEN)
            create_user_auth(user_id=user.id, token_type=UserAuth.REFRESH_TOKEN)
        self.assertEqual(UserAuth.objects.count(), 20)

    def test_create_user_auth_user(self):
        create_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(UserAuth.objects.first().user_id, self.user.id)

    def test_create_user_Auth_token_type(self):
        create_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(UserAuth.objects.first().token_type, UserAuth.ACCESS_TOKEN)
        create_user_auth(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
        self.assertEqual(UserAuth.objects.first().token_type, UserAuth.REFRESH_TOKEN)

    def test_create_user_auth_without_uuid(self):
        create_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(type(UserAuth.objects.first().uuid), uuid.UUID)
        self.assertIsNotNone(UserAuth.objects.first().uuid)

    def test_create_user_auth_with_uuid(self):
        uuid_field = uuid.uuid4()
        create_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN, uuid_filed=uuid_field)
        self.assertEqual(UserAuth.objects.first().uuid, uuid_field)

    def test_get_user_auth_uuid(self):
        clear_all_cache()
        access_uuid = get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(UserAuth.objects.count(), 1)
        self.assertEqual(str(UserAuth.objects.first().uuid), access_uuid)

    def test_get_user_auth_uuid_cache_info_with_access_key(self):
        if app_setting.cache_using:
            clear_all_cache()
            access_uuid = get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
            cache_uuid = get_cache(key=ACCESS_UUID_CACHE_KEY.format(user_id=self.user.id))
            self.assertIsNotNone(cache_uuid)
            self.assertEqual(access_uuid, cache_uuid)

    def test_get_user_auth_uuid_cache_info_with_refresh_key(self):
        if app_setting.cache_using:
            clear_all_cache()
            refresh_uuid = get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
            cache_uuid = get_cache(key=REFRESH_UUID_CACHE_KEY.format(user_id=self.user.id))
            self.assertIsNotNone(cache_uuid)
            self.assertEqual(refresh_uuid, cache_uuid)

    def test_get_user_auth_uuid_only_create_once(self):
        clear_all_cache()
        for i in range(10):
            get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
            get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)

        self.assertEqual(UserAuth.objects.count(), 2)
        self.assertEqual(UserAuth.objects.filter(token_type=UserAuth.ACCESS_TOKEN).count(), 1)
        self.assertEqual(UserAuth.objects.filter(token_type=UserAuth.REFRESH_TOKEN).count(), 1)

    def test_update_user_auth_uuid_create_new_user_auth(self):
        update_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(UserAuth.objects.count(), 1)

    def test_update_user_auth_uuid_create_once(self):
        for i in range(10):
            update_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
            update_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)

        self.assertEqual(UserAuth.objects.count(), 2)
        self.assertEqual(UserAuth.objects.filter(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN).count(), 1)

    def test_update_user_auth_exist_user_auth(self):
        uuid_field = get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        new_uuid_field = update_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertNotEquals(uuid_field, new_uuid_field)
        self.assertEqual(str(UserAuth.objects.first().uuid), new_uuid_field)

    def test_get_uuid_from_database_once(self):
        clear_all_cache()
        get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
        UserAuth.objects.all().delete()
        uuid_field_from_cache = get_user_auth_uuid(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
        self.assertIsNotNone(uuid_field_from_cache)

    def test_get_user_auth_access_token(self):
        user_auth = get_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        self.assertEqual(user_auth.token_type, UserAuth.ACCESS_TOKEN)

    def test_get_user_auth_refresh_token(self):
        user_auth = get_user_auth(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
        self.assertEqual(user_auth.token_type, UserAuth.REFRESH_TOKEN)

    def test_get_user_auth_create_once(self):
        user_auth = get_user_auth(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
        user_auth2 = get_user_auth(user_id=self.user.id, token_type=UserAuth.REFRESH_TOKEN)
        self.assertEqual(user_auth2.uuid, user_auth.uuid)

    @override_settings(JWY_AUTH_USING_CACHE=True)
    def tset_get_user_auth_cache_uuid(self):
        clear_all_cache()
        user_auth = get_user_auth(user_id=self.user.id, token_type=UserAuth.ACCESS_TOKEN)
        uuid_cache = get_cache(key=ACCESS_UUID_CACHE_KEY.format(user_id=self.user.id))
        self.assertEqual(str(user_auth.uuid), uuid_cache)

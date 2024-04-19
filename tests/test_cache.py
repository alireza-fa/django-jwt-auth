import time

from django.test import SimpleTestCase
from d_jwt_auth.cache import get_cache, set_cache, delete_cache, clear_all_cache, incr_cache


class TestSimple(SimpleTestCase):
    def setUp(self):
        self.key = "test_set_cache"

    def test_set_and_get_cache(self):
        set_cache(key="test_set_cache", value=1, timeout=10)
        info = get_cache(key=self.key)
        self.assertEqual(info, 1)

    def test_cache_timeout(self):
        set_cache(key=self.key, value=1, timeout=1)
        time.sleep(2)
        self.assertEqual(get_cache(key=self.key), None)

    def test_delete_cache(self):
        set_cache(key=self.key, value=1, timeout=120)
        delete_cache(key=self.key)
        self.assertEqual(get_cache(key=self.key), None)

    def test_clear_all_cache(self):
        for i in range(100):
            set_cache(key="%s:%d" % (self.key, i), value=i, timeout=120)

        clear_all_cache()

        for i in range(100):
            self.assertEqual(get_cache(key="%s:%d" % (self.key, i)), None)

    def test_incr_cache(self):
        set_cache(key=self.key, value=0, timeout=120)

        for i in range(10):
            incr_cache(key=self.key)
            self.assertEqual(get_cache(key=self.key), i + 1)

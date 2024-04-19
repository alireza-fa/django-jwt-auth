from ast import literal_eval
from Crypto.Cipher._mode_ecb import EcbMode
from django.test import SimpleTestCase

from d_jwt_auth.encryption import get_new_cipher, encrypt, decrypt
from d_jwt_auth.app_settings import app_setting


class TestEncryption(SimpleTestCase):

    def test_get_new_cipher(self):
        chpiher = get_new_cipher(key=app_setting.encrypt_key)
        self.assertEqual(type(chpiher), EcbMode)

    def test_encrypt_and_decrypt_string(self):
        encrypted_data = encrypt(data="text", key=app_setting.encrypt_key)
        decrypted_data = decrypt(encrypted=encrypted_data.encode(), key=app_setting.encrypt_key)
        self.assertEqual(decrypted_data, "text")

    def test_encrypt_and_decrypt_integer(self):
        encrypted_data = encrypt(data="11", key=app_setting.encrypt_key)
        decrypted_data = decrypt(encrypted=encrypted_data.encode(), key=app_setting.encrypt_key)
        self.assertEqual(int(decrypted_data), 11)

    def test_encrypt_and_decrypt_map(self):
        encrypted_data = encrypt(data=str({"name": "alireza"}), key=app_setting.encrypt_key)
        decrypted_data = decrypt(encrypted=encrypted_data.encode(), key=app_setting.encrypt_key)
        self.assertEqual(literal_eval(decrypted_data), {"name": "alireza"})

    def test_decrypt_with_invalid_data(self):
        with self.assertRaises(ValueError):
            decrypt(encrypted="invalid data".encode(), key=app_setting.encrypt_key)

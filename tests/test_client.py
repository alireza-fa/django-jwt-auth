from django.test import SimpleTestCase, RequestFactory

from d_jwt_auth import client


class TestClient(SimpleTestCase):

    def test_request_ip_address_remote(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "127.0.0.1"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_remote_list(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "127.0.0.1, 128.1.0.8"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_remote_with_port(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "127.0.0.1:1234"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_remote_with_port_list(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "127.0.0.1:1234, 128.0.0.9:1234"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_v6(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_v6_list(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = ("2001:0db8:85a3:0000:0000:8a2e:0370:7334,"
                                       " 3001:0db8:85a3:0000:0000:8a2e:0370:7334")
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_v6_loopback(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "::1"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "::1")

    def test_request_ip_address_v6_with_port(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_v6_with_port_list(self):
        request = RequestFactory().get(path="/")
        request.META["REMOTE_ADDR"] = ("[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234,"
                                       " [3001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234")
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_x_forwarded(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.1"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_x_forwarded_list(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.1, 128.1.0.8"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_x_forwarded_with_port(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.1:1234"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_x_forwarded_with_port_list(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.1:1234, 128.0.0.9:1234"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "127.0.0.1")

    def test_request_ip_address_v6_x_forwarded(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_v6_x_forwarded_list(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = ("2001:0db8:85a3:0000:0000:8a2e:0370:7334,"
                                                " 3001:0db8:85a3:0000:0000:8a2e:0370:7334")
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_v6_loopback_x_forwarded(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "::1"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "::1")

    def test_request_ip_address_v6_with_port_x_forwarded(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_request_ip_address_v6_with_port_x_forwarded_list(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = ("[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234,"
                                                " [3001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234")
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.IP_ADDRESS], "2001:db8:85a3::8a2e:370:7334")

    def test_device_name(self):
        request = RequestFactory().get(path="/")
        request.META["HTTP_X_FORWARDED_FOR"] = ("[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234,"
                                                " [3001:0db8:85a3:0000:0000:8a2e:0370:7334]:1234")
        request.META["HTTP_USER_AGENT"] = "test-device"
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.DEVICE_NAME], "test-device")

    def test_device_name_empty(self):
        request = RequestFactory().get(path="/")
        client_info = client.get_client_info(request=request)
        self.assertEqual(client_info[client.DEVICE_NAME], "")

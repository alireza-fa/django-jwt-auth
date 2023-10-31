from rest_framework.views import APIView
from rest_framework.response import Response


class UserLoginView(APIView):
    """
    The login function is the function that should do this:
        1. Get user information for login (such as email).
        2. Login the user or send a message confirming the account
    """

    def post(self, request):
        pass


class UserRefreshView(APIView):
    """"""

    def post(self, request):
        pass


class UserVerifyView(APIView):
    """"""

    def post(self, request):
        pass

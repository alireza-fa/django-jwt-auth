# d_jwt_auth

The `d_jwt_auth` package is designed for user authentication via JSON Web Tokens (JWT).

## Why use d_jwt_auth?

This package allows you to easily set up a secure JWT authentication system with useful features for your Django application.

Some key strengths of this package include:

1. **Ability to use access token claims to retrieve user information instead of querying the database on each request.** This feature has improved the performance of user retrieval threefold.

2. **Token encryption**

3. **Professional and highly efficient token invalidation method**

4. **Ability to use caching, doubling the performance in token validation**

5. **Validation access token with ip address and device && validation refresh token with device name**

## Getting Started with d_jwt_auth

First, install the `d_jwt_auth` package:

```
pip install d_jwt_auth
```

Add it to your `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    ...
    "d_jwt_auth",
]
```

Run the `python manage.py migrate` command to create the `user_auth` table.

Add JWTAuthentication in rest_framework Authentication Class:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'd_jwt_auth.authenticate.JWTAuthentication',
        ...
    ),
}
```

## Creating Access Token and Refresh Token for a User

To create an access token and refresh token for a user, you can use the `generate_token` function from the `d_jwt_auth.token` module.

```python
from d_jwt_auth.token import generate_token

class LoginView(APIView):

    def post(self, request):
        ...
        token = generate_token(request=request, user=user)
        return Response(data=token, status=status.HTTP_200_OK)
```

The `generate_token` function will generate a new access token and refresh token for the provided user.

## Token Verification

To verify the validity of a token, you can use the `verify_token` function from the `d_jwt_auth.token` module.

```python
from d_jwt_auth.token import verify_token

class VerifyTokenView(APIView):

    def post(self, request):
        ...
        if verify_token(request=request, raw_token=serializer.validated_data["token"]):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
```

The `verify_token` function returns `True` if the token is valid, and `False` otherwise.

## Refreshing Access Token

To refresh an access token, you can use the `refresh_access_token` function from the `d_jwt_auth.token` module.

```python
from d_jwt_auth.token import refresh_access_token
from d_jwt_auth.exceptions import TokenError

class RefreshTokenView(APIView):

    def post(self, request):
        ...
        try:
            access_token = refresh_access_token(
                request=request, raw_refresh_token=serializer.refresh_token["refresh_token"])
        except TokenError as err:
            ...

        return Response(data={"access_token": access_token}, status=status.HTTP_200_OK)
```

The `refresh_access_token` function takes the request object and the raw refresh token as arguments, and returns a new access token if the refresh token is valid. If there's an issue with the refresh token, it will raise a `TokenError` exception.

## d_jwt_auth Settings

The `d_jwt_auth` settings are configured in the `settings.py` file of your Django project and include the following options:

`JWT_AUTH_ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)`
The lifetime of the access token. The default is 10 minutes.

`JWT_AUTH_REFRESH_TOKEN_LIFETIME = timedelta(days=30)`
The lifetime of the refresh token. The default is 30 days.

`JWT_AUTH_REFRESH_TOKEN_CLAIMS = {"id": 0, "ip_address": "", "device_name": ""}`
This setting allows you to specify the claims you want to include in the refresh token. The `id` field is for user identification, and the `ip_address` and `device_name` fields are for token validation. These fields are included by default, and you cannot remove them.

`JWT_AUTH_ACCESS_TOKEN_CLAIMS = {"id": 0, "ip_address": "", "device_name": ""}`
This setting allows you to specify the claims you want to include in the access token. Similar to the refresh token, the `id`, `ip_address`, and `refresh_token` fields are included by default.

Note: If you want to create the user object using the access token claims and achieve better performance than retrieving user data from the database, you need to set the required fields from the user model exactly as they are defined in the model, in the access token claims. Finally, you need to set `JWT_AUTH_GET_USER_BY_ACCESS_TOKEN` to `True`.

For example:

```python
JWT_AUTH_ACCESS_TOKEN_CLAIMS = {
    "username": "",
    "email": "",
    "age": 0,
}

JWT_AUTH_GET_USER_BY_ACCESS_TOKEN = True
```

The `d_jwt_auth` settings are configured in the `settings.py` file of your Django project and include the following options:

`JWT_AUTH_ACCESS_TOKEN_USER_FIELD_CLAIMS = {
"id": 0,
"username": "",
"email": "",
"age": 0,
}`

If you want to create the user object using the access token, you need to set this field along with the previous `JWT_AUTH_ACCESS_TOKEN_CLAIMS` and `JWT_AUTH_GET_USER_BY_ACCESS_TOKEN` fields. This field specifies the access token claims that correspond to the fields in your user model.

`JWT_AUTH_ENCRYPT_KEY = b'32 bytes'`

This field specifies the `ENCRYPT_KEY` value. The tokens are encrypted and sent to the client.
If you don't set this field, a new `ENCRYPT_KEY` is generated every time your Django app is run.

`JWT_AUTH_CACHE_USING = False`

This field allows you to specify whether to use caching for token validation or not. If you want to use caching, set it to `True`. Using caching can improve performance by at least two times, and significantly fewer queries are made to the database to retrieve the `UseAuth` object.
By default, this field is set to `False`, but it is recommended to use caching.

`JWT_AUTH_GET_USER_BY_ACCESS_TOKEN = False`

Based on the previous explanations, if you set this field to `True`, the user information will be retrieved from the access token. By using this feature, you no longer need to query the database every time to retrieve user information, and the response time for retrieving user information can be at least two times faster.

## ----------------------- ----------------------
For customizations and modifications, you have complete freedom, and you can easily personalize the package according to your project's needs.

I would appreciate it if you could support me by starring this project and contributing to its improvement.

I hope this package proves useful for you.

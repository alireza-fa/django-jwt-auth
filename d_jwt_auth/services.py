import uuid

from .models import UserAuth
from .cache import get_cache, set_cache, delete_cache


ACCESS_UUID_CACHE_KEY = "user:access:uuid:{user_id}"
REFRESH_UUID_CACHE_KEY = "user:refresh:uuid:{user_id}"

TOKEN_TYPE_KEY = {
    UserAuth.ACCESS_TOKEN: ACCESS_UUID_CACHE_KEY,
    UserAuth.REFRESH_TOKEN: REFRESH_UUID_CACHE_KEY,
}


def create_user_auth(user_id: int, token_type: int, uuid_filed: uuid.UUID | None = None) -> UserAuth:
    user_auth = UserAuth(user_id=user_id, token_type=token_type)
    if uuid_filed:
        user_auth.uuid = uuid_filed
    else:
        user_auth.uuid = uuid.uuid4()
    user_auth.save()
    return user_auth


def get_user_auth_uuid(user_id: int, token_type: int) -> str:
    access_uuid = get_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id))
    if access_uuid:
        return access_uuid

    user_auths = UserAuth.objects.filter(user_id=user_id, token_type=token_type)
    if user_auths.exists():
        user_auth = user_auths.first()
    else:
        user_auth = create_user_auth(user_id=user_id, token_type=token_type)

    set_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id), value=str(user_auth.uuid), timeout=60*60*24*30)

    return str(user_auth.uuid)


def update_user_auth_uuid(user_id: int, token_type: int) -> str:
    user_auths = UserAuth.objects.filter(user_id=user_id, token_type=token_type)
    if user_auths.exists():
        user_auth = user_auths.first()
        user_auth.uuid = uuid.uuid4()
        user_auth.save()
    else:
        user_auth = create_user_auth(user_id=user_id, token_type=token_type)

    set_cache(key=TOKEN_TYPE_KEY[token_type].format(user_id=user_id), value=str(user_auth.uuid), timeout=60*60*24*30)

    return str(user_auth.uuid)

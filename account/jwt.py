from calendar import timegm

from django.utils import timezone
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):

    payload = {
        "user_id": user.pk,
        "username": str(user.username),
        "exp": timezone.now() + api_settings.JWT_EXPIRATION_DELTA,
    }

    payload["user_id"] = str(user.pk)

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload["orig_iat"] = timegm(timezone.now().utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload["aud"] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload["iss"] = api_settings.JWT_ISSUER

    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {"token": token}


def jwt_get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get("username")


def default_create_token(token_model, user, serializer):
    token, _ = token_model.objects.get_or_create(user=user)
    return token

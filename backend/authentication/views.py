from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    """
    View for handling Google OAuth2 login.

    Attributes:
        adapter_class: The adapter class for Google OAuth2.
        callback_url: The URL to redirect to after Google authentication.
        client_class: The OAuth2 client class for Google.

    Note:
        The `callback_url` is set to "http://127.0.0.1:3000/" by default.
        It should be changed based on the DEBUG value from settings.py.
    """
    adapter_class = GoogleOAuth2Adapter
    # TODO change this based on DEBUG value from settings.py
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client

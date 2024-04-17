from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # TODO change this based on DEBUG value from settings.py
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client

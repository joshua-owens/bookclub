import logging
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.shortcuts import render

# Create your views here.
from django.views import View
from inertia import render
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter, oauth2_login
from allauth.socialaccount import providers
from allauth.socialaccount.providers.base.constants import (
    AuthAction,
    AuthError,
)
from allauth.socialaccount.models import SocialApp

from allauth.socialaccount.models import SocialLogin

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'Home', props={
        'data': 'test'
    })


def login(request):
    logger.info("Entering login view")
    app = SocialApp.objects.get(provider='discord')
    adapter = DiscordOAuth2Adapter(request)

    callback_url = adapter.get_callback_url(request, app)
    provider = adapter.get_provider()
    scope = provider.get_scope(request)


    auth_url = adapter.authorize_url
    auth_params = provider.get_auth_params(request, AuthAction.AUTHENTICATE)

    pkce_params = provider.get_pkce_params()
    code_verifier = pkce_params.pop("code_verifier", None)
    auth_params.update(pkce_params)
    if code_verifier:
        request.session["pkce_code_verifier"] = code_verifier


    client = adapter.client_class(
        request,
        app.client_id,
        app.secret,
        adapter.access_token_method,
        adapter.access_token_url,
        callback_url,
        scope,
        scope_delimiter=adapter.scope_delimiter,
        headers=adapter.headers,
        basic_auth=adapter.basic_auth,
    )

    client.state = SocialLogin.stash_state(request)
    redirect_url = client.get_redirect_url(auth_url, auth_params)
    logger.info(f"Redirect URL: {redirect_url}")

    return render(request, 'Login', props={
        'discordAuthUrl': redirect_url,
    })

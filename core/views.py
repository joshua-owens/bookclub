from allauth.socialaccount.models import SocialApp
from django.shortcuts import render

# Create your views here.
from django.views import View
from inertia import render
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter

def index(request):
    return render(request, 'Home', props={
        'data': 'test'
    })


def login(request):
    adapter = DiscordOAuth2Adapter(request)
    app = SocialApp.objects.get(provider='discord')
    client_id = app.client_id
    redirect_uri = adapter.get_callback_url(request, None)
    auth_url_base = 'https://discord.com/api/oauth2/authorize'
    discord_auth_url = f"{auth_url_base}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify%20email"

    return render(request, 'Login', props={
        'discordAuthUrl': discord_auth_url,
    })

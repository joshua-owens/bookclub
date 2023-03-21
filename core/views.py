from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from django.conf import settings

from allauth.socialaccount.models import SocialToken, SocialApp
import requests

class HomeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                # Get Discord access token
                token = SocialToken.objects.get(account__user=request.user, account__provider='discord')
                discord_api_url = 'https://discord.com/api/v10'

                # Fetch user's guilds
                response = requests.get(
                    f'{discord_api_url}/users/@me/guilds',
                    headers={'Authorization': f'Bearer {token.token}'}
                )
                guilds = response.json()

                # Check if the user is a member of the specific Discord server
                if any(guild['id'] == settings.DISCORD_SERVER_ID for guild in guilds):
                    return render(request, 'core/home.html')
                else:
                    return HttpResponseForbidden("You're not a member of the required Discord server.")
            except SocialToken.DoesNotExist:
                return HttpResponseForbidden("Discord authentication is required.")
        else:
            return render(request, 'core/login.html')

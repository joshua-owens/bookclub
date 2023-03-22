import json
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from dotenv import load_dotenv
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Loads Discord credentials from .env file and creates a SocialApp entry'

    def handle(self, *args, **options):
        load_dotenv()
        discord_client_id = os.getenv('DISCORD_CLIENT_ID')
        discord_client_secret = os.getenv('DISCORD_SECRET')

        site = Site.objects.get(pk=1)

        social_app, created = SocialApp.objects.get_or_create(
            provider="discord",
            defaults={
                "name": "Discord",
                "client_id": discord_client_id,
                "secret": discord_client_secret,
                "key": "",
            },
        )

        if not created:
            social_app.client_id = discord_client_id
            social_app.secret = discord_client_secret
            social_app.save()

        social_app.sites.add(site)

        self.stdout.write(self.style.SUCCESS('Discord credentials loaded successfully'))

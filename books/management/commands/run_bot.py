from django.core.management.base import BaseCommand
from books import bot

class Command(BaseCommand):
    help = 'Runs the Discord bot'

    def handle(self, *args, **options):
        bot.client.run(bot.settings.DISCORD_BOT_TOKEN)

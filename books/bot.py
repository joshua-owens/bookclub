import os
import discord
from discord.ext import commands
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from channels.db import database_sync_to_async
from datetime import timedelta
from django.utils import timezone
from .models import BookVote, Book

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

EMOJI_BOOK_ONE = "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}"  # Thumbs Up emoji
EMOJI_BOOK_TWO = "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}"  # Thumbs Down emoji

async def get_book_data(isbn):
    service = build("books", "v1", developerKey=settings.GOOGLE_API_KEY)
    data = service.volumes().list(q=f"isbn:{isbn}").execute()

    if data["totalItems"] > 0:
        volume_info = data["items"][0]["volumeInfo"]

        print(volume_info["imageLinks"])
        cover_url = None
        if "imageLinks" in volume_info:
            cover_url = volume_info["imageLinks"]["thumbnail"]

        return {
            "isbn": isbn,
            "title": volume_info.get("title", ""),
            "author": ", ".join(volume_info.get("authors", [])),
            "description": volume_info.get("description", ""),
            "cover_url": cover_url,
        }
    else:
        return None

@database_sync_to_async
def create_book_vote(book1, book2, vote_message):
    expires_at = timezone.now() + timedelta(weeks=2)
    book_vote = BookVote(book1=book1, book2=book2, expires_at=expires_at, discord_message_id=vote_message.id, discord_channel_id=vote_message.channel.id)
    book_vote.save()
    return book_vote

@database_sync_to_async
def update_book_vote(vote_message_id, book1_votes, book2_votes):
    book_vote = BookVote.objects.filter(discord_message_id=vote_message_id).first()
    if book_vote:
        book_vote.update_vote_counts(book1_votes, book2_votes)
    return book_vote

async def count_votes(vote_message):
    book1_votes = 0
    book2_votes = 0

    for reaction in vote_message.reactions:
        if str(reaction.emoji) == EMOJI_BOOK_ONE:
            book1_votes = reaction.count - 1  # Subtract 1 to exclude the bot's own reaction
        elif str(reaction.emoji) == EMOJI_BOOK_TWO:
            book2_votes = reaction.count - 1  # Subtract 1 to exclude the bot's own reaction

    return book1_votes, book2_votes

@database_sync_to_async
def create_or_update_book(book_data):
    book, _ = Book.objects.update_or_create(
        isbn=book_data["isbn"],
        defaults={
            "title": book_data["title"],
            "author": book_data["author"],
            "description": book_data["description"],
            "cover_url": book_data["cover_url"],
        },
    )
    return book


async def remove_reaction(message, emoji, user):
    reaction = discord.utils.get(message.reactions, emoji=str(emoji))
    if reaction:
        await reaction.remove(user)

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    channel = client.get_channel(payload.channel_id)
    vote_message = await channel.fetch_message(payload.message_id)

    guild = client.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    if user is None:
        user = await guild.fetch_member(payload.user_id)

    if str(payload.emoji) == EMOJI_BOOK_ONE:
        await remove_reaction(vote_message, EMOJI_BOOK_TWO, user)
    elif str(payload.emoji) == EMOJI_BOOK_TWO:
        await remove_reaction(vote_message, EMOJI_BOOK_ONE, user)

    book1_votes, book2_votes = await count_votes(vote_message)
    await update_book_vote(vote_message.id, book1_votes, book2_votes)


@client.command()
async def vote(ctx, isbn1: str, isbn2: str):
    book1_data = await get_book_data(isbn1)
    book2_data = await get_book_data(isbn2)

    if book1_data and book2_data:
        book1 = await create_or_update_book(book1_data)
        book2 = await create_or_update_book(book2_data)
        embed1 = discord.Embed(
            title=f"Book 1: {book1.title} by {book1.author}",
            description=f"ISBN: {book1.isbn}\n{book1.description}\n\u200B",
            # color=discord.Color.red()
        )
        embed1.set_image(url=book1.cover_url)

        embed2 = discord.Embed(
            title=f"Book 2: {book2.title} by {book2.author}",
            description=f"ISBN: {book2.isbn}\n{book2.description}\n\u200B",
            # color=discord.Color.blue()
        )
        embed2.set_image(url=book2.cover_url)

        vote_message = await ctx.send(
            content=f"React with {EMOJI_BOOK_ONE} for Book 1 or {EMOJI_BOOK_TWO} for Book 2",
            embeds=[embed1, embed2]
        )


        await vote_message.add_reaction(EMOJI_BOOK_ONE)
        await vote_message.add_reaction(EMOJI_BOOK_TWO)
        await create_book_vote(book1, book2, vote_message)

    else:
        await ctx.send("Invalid ISBN(s) provided.")

    await ctx.message.delete()
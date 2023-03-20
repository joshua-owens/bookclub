# Generated by Django 4.1.7 on 2023-03-19 22:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=60)),
                ("auther", models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name="BookVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("book1_title", models.CharField(max_length=255)),
                ("book2_title", models.CharField(max_length=255)),
                ("book1_votes", models.IntegerField(default=0)),
                ("book2_votes", models.IntegerField(default=0)),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                (
                    "end_time",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 4, 2, 22, 30, 57, 869260)
                    ),
                ),
                ("discord_message_id", models.BigIntegerField()),
                ("discord_channel_id", models.BigIntegerField()),
                ("expired", models.BooleanField(default=False)),
            ],
        ),
    ]

from django.db import models
import datetime

class Book(models.Model):
    title = models.CharField(max_length=255, default='')
    author = models.CharField(max_length=255, default='')
    isbn = models.CharField(max_length=13, unique=True, default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.title

class BookVote(models.Model):
    book1 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_vote_book1', default=None)
    book2 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_vote_book2', default=None)
    book1_votes = models.IntegerField(default=0)
    book2_votes = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    discord_message_id = models.BigIntegerField()
    discord_channel_id = models.BigIntegerField()
    expired = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default=None)

    def __str__(self):
        return f'{self.book1} vs {self.book2}'

    def update_vote_counts(self, book1_votes: int, book2_votes: int):
        self.book1_votes = book1_votes
        self.book2_votes = book2_votes
        self.save()

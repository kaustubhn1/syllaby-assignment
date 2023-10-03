from django.db import models
from user.models import Profile


class Book(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    book_name = models.CharField(blank=False, null=False, max_length=256)
    content = models.JSONField(null=True, default={"sections": []})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name

from django.db import models
from user.models import Profile
from book.models import Book


class BookCollaboratorMapper(models.Model):
    collaborator = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    access_revoked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.book_name} | {self.collaborator.user.username}"
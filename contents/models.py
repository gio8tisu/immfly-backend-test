import uuid

from django.db import models


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    language = models.ForeignKey("ChannelLanguage", on_delete=models.PROTECT)
    picture = models.ImageField()


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.IntegerField()  # TODO: Must be between 0-10.
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey("ContentGenre", on_delete=models.PROTECT)
    description = models.CharField(max_length=1024)
    authors = models.ManyToManyField("Author")


class ChannelLanguage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=5, unique=True)


class ContentGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)

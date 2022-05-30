import uuid

from django.db import models


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    language = models.CharField(max_length=16)


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.IntegerField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)

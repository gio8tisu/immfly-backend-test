import uuid

from django.db import models


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    language = models.ForeignKey("ChannelLanguage", on_delete=models.PROTECT)
    picture = models.ImageField()
    parent_channel = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subchannels",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_reference",
                check=models.Q(parent_channel=None)
                | ~models.Q(parent_channel=models.F("id")),
            ),
        ]


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField()
    rating = models.IntegerField()  # TODO: Must be between 0-10.
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="contents", null=True
    )
    genre = models.ForeignKey("ContentGenre", on_delete=models.PROTECT)
    description = models.CharField(max_length=1024)
    authors = models.ManyToManyField("Author")


class ChannelLanguage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=5, unique=True)


class ContentGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32, unique=True)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ChannelManager(models.Manager):
    def create_channel(self, title, language, picture, subchannels, contents):
        if subchannels and contents:
            raise ValidationError("Channel cannot have both subchannels and contents")
        if not subchannels and not contents:
            raise ValidationError("Channel must have subchannels or contents")

        new_channel = Channel(title=title, language=language, picture=picture)
        new_channel.full_clean()
        new_channel.save()

        if subchannels:
            new_channel.subchannels.add(*subchannels)
        if contents:
            new_channel.contents.add(*contents)

        return new_channel


class Channel(models.Model):
    objects = ChannelManager()

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
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="contents",
        null=True,
        blank=True,
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

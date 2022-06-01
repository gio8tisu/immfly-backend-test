import factory
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.test import TestCase

from contents.factories import (AuthorFactory, ChannelLanguageFactory,
                                ContentFactory, ContentGenreFactory)
from contents.models import Channel


class ContentTests(TestCase):
    def test_content_factory_is_valid(self):
        author = AuthorFactory()
        genre = ContentGenreFactory()
        content = ContentFactory.build(authors=[author], genre=genre)
        content.full_clean()

    def test_content_cannot_be_created_with_higher_rating(self):
        author = AuthorFactory()
        genre = ContentGenreFactory()
        content = ContentFactory.build(rating=100, authors=[author], genre=genre)
        with self.assertRaises(ValidationError):
            content.full_clean()

    def test_content_cannot_be_created_with_lower_rating(self):
        author = AuthorFactory()
        genre = ContentGenreFactory()
        content = ContentFactory.build(rating=-100, authors=[author], genre=genre)
        with self.assertRaises(ValidationError):
            content.full_clean()


class ChannelTests(TestCase):
    def test_create_channel_works_with_content(self):
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        language = ChannelLanguageFactory()

        genre = ContentGenreFactory()
        author = AuthorFactory()
        content = ContentFactory(authors=[author], genre=genre)

        channel = Channel.objects.create_channel(
            "Title", language, picture, [], [content]
        )

    def test_create_channel_works_with_subchannels(self):
        language = ChannelLanguageFactory()
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        genre = ContentGenreFactory()
        author = AuthorFactory()
        content = ContentFactory(authors=[author], genre=genre)
        subchannel = Channel.objects.create_channel(
            "Subchannel", language, picture, [], [content]
        )

        channel = Channel.objects.create_channel(
            "Channel", language, picture, [subchannel], []
        )

    def test_create_channel_fails_with_no_subchannels_or_content(self):
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        language = ChannelLanguageFactory()

        with self.assertRaises(ValidationError):
            channel = Channel.objects.create_channel(
                "Channel", language, picture, None, None
            )

    def test_create_channel_fails_with_subchannels_and_content(self):
        language = ChannelLanguageFactory()
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        genre = ContentGenreFactory()
        author = AuthorFactory()
        sub_content = ContentFactory(authors=[author], genre=genre)
        content = ContentFactory(authors=[author], genre=genre)
        subchannel = Channel.objects.create_channel(
            "Subchannel", language, picture, [], [sub_content]
        )

        with self.assertRaises(ValidationError):
            channel = Channel.objects.create_channel(
                "Channel", language, picture, [subchannel], [content]
            )

import factory
from django.core.files.base import ContentFile
from django.test import TestCase

from contents.factories import (AuthorFactory, ChannelLanguageFactory,
                                ContentFactory, ContentGenreFactory)
from contents.models import Channel
from contents.services import compute_channel_rating


class TestChannelRatingAlgorithm(TestCase):
    def test_channel_with_single_content_works(self):
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        language = ChannelLanguageFactory()

        genre = ContentGenreFactory()
        author = AuthorFactory()
        content = ContentFactory(authors=[author], genre=genre, rating=10)

        channel = Channel.objects.create_channel(
            "Title", language, picture, [], [content]
        )

        channel_rating = compute_channel_rating(channel)

        self.assertEqual(channel_rating, 10)

    def test_channel_with_multiple_contents_works(self):
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        language = ChannelLanguageFactory()

        genre = ContentGenreFactory()
        author = AuthorFactory()
        content1 = ContentFactory(authors=[author], genre=genre, rating=10)
        content2 = ContentFactory(authors=[author], genre=genre, rating=5)

        channel = Channel.objects.create_channel(
            "Title", language, picture, [], [content1, content2]
        )

        channel_rating = compute_channel_rating(channel)

        self.assertEqual(channel_rating, 7.5)

    def test_channel_with_subchannels_works(self):
        language = ChannelLanguageFactory()
        picture = ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 1024}),
            "example.jpg",
        )
        genre = ContentGenreFactory()
        author = AuthorFactory()
        content1 = ContentFactory(authors=[author], genre=genre, rating=10)
        content2 = ContentFactory(authors=[author], genre=genre, rating=5)
        subchannel1 = Channel.objects.create_channel(
            "Subchannel", language, picture, [], [content1, content2]
        )
        content3 = ContentFactory(authors=[author], genre=genre, rating=10)
        subchannel2 = Channel.objects.create_channel(
            "Subchannel", language, picture, [], [content3]
        )

        channel = Channel.objects.create_channel(
            "Channel", language, picture, [subchannel1, subchannel2], []
        )

        channel_rating = compute_channel_rating(channel)

        # Subchannel 1 has rating of 7.5
        # Subchannel 2 has rating of 10
        # Channel should have rating of 8.75
        self.assertEqual(channel_rating, 8.75)

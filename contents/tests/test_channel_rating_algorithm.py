import factory
from django.core.files.base import ContentFile
from django.test import TestCase

from contents.factories import (AuthorFactory, ChannelFactory,
                                ChannelLanguageFactory, ContentFactory,
                                ContentGenreFactory)
from contents.models import Channel
from contents.services import compute_channel_rating


class TestChannelRatingAlgorithm(TestCase):
    def test_channel_with_single_content_works(self):
        content = ContentFactory(rating=10)
        channel = ChannelFactory(contents=[content])

        channel_rating = compute_channel_rating(channel)

        self.assertEqual(channel_rating, 10)

    def test_channel_with_multiple_contents_works(self):
        content1 = ContentFactory(rating=10)
        content2 = ContentFactory(rating=5)

        channel = ChannelFactory(contents=[content1, content2])

        channel_rating = compute_channel_rating(channel)

        self.assertEqual(channel_rating, 7.5)

    def test_channel_with_subchannels_works(self):
        content1 = ContentFactory(rating=10)
        content2 = ContentFactory(rating=5)
        subchannel1 = ChannelFactory(contents=[content1, content2])
        content3 = ContentFactory(rating=10)
        subchannel2 = ChannelFactory(contents=[content3])

        channel = ChannelFactory(subchannels=[subchannel1, subchannel2])

        channel_rating = compute_channel_rating(channel)

        # Subchannel 1 has rating of 7.5
        # Subchannel 2 has rating of 10
        # Channel should have rating of 8.75
        self.assertEqual(channel_rating, 8.75)

from django.test import TestCase

from contents.factories import ChannelFactory, ContentFactory
from contents.services import get_node_channels


class TestGetRootChannels(TestCase):
    def test_channel_with_subchannels_works(self):
        content1 = ContentFactory(rating=10)
        content2 = ContentFactory(rating=5)
        subchannel1 = ChannelFactory(contents=[content1, content2])
        content3 = ContentFactory(rating=10)
        subchannel2 = ChannelFactory(contents=[content3])
        subchannel3 = ChannelFactory(subchannels=[subchannel2])

        channel = ChannelFactory(subchannels=[subchannel1, subchannel3])

        self.assertEqual(get_node_channels().get(), channel)

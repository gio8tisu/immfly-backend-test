from django.test import TestCase
from rest_framework import status

from contents.factories import ChannelFactory, ContentFactory


class TestChannelAPI(TestCase):
    def test_channel_detail_with_single_content_works(self):
        content_rating = 10.0
        content = ContentFactory(rating=content_rating)
        channel = ChannelFactory(contents=[content])

        response = self.client.get(f"/api/channels/{channel.id}/")

        expected_data = {
            "id": str(channel.id),
            "title": channel.title,
            "language": channel.language.language,
            "rating": content_rating,
            "subchannels": [],
            "contents": [f"http://testserver/api/contents/{content.id}/"],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)

    def test_channel_detail_with_single_subchannel_works(self):
        content_rating = 10.0
        content1 = ContentFactory(rating=content_rating)
        content2 = ContentFactory(rating=content_rating)
        subchannel = ChannelFactory(contents=[content1, content2])

        channel = ChannelFactory(subchannels=[subchannel])

        response = self.client.get(f"/api/channels/{channel.id}/")

        expected_data = {
            "id": str(channel.id),
            "title": channel.title,
            "language": channel.language.language,
            "rating": content_rating,
            "subchannels": [f"http://testserver/api/channels/{subchannel.id}/"],
            "contents": [],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)

    def test_channel_list_works(self):
        content_rating = 10.0
        content1 = ContentFactory(rating=content_rating)
        content2 = ContentFactory(rating=content_rating)
        subchannel1 = ChannelFactory(contents=[content1, content2])
        content3 = ContentFactory(rating=content_rating)
        subchannel2 = ChannelFactory(contents=[content3])
        channel = ChannelFactory(subchannels=[subchannel1, subchannel2])

        response = self.client.get(f"/api/channels/")

        expected_data = {
            "id": str(channel.id),
            "title": channel.title,
            "language": channel.language.language,
            "rating": content_rating,
            "subchannels": [
                f"http://testserver/api/channels/{subchannel1.id}/",
                f"http://testserver/api/channels/{subchannel2.id}/",
            ],
            "contents": [],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(response.data[0], expected_data)

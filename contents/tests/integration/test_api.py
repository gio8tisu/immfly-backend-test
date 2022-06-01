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
            "contents": [
                {
                    "id": str(content.id),
                    "file": f"http://testserver{content.file.url}",
                    "description": content.description,
                    "rating": content_rating,
                    "genre": content.genre.name,
                    "authors": [],
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, expected_data)

    def test_channel_detail_with_single_subchannel_works(self):
        self.maxDiff = None
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
            "subchannels": [
                {
                    "id": str(subchannel.id),
                    "title": subchannel.title,
                    "language": subchannel.language.language,
                    "rating": content_rating,
                    "contents": [
                        {
                            "id": str(content1.id),
                            "file": f"http://testserver{content1.file.url}",
                            "description": content1.description,
                            "rating": content_rating,
                            "genre": content1.genre.name,
                            "authors": [],
                        },
                        {
                            "id": str(content2.id),
                            "file": f"http://testserver{content2.file.url}",
                            "description": content2.description,
                            "rating": content_rating,
                            "genre": content2.genre.name,
                            "authors": [],
                        },
                    ],
                    "subchannels": [],
                }
            ],
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
                {
                    "id": str(subchannel1.id),
                    "title": subchannel1.title,
                    "language": subchannel1.language.language,
                    "rating": content_rating,
                    "contents": [
                        {
                            "id": str(content1.id),
                            "file": f"http://testserver{content1.file.url}",
                            "description": content1.description,
                            "rating": content_rating,
                            "genre": content1.genre.name,
                            "authors": [],
                        },
                        {
                            "id": str(content2.id),
                            "file": f"http://testserver{content2.file.url}",
                            "description": content2.description,
                            "rating": content_rating,
                            "genre": content2.genre.name,
                            "authors": [],
                        },
                    ],
                    "subchannels": [],
                },
                {
                    "id": str(subchannel2.id),
                    "title": subchannel2.title,
                    "language": subchannel2.language.language,
                    "rating": content_rating,
                    "contents": [
                        {
                            "id": str(content3.id),
                            "file": f"http://testserver{content3.file.url}",
                            "description": content3.description,
                            "rating": content_rating,
                            "genre": content3.genre.name,
                            "authors": [],
                        },
                    ],
                    "subchannels": [],
                },
            ],
            "contents": [],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(response.data[0], expected_data)

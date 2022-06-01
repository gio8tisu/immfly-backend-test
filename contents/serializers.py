from rest_framework import serializers

from .models import Channel, Content
from .services import compute_channel_rating


class ContentSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True)
    authors = serializers.SlugRelatedField(
        slug_field="full_name", read_only=True, many=True
    )

    class Meta:
        model = Content
        fields = ["id", "file", "description", "rating", "genre", "authors"]


class ChannelSerializer(serializers.ModelSerializer):
    language = serializers.SlugRelatedField(slug_field="language", read_only=True)
    rating = serializers.SerializerMethodField()
    contents = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="content-detail"
    )
    subchannels = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="channel-detail"
    )

    def get_rating(self, obj):
        return compute_channel_rating(obj)

    class Meta:
        model = Channel
        fields = ["id", "title", "language", "rating", "contents", "subchannels"]

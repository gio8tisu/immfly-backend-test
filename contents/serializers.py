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
    contents = ContentSerializer(many=True)

    def get_rating(self, obj):
        return compute_channel_rating(obj)

    def get_fields(self):
        # Override to allow self-referencing nested serialization.
        fields = super().get_fields()
        fields["subchannels"] = ChannelSerializer(many=True)
        return fields

    class Meta:
        model = Channel
        fields = ["id", "title", "language", "rating", "contents", "subchannels"]

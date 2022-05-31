from rest_framework import serializers

from .models import Channel, Content


class ContentSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True)
    authors = serializers.SlugRelatedField(
        slug_field="full_name", read_only=True, many=True
    )

    class Meta:
        model = Content
        fields = ["id", "file", "rating", "genre", "authors"]


class ChannelSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Channel
        fields = ["id", "title", "language", "contents"]

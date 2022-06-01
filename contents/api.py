from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer
from .services import get_channels_with_subchannels


@api_view(["GET"])
def channels_list(request):
    """
    List channels.
    """
    channels = get_channels_with_subchannels()
    serializer = ChannelSerializer(channels, context={"request": request}, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def channel_detail(request, pk):
    """
    Retrieve a channel.
    """
    channel = get_object_or_404(Channel, pk=pk)

    serializer = ChannelSerializer(channel, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def content_detail(request, pk):
    """
    Retrieve a content.
    """
    content = get_object_or_404(Content, pk=pk)

    serializer = ContentSerializer(content)
    return Response(serializer.data)

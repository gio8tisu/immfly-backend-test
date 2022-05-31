from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Channel
from .serializers import ChannelSerializer


@api_view(["GET"])
def channels_list(request):
    """
    List channels.
    """
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def channel_detail(request, pk):
    """
    Retrieve a channel.
    """
    channel = get_object_or_404(Channel, pk=pk)

    serializer = ChannelSerializer(channel)
    return Response(serializer.data)

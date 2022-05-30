from rest_framework import views, response

from .models import Channel
from .serializers import (
    ChannelSerializer,
)


class ChannelsListAPI(views.APIView):
    def get(self, request):
        channels = Channel.objects.all()
        serializer = ChannelSerializer(channels, many=True)
        return response.Response(serializer.data)

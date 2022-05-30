from django.urls import path

from .api import (
    ChannelsListAPI,
)

urlpatterns = [
    path("api/channels/", ChannelsListAPI.as_view(), "channels-list"),
]

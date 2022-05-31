from django.urls import path

from .api import (
    ChannelsListAPI,
)

urlpatterns = [
    path("channels/", ChannelsListAPI.as_view(), name="channels-list"),
]

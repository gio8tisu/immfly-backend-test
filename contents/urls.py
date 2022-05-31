from django.urls import path

from .api import channel_detail, channels_list

urlpatterns = [
    path("channels/", channels_list, name="channels-list"),
    path("channels/<pk>/", channel_detail, name="channel-detail"),
]

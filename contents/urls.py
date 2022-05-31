from django.urls import path

from .api import channels_list

urlpatterns = [
    path("channels/", channels_list, name="channels-list"),
]

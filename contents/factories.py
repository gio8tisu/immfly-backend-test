import factory

from .models import Channel


class ChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Channel

    title = "TV Shows"

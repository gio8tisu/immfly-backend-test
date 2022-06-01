from django.db.models import Avg, Count

from .models import Channel


def compute_channel_rating(channel):
    """Compute channel rating based on its content.

    The rating of a channel is the average of the ratings of all the channels
    underneath, if the channel has no subchannels its rating is the average of the
    ratings of its contents. If a channel has no contents, it does not affect the
    ratings of its parent since its value is undefined.

    Assumes channel has been created with `ChannelManager`'s `create_channel`
    method, i.e. it has either subchannels or content and doesn't reference
    itself.
    """
    if channel.contents.count():
        return channel.contents.all().aggregate(Avg("rating"))["rating__avg"]

    # Channel has subchannels.
    subchannels_ratings = [compute_channel_rating(s) for s in channel.subchannels.all()]
    return sum(subchannels_ratings) / len(subchannels_ratings)


def get_node_channels():
    return Channel.objects.filter(parent_channel=None)

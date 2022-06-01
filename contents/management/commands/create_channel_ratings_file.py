import csv
import logging
from operator import itemgetter

from django.core.management.base import BaseCommand

from contents.models import Channel
from contents.services import compute_channel_rating

logger = logging.getLogger("main")


class Command(BaseCommand):
    help = "creates CSV file with channels ratings."

    def add_arguments(self, parser):
        parser.add_argument("output_file", help="Path to CSV file")

    def handle(self, **options):
        with open(options["output_file"], "w", newline="") as fd:
            fieldnames = ["channel_id", "channel_rating"]
            writer = csv.DictWriter(fd, fieldnames=fieldnames)
            writer.writeheader()

            logger.info("Computing channel ratings")

            ratings = []
            for channel in Channel.objects.all():
                rating = compute_channel_rating(channel)
                ratings.append({"channel_id": channel.id, "channel_rating": rating})

            ratings.sort(key=itemgetter("channel_rating"), reverse=True)

            logger.info("Writing CSV file")
            writer.writerows(ratings)

from django.core.management.base import BaseCommand, CommandError
from recommender_main.models import Anime

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        print(len(Anime.objects.all()))
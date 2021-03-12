from django.core.management.base import BaseCommand, CommandError
from recommender_main.models import Anime
import pprint
import json
class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        with open('recommendations_1.json') as f:
            data_1 = json.load(f)
            pprint.pprint(data_1['https://myanimelist.net/anime/37779/Yakusoku_no_Neverland'])

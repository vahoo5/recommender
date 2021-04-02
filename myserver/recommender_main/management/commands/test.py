from django.core.management.base import BaseCommand, CommandError
from recommender_main.models import Anime
import pprint
import json
import jellyfish
class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        print(jellyfish.levenshtein_distance('Steins;Gate', 'Steins;Gate'))

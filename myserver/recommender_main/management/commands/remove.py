from django.core.management.base import BaseCommand, CommandError
from recommender_main.models import Anime
import pprint
class Command(BaseCommand):
    help = 'remove record by id'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        id = kwargs['id']
        try:
            asd = Anime.objects.filter(id=id).delete()
            print(asd)
        except:
            print('cant remove that')
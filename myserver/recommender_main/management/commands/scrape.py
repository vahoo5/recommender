from django.core.management.base import BaseCommand, CommandError
from recommender_main.mal_helper import UrlGenerator, AnimeScraper
from recommender_main.models import Anime
import pprint
from recommender_main.worker import Worker
from queue import Queue
import time
import logging
from datetime import date

class Command(BaseCommand):
    help = 'scrape and save'

    def add_arguments(self, parser):
        parser.add_argument('n_top', type=int, nargs='+')

    def handle(self, *args, **kwargs):
        logging.basicConfig(filename=f'{str(date.today())}_scrape.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
        start = time.time()
        n_top = kwargs['n_top']
        min_ = n_top[0]
        max_ = n_top[1]

        gen = UrlGenerator(min_, max_)
        scraper1 = AnimeScraper()
        scraper2 = AnimeScraper()
        scraper3 = AnimeScraper()

        url_queue = Queue(maxsize=max_-min_)
        url_parser = Worker(url_queue, gen, name='urlparser')

        anime_parser1 = Worker(url_queue, scraper1, loader=False, name='animeparser1')
        anime_parser2 = Worker(url_queue, scraper2, loader=False, name='animeparser2')
        anime_parser3 = Worker(url_queue, scraper3, loader=False, name='animeparser3')

        url_parser.start()
        anime_parser1.start()
        anime_parser2.start()
        anime_parser3.start()

        anime_parser1.join()
        anime_parser2.join()
        anime_parser3.join()

        scraper1.finish()
        scraper2.finish()
        scraper3.finish()

        finish = time.time() - start
        print(str(finish))
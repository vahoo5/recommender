from threading import Thread
from .models import Anime
import logging


class Worker(Thread):
    def __init__(self, queue, scraper, loader=True, daemon=True, name=None):
        Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.scraper = scraper
        self.loader = loader

    def run(self):
        if self.loader:
            it = self.scraper.scrape_top_x_urls()
            urls = ''
            while True:
                urls = next(it)
                if urls == 'done':
                    self.queue.put(urls)
                    break
                for u in urls:
                    self.queue.put(u)
                logging.info(self.name + f" put {len(urls)} urls in queue")
        else:
            while True:
                url = self.queue.get()
                if url == 'done':
                    self.queue.put('done')
                    print(f'{self.name} is done')
                    break
                anime_dct = self.scraper.scrape_anime_from_url(url)
                anime = Anime(**anime_dct)
                anime.save()
                logging.info('save successful')
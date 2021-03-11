import requests
import time
from bs4 import BeautifulSoup as BS
import logging
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class AnimeScraper():
    def __init__(self):
        self.toSplit = ['Synonyms', 'Producers', 'Licensors', 'Studios']
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.headless = True
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.selectorTitle = 'h1.title-name.h1_bold_none'
        self.selectorDescription = 'p[itemprop=description]'
        self.selectorFeatures = '#content>table>tbody>tr>td.borderClass>div>h2 ~ div'
        self.selectorGenres = '#content>table>tbody>tr>td.borderClass>div>h2 ~ div>span[itemprop=genre]'
        self.selectorScore = '#content>table>tbody>tr>td.borderClass>div>h2 ~ div>span[itemprop=ratingValue]'
        self.btn = '#reform > button'
        self.timeout = 20

    def finish(self):
        self.browser.quit()

    def scrape_anime_from_url(self, url):
        while True:
            try:
                self.browser.get(url)
                html = self.browser.page_source
                soup = BS(html, features='html.parser')
                description = soup.select(self.selectorDescription)
                name = soup.select(self.selectorTitle)
                elements = soup.select(self.selectorFeatures)
                genres = [x.text for x in soup.select(self.selectorGenres)]
                score = float(soup.select(self.selectorScore)[0].text)
                dict1 = dict([x.text.strip().split(':',1) for x in elements if x.text.strip()!=''])
                dict1 = (lambda dct: {x.lower():dct[x].strip() for x in dct.keys()})(dict1)
                values = [','.join([y.strip() for y in dict1[x].split(',')]) if x in self.toSplit
                        else dict1[x].split('\n')[0].strip()[:-1] if x == 'ranked'
                        else score if x == 'score'
                        else ','.join(genres) if x == 'genres'
                        else dict1[x]
                        for x in dict1.keys()]
                finalDict = {x:y for x,y in zip(dict1.keys(),values)}
                finalDict['name'] = name[0].text
                finalDict['description'] = description[0].text.replace('[Written by MAL Rewrite]', '').strip()
                finalDict['url'] = url
                finalDict['kind'] = finalDict.pop('type')
                finalDict['ranked'] = int(finalDict['ranked'].replace('#', ''))

                finalDict['popularity'] = -1
                try:
                    finalDict['popularity'] = int(finalDict['popularity'].replace('#', ''))
                except:
                    pass
                finalDict['members'] = -1
                try:
                    finalDict['members'] = int(finalDict['members'].replace(',', ''))
                except:
                    pass
                finalDict['favorites'] = -1
                try:
                    finalDict['favorites'] = int(finalDict['favorites'].replace(',', ''))
                except:
                    pass
                finalDict['episodes'] = -1
                try:
                    finalDict['episodes'] = int(finalDict['episodes'])
                except:
                    pass
                return finalDict

            except Exception as e:
                try:
                    self.browser.find_element_by_css_selector(self.btn).click()
                    logging.log('clicked button')
                except Exception as e:
                    print('couldnt click')
                logging.error(e)
                logging.error(f'waiting {self.timeout} seconds, before retrying to scrape {url}')
                time.sleep(self.timeout)

class UrlGenerator():
    def __init__(self, min_, max_):
        self.minx = min_
        self.maxx = max_
        self.selectorTopAnime = 'tr.ranking-list>td.title.al.va-t.word-break>a'
        self.listUrl = 'https://myanimelist.net/topanime.php?limit='
        self.timeout = 20

    def scrape_top_x_urls(self):
        count = 0
        iters = (self.maxx - self.minx) // 50
        while count < iters:
            response = requests.get(self.listUrl + str(self.minx + count * 50), "html.parser")
            if response.status_code == 200:
                try:
                    soup = BS(response.text, features="html.parser")
                    urls = [x['href'] for x in soup.select(self.selectorTopAnime)]
                    logging.info(f'done - at {self.minx + count * 50} now')
                    yield urls
                    count += 1
                except Exception as e:
                    logging.error(f'stopped at limit: {self.minx + count * 50}, while getting urls, waiting {self.timeout} seconds')
                    time.sleep(self.timeout)
            else:
                logging.error('not 200 status code')
        yield 'done' 
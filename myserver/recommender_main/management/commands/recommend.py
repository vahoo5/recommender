from recommender_main.models import Anime
from django.core.management.base import BaseCommand, CommandError
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval

def getSimilar(cosine_sim):
    results = {}
    for idx, row in animes.iterrows():
        similar_indices = cosine_sim[idx].argsort()[:-50:-1] 
        similar_items = [(cosine_sim[idx][i], animes['Url'][i]) for i in similar_indices] 
        results[row['Url']] = similar_items[1:]
    return results

def toJson(result, name):
    a = pd.DataFrame(result)
    a = a.transpose()
    a.to_json('recommendations_'+ name +'.json',orient='index')

def get_time_in_min(s):
    types = ['hr', 'sec', 'min']
    time_in_min = 0
    for i in types:
        temp = re.search('[0-9]+ '+ i, s)
        if type(temp) is re.Match:
            t = re.search('[0-9]+', temp.group()).group()
            if i == 'hr':
                time_in_min += int(t)*60
            elif i == 'min':
                time_in_min += int(t)
            else:
                time = int(t)/60
                time_in_min += time
    return time_in_min
    
class Command(BaseCommand):
    help = 'calculate recommendations'

    def handle(self, *args, **kwargs):
        df = pd.DataFrame(list(Anime.objects.filter(id__lte=100).values()))
        print(df.head())
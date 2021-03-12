from recommender_main.models import Anime
from django.core.management.base import BaseCommand, CommandError
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval

def getSimilar(cosine_sim, animes):
    results = {}
    print(animes.tail())
    for idx, row in animes.iterrows():
        
        similar_indices = cosine_sim[idx].argsort()[:-50:-1] 
        similar_items = [(cosine_sim[idx][i], animes['url'].iloc[i]) for i in similar_indices] 
        results[row['url']] = similar_items[1:]
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
    
def clean(animes):
    animes['duration'] = animes['duration'].apply(lambda x: get_time_in_min(x))
    animes['description'] = animes['description'].apply(lambda x: re.sub('\[Source.*\]|\(Source.*\)|Source.*|\[.*(by|By).*\]','',x).strip())
    animes['genres'] = animes['genres'].apply(lambda x: [y.replace(' ','') for y in x.split(',')])
    animes['metadata'] = animes.apply(lambda x : ' '.join(x['genres']), axis = 1)
    animes = animes[(lambda x: [True if y in ['TV', 'Movie'] else False for y in x])(animes['kind'])]
    animes = animes[(lambda x: [True if y>15 else False for y in x])(animes['duration'])]
    animes.index = [x for x in range(animes.shape[0])]
    return animes


class Command(BaseCommand):
    help = 'calculate recommendations'

    def handle(self, *args, **kwargs):
        animes = pd.DataFrame(list(Anime.objects.all().values()))
        animes = clean(animes)
        print(animes.shape)
        tf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tf.fit_transform(animes['description'])
        cosine_similarities_description = linear_kernel(tfidf_matrix, tfidf_matrix)

        count_vec = CountVectorizer(stop_words='english')
        count_vec_matrix = count_vec.fit_transform(animes['metadata'])

        cosine_similarities_metadata = cosine_similarity(count_vec_matrix, count_vec_matrix)
        cosine_similarities_05 = (cosine_similarities_description + cosine_similarities_metadata) / 2

        print(cosine_similarities_description.shape)
        print(cosine_similarities_metadata.shape)
        results_1 = getSimilar(cosine_similarities_metadata, animes)
        results_05 = getSimilar(cosine_similarities_05, animes)
        results_0 = getSimilar(cosine_similarities_description, animes)
        toJson(results_1, '1')
        toJson(results_05, '05')
        toJson(results_0, '0')
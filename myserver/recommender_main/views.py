from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from .models import Anime
import json
import pprint
class DisplayAll(View):
    def post(self, request):
        url = request.POST.get('anime_url')
        top_n = request.POST.get('top_n')
        by_genre = request.POST.get('recommendation_type1')
        by_description = request.POST.get('recommendation_type2')
        by_mixed = request.POST.get('recommendation_type3')

        info = ''
        top_list_1 = None
        top_list_05 = None
        top_list_0 = None

        if url:
            url=str(url)
            try:
                if by_genre:
                    with open('recommendations_1.json') as f:
                        data_1 = json.load(f)
                    top_1 = data_1[url]
                    top_list_1 = [top_1[str(x)] for x in range(int(top_n))]
                if by_description:
                    with open('recommendations_05.json') as f:
                        data_05 = json.load(f)
                    top_05 = data_05[url]
                    top_list_05 = [top_05[str(x)] for x in range(int(top_n))]
                if by_mixed:
                    with open('recommendations_0.json') as f:
                        data_0 = json.load(f)
                    top_0 = data_0[url]
                    top_list_0 = [top_0[str(x)] for x in range(int(top_n))]

            except KeyError as e:
                info = 'This anime is not in the database.'

        all_animes = Anime.objects.filter(id__lte=80)
        context = { 'animes' : all_animes,
                    'info' : info,
                    'top_1' : top_list_1,
                    'top_05' : top_list_05,
                    'top_0' : top_list_0}
        return render(request=request, template_name="index.html", context=context)
    def get(self, request):
        return render(request=request, template_name="index.html", context=None)
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from .models import Anime
import json
import pprint
class DisplayAll(View):
    def get(self, request):
        url = request.GET.get('anime_url')
        top_n = request.GET.get('top_n')
        info = ''
        top_list_1 = None
        top_list_07 = None
        if url:
            url=str(url)
            with open('recommendations_1.json') as f:
                data_1 = json.load(f)
            with open('recommendations_07.json') as f:
                data_07 = json.load(f)
            try:
                top_1 = data_1[url]
                top_07 = data_07[url]
                pprint.pprint(top_1)
                top_list_1 = [top_1[str(x)] for x in range(int(top_n))]
                top_list_07 = [top_07[str(x)] for x in range(int(top_n))]
            except KeyError as e:
                info = 'This anime is not in the database.'
        all_animes = Anime.objects.filter(id__lte=80)
        context = { 'animes' : all_animes,
                    'info' : info,
                    'top_1' : top_list_1,
                    'top_07' : top_list_07}
        return render(request=request, template_name="index.html", context=context)

def index(request):
    a = Anime.objects.all()[0]
    fields = Anime._meta.get_fields()
    asd = ''
    for f in fields:
        asd += f.name + str(getattr(a, f.name)) + '\n'
    return HttpResponse(asd)
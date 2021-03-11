from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from .models import Anime

class DisplayAll(View):
    def get(self, request):
        all_animes = Anime.objects.all()
        context = {'animes' : all_animes}
        return render(request=request, template_name="index.html", context=context)

def index(request):
    a = Anime.objects.all()[0]
    fields = Anime._meta.get_fields()
    asd = ''
    for f in fields:
        asd += f.name + str(getattr(a, f.name)) + '\n'
    return HttpResponse(asd)
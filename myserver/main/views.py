from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View

class HomePageView(View):
    
    def get(self, request):
        context = {'title' : 'szia'}
        return render(request=request, template_name="homepage.html", context=context)

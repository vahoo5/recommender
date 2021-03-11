from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.DisplayAll.as_view(), name='recommender_main'),
]
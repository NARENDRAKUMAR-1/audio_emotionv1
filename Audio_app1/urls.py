
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),

    path('', views.home, name='home' ),

    path('audio/', views.Audio_store),
    path('audio/audio/', views.Audio_store),

    path('audio/audio/result/', views.analyse_audio),
]
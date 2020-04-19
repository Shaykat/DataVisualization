from django.urls import path
from . import views

"""Url mapping with the view methods for visual app"""
app_name = 'visual'
urlpatterns = [
    path('', views.index, name='index'),
    path('world_wide/', views.world_wide, name='world_wide'),
    path('country_wide/', views.country_wide, name='country_wide'),
    path('timeline/', views.time_line, name='time_line'),
]

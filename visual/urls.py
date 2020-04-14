from django.urls import path
from . import views

app_name = 'visual'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('world_wide/', views.world_wide, name='world_wide'),
    path('country_wide/', views.country_wide, name='country_wide'),
    path('timeline/', views.time_line, name='time_line'),
    path('covid_line_chart/', views.covid_line_chart, name='covid_line_chart'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]

from django.urls import path
from . import views

app_name = 'visual'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('covid_chart/', views.covid_chart, name='covid_chart'),
    path('covid_line_chart/', views.covid_line_chart, name='covid_line_chart'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]

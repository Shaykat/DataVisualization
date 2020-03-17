from django.urls import path
from . import views

app_name = 'visual'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('covid_chart/', views.covid_chart, name='covid_chart'),
    path('covid_bubble_chart/', views.covid_bubble_chart, name='covid_bubble_chart'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]

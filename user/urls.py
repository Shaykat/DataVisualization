from django.urls import path, include
from .views import (user_list, signup, log_in, upload_data)

"""Url mapping with the view methods for user app"""
app_name = "user"
urlpatterns = [
    path('', user_list, name='user_list'),
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='log_in'),
    path('upload_data/', upload_data, name='upload_data'),

]

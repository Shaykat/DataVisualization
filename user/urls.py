from django.urls import path, include
from .views import (users, signup, log_in, upload_data)
urlpatterns = [
    path('', users, name='userlist'),
    path('signup/', signup, name='signup'),
    path('login/', log_in, name='log_in'),
    path('upload_data/', upload_data, name='upload_data'),

]

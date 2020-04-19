import re
import pandas as pd
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Users
from visual.models import CovidObservation
from visual.views import index
from .form import SignupForm, LoginForm, UploadForm
from datetime import datetime


def user_list(request):
    """Load the user list"""
    context = {}
    context['items'] = Users.objects.all()
    return render(request, 'user_list.html', context)


def signup(request):
    """if the password1 and password2 matches then create user and then redirect the user to user_list view"""
    form = SignupForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        authenticate(username=username, password=password)
        form.save()
        return redirect('/user')
    else:
        form = SignupForm()
    return render(request, './signup.html', {'form': form})


def log_in(request):
    """if the username and password matches then this view redirect the user to home page if user type is user"""
    """else to upload_data page"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = Users.objects.filter(username=form.data['username'])[0]
            if user:
                if user.user_type == 1:
                    return redirect('index')
                else:
                    return redirect('user:upload_data')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def upload_data(request):
    """Get the file uploaded by user from request then read the file using pandas then parse all the columns"""
    """Convert the string date to datetime and create instances of the  CovidObservation class"""
    """and save them into database"""
    if request.method == 'POST':
        csv_file = request.FILES['file']
        data = pd.read_csv(csv_file)

        # you can use the re library --> import re
        observations = data['ObservationDate']
        province = data['Province/State']
        country = data['Country/Region']
        confirmed = data['Confirmed']
        deaths = data['Deaths']
        recovered = data['Recovered']
        # rows = re.split('\n', data.decode('utf-8'))  # splits along new line
        objs = []
        for i, row in enumerate(observations):
            DATE_FORMAT = "%Y-%m-%d"
            DATE_FORMAT_ = "%m/%d/%Y"
            yyyymmdd = observations[i] if observations[i] else ""
            if yyyymmdd:
                yyyymmdd = datetime.strptime(datetime.strftime(datetime.strptime(yyyymmdd, DATE_FORMAT_), DATE_FORMAT), DATE_FORMAT)

            objs.append(CovidObservation(
                serial_num=i,
                observation_date=yyyymmdd,
                confirmed_case=confirmed[i] if confirmed[i] else 0,
                death_case=deaths[i] if deaths[i] else 0,
                recovered_case=recovered[i] if recovered[i] else 0,
                province_id=province[i] if province[i] else "",
                country_id=country[i] if country[i] else "",
            ))
        CovidObservation.objects.bulk_create(objs)
        return redirect('http://127.0.0.1:8000/visual')
    else:
        form = UploadForm()
        return render(request, 'upload_data.html', {'form': form})

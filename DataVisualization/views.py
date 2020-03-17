from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


def index(request):
    context = {}
    return render(request, './index.html', context)
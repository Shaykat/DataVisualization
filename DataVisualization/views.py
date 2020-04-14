from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from visual.models import CovidObservation
from visual.views import get_queryset


def index(request):
    template = loader.get_template('./index.html')
    context_object_name = 'observation_list'
    search_query = ""
    latest_date = CovidObservation.objects.latest('observation_date').observation_date

    if request.method == 'GET':
        search_query = request.GET.get('country', "")
    queryset = get_queryset(search_query, 'country')

    context = {
        context_object_name: queryset.filter(observation_date=latest_date)
    }

    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    return HttpResponse(template.render(context, request))
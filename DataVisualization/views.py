from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from visual.models import CovidObservation
from visual.views import get_queryset


def index(request):
    """Index view. This view render the home page and pass the list of all cases in the last day from database"""
    template = loader.get_template('./index.html')
    context_object_name = 'observation_list'
    """ Find the last date from database"""
    latest_date = CovidObservation.objects.latest('observation_date').observation_date
    """Get the Query set for worldwide cases"""
    queryset = get_queryset(request, 'country')

    """Make the dictionary and filter the queryset by latest date"""
    context = {
        context_object_name: queryset.filter(observation_date=latest_date)
    }

    """if the request came from any ajax call, data will be sent as Json"""
    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    """if it is not a ajax call it will return http response"""
    return HttpResponse(template.render(context, request))

import json
from django.template.loader import render_to_string
from django.views import generic
from django.db.models import Sum, Q
from django.http import JsonResponse, HttpResponse
from django.template import loader
from .models import CovidObservation


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

    """if the request came from any ajax call, data will be populate in html table to be rendered in the front end"""
    """and send as Json"""
    if request.is_ajax():
        html = render_to_string(
            template_name="covid_list_partial_view.html",
            context=context
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    """if it is not a ajax call it will return http response"""
    return HttpResponse(template.render(context, request))


def world_wide(request):
    """This view process data for all the countries death, confirmed and recovered case and send as Json Response"""
    template = loader.get_template('./world_wide.html')
    context_object_name = 'observation_list'
    data = []

    """ Find the last date from database"""
    latest_date = CovidObservation.objects.latest('observation_date').observation_date
    """Get the Query set for worldwide cases"""
    queryset = get_queryset(request, 'country').filter(observation_date=latest_date)

    """format the data get from query, according to the client need"""
    for entry in queryset.order_by('-country_confirmed_case')[:30]:
        data.append({
            'country': entry['country_id'],
            'confirmed_cases': entry['country_confirmed_case'],
            'death_cases': entry['country_death_case'],
            'recovered_cases': entry['country_recovered_case'],
        })

    """Convert the dictionary data into Jason data"""
    context = {
        context_object_name: json.dumps(data)
    }
    """if the request came from any ajax call, send as Json Response"""
    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    """if it is not a ajax call it will return http response"""
    return HttpResponse(template.render(context, request))


def country_wide(request):
    """This view process data for all the Province death, confirmed and recovered case and send as Json Response"""
    template = loader.get_template('./country_wide.html')
    context_object_name = 'observation_list'
    data = []

    """ Find the last date from database"""
    latest_date = CovidObservation.objects.latest('observation_date').observation_date
    """Get the Query set for countrywide cases"""
    queryset = get_queryset(request, 'province').filter(observation_date=latest_date)

    """format the data get from query, according to the client need"""
    for entry in queryset.order_by('-Province_confirmed_case')[:20]:
        data.append({
            'province': entry['province_id'],
            'cases': entry['Province_confirmed_case'],
        })

    """Convert the dictionary data into Jason data"""
    context = {
        context_object_name: json.dumps(data)
    }

    """if the request came from any ajax call, send as Json Response"""
    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    """if it is not a ajax call it will return http response"""
    return HttpResponse(template.render(context, request))


def time_line(request):
    """This view process data as date wise death, confirmed and recovered case for whole world and send as Json"""
    template = loader.get_template('./time_line.html')
    context_object_name = 'observation_list'
    days = 0
    data = []

    """Parse days from Get request"""
    if request.method == 'GET':
        days = int(request.GET.get('days', 0))

    """Get the Query set for timeline"""
    queryset = get_queryset(request, 'timeline')

    """If user request for 30 days timeline this view will render last_30_days template"""
    if days:
        template = loader.get_template('./last_30_days.html')
        queryset = queryset[:days]

    """format the data get from query, according to the client need"""
    for entry in queryset:
        data.append({
            'observation_date': str(entry['observation_date']),
            'confirmed_cases': entry['country_confirmed_case'],
            'death_cases': entry['country_death_case'],
            'recovered_cases': entry['country_recovered_case'],
        })

    """Convert the dictionary data into Jason data"""
    context = {
        context_object_name: json.dumps(data)
    }

    """if the request came from any ajax call, send as Json Response"""
    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    """if it is not a ajax call it will return http response"""
    return HttpResponse(template.render(context, request))


def get_the_search_string(request):
    """ Parse the search string from Get Request"""
    search_query = ""
    if request.method == 'GET':
        search_query = request.GET.get('country', None)
    return search_query


def get_queryset(request, group_by):
    """Get the search string"""
    search_query = get_the_search_string(request)

    """If query request for country wide then group by province, group by country when ask for worldwide"""
    """if ask for timeline group by date and returns the queryset return by django ORM"""
    if group_by == 'province':
        if search_query:
            queryset = CovidObservation.objects.values('country_id', 'province_id', 'observation_date').annotate(
                Province_confirmed_case=Sum('confirmed_case'),
                Province_death_case=Sum('death_case'),
                Province_recovered_case=Sum('recovered_case')).filter(
                country_id=search_query).order_by('-Province_confirmed_case')
        else:
            queryset = CovidObservation.objects.values('country_id', 'province_id', 'observation_date').annotate(
                Province_confirmed_case=Sum('confirmed_case'),
                Province_death_case=Sum('death_case'),
                Province_recovered_case=Sum('recovered_case')).order_by('-Province_confirmed_case')
    elif group_by == 'country':
        if search_query:
            queryset = CovidObservation.objects.values('country_id', 'observation_date').annotate(
                country_confirmed_case=Sum('confirmed_case'),
                country_death_case=Sum('death_case'),
                country_recovered_case=Sum('recovered_case')).filter(
                country_id=search_query).order_by('-country_confirmed_case')
        else:
            queryset = CovidObservation.objects.values('country_id', 'observation_date').annotate(
                country_confirmed_case=Sum('confirmed_case'),
                country_death_case=Sum('death_case'),
                country_recovered_case=Sum('recovered_case')).order_by('-country_confirmed_case')
    else:
        if search_query:
            queryset = CovidObservation.objects.values('country_id', 'observation_date').annotate(
                country_confirmed_case=Sum('confirmed_case'),
                country_death_case=Sum('death_case'),
                country_recovered_case=Sum('recovered_case')).filter(
                country_id=search_query).order_by('-observation_date')
        else:
            queryset = CovidObservation.objects.values('observation_date').annotate(
                country_confirmed_case=Sum('confirmed_case'),
                country_death_case=Sum('death_case'),
                country_recovered_case=Sum('recovered_case')).order_by('-observation_date')
    return queryset


import json
from django.template.loader import render_to_string
from django.views import generic
from django.db.models import Sum, Q
from django.http import JsonResponse, HttpResponse
from django.template import loader
from .models import CovidObservation


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
        html = render_to_string(
            template_name="covid_list_partial_view.html",
            context=context
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return HttpResponse(template.render(context, request))


def world_wide(request):
    template = loader.get_template('./world_wide.html')
    context_object_name = 'observation_list'
    search_query = ""
    data = []

    latest_date = CovidObservation.objects.latest('observation_date').observation_date
    if request.method == 'GET':
        search_query = request.GET.get('country', None)
    queryset = get_queryset(search_query, 'country').filter(observation_date=latest_date)

    for entry in queryset.order_by('-country_confirmed_case')[:30]:
        data.append({
            'country': entry['country_id'],
            'confirmed_cases': entry['country_confirmed_case'],
            'death_cases': entry['country_death_case'],
            'recovered_cases': entry['country_recovered_case'],
        })

    context = {
        context_object_name: json.dumps(data)
    }

    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    return HttpResponse(template.render(context, request))


def country_wide(request):
    template = loader.get_template('./country_wide.html')
    context_object_name = 'observation_list'
    search_query = ""
    data = []

    latest_date = CovidObservation.objects.latest('observation_date').observation_date
    if request.method == 'GET':
        search_query = request.GET.get('country', None)
    queryset = get_queryset(search_query, 'province').filter(observation_date=latest_date)

    for entry in queryset.order_by('-Province_confirmed_case')[:20]:
        data.append({
            'province': entry['province_id'],
            'cases': entry['Province_confirmed_case'],
        })

    context = {
        context_object_name: json.dumps(data)
    }

    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    return HttpResponse(template.render(context, request))


def time_line(request):
    template = loader.get_template('./time_line.html')
    context_object_name = 'observation_list'
    search_query = ""
    days = 0
    data = []

    if request.method == 'GET':
        search_query = request.GET.get('country', None)
        days = int(request.GET.get('days', 0))
    queryset = get_queryset(search_query, 'timeline')
    if days:
        template = loader.get_template('./last_30_days.html')
        queryset = queryset[:days]

    for entry in queryset:
        data.append({
            'observation_date': str(entry['observation_date']),
            'confirmed_cases': entry['country_confirmed_case'],
            'death_cases': entry['country_death_case'],
            'recovered_cases': entry['country_recovered_case'],
        })

    context = {
        context_object_name: json.dumps(data)
    }

    if request.is_ajax():
        return JsonResponse(data=context, safe=False)

    return HttpResponse(template.render(context, request))


def get_queryset(search_query, group_by):
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


def covid_chart(request):
    labels = []
    data = []
    search_query = ""
    if request.method == 'GET':
        search_query = request.GET.get('country', None)

    queryset = CovidObservation.objects.values('country_id', 'province_id').annotate(
        Province_confirmed_case=Sum('confirmed_case'))
    if search_query:
        queryset = queryset.filter(country_id=search_query)
    for entry in queryset.order_by('-Province_confirmed_case')[:10]:
        labels.append(entry['province_id'])
        data.append(entry['Province_confirmed_case'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def covid_line_chart(request):
    labels = []
    data = []

    search_query = ""
    if request.method == 'GET':
        search_query = request.GET.get('country', None)

    queryset = CovidObservation.objects.values('country_id').annotate(
        Country_death_case=Sum('death_case')).order_by('-Country_death_case')[:5]
    for entry in queryset:
        labels.append(entry['country_id'])
        data.append(entry['Country_death_case'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


from django.views import generic
from django.db.models import Sum, Q
from django.http import JsonResponse, HttpResponse
from django.template import loader
from .models import Country, Province, CovidObservation


# class IndexView(generic.ListView):
#     template_name = './index.html'
#     context_object_name = 'observation_list'
#
#     def get_queryset(self):
#         """Return the last five published observation."""
#         search_query = ""
#         if self.request.method == 'GET':
#             search_query = self.request.GET.get('country', None)
#
#         queryset = CovidObservation.objects.values('country_id__name', 'province_id__name').annotate(
#             Province_confirmed_case=Sum('confirmed_case'),
#             Province_death_case=Sum('death_case')).order_by('-Province_confirmed_case')
#
#         # return CovidObservation.objects.order_by('-observation_date')[:5]
#         return queryset


def index(request):
    template = loader.get_template('./index.html')
    context_object_name = 'observation_list'
    search_query = ""

    if request.method == 'GET':
        search_query = request.GET.get('country', None)

    queryset = CovidObservation.objects.values('country_id__name', 'province_id__name').annotate(
        Province_confirmed_case=Sum('confirmed_case'),
        Province_death_case=Sum('death_case')).filter(country_id__name=search_query).order_by('-Province_confirmed_case')

    context = {
        context_object_name: queryset
    }

    return HttpResponse(template.render(context, request))


class DetailView(generic.DetailView):
    model = Country
    template_name = './detail.html'


def covid_chart(request):
    labels = []
    data = []
    search_query = ""
    if request.method == 'GET':
        search_query = request.GET.get('country', None)

    queryset = CovidObservation.objects.values('country_id__name', 'province_id__name').annotate(
        Province_confirmed_case=Sum('confirmed_case'))
    if search_query:
        queryset = queryset.filter(country_id__name=search_query)
    for entry in queryset.order_by('-Province_confirmed_case')[:10]:
        labels.append(entry['province_id__name'])
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

    queryset = CovidObservation.objects.values('country_id__name').annotate(
        Country_death_case=Sum('death_case')).order_by('-Country_death_case')[:5]
    for entry in queryset:
        labels.append(entry['country_id__name'])
        data.append(entry['Country_death_case'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


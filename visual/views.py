from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Sum
from django.http import JsonResponse
from tablib import Dataset
from .models import Country, Province, CovidObservation


class IndexView(generic.ListView):
    template_name = './index.html'
    context_object_name = 'observation_list'

    def get_queryset(self):
        """Return the last five published observation."""
        queryset = CovidObservation.objects.values('country_id__name', 'province_id__name').annotate(Province_confirmed_case=Sum('confirmed_case')).order_by('-Province_confirmed_case')
        # for entry in queryset:
        #     labels.append(entry['country_id__name'])
        #     data.append(entry['country_confirmed_case'])

        # return CovidObservation.objects.order_by('-observation_date')[:5]
        return queryset


class DetailView(generic.DetailView):
    model = Country
    template_name = './detail.html'


def covid_chart(request):
    labels = []
    data = []

    queryset = CovidObservation.objects.values('country_id__name', 'province_id__name').annotate(Province_confirmed_case=Sum('confirmed_case')).order_by('-Province_confirmed_case')
    for entry in queryset:
        labels.append(entry['province_id__name'])
        data.append(entry['Province_confirmed_case'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def covid_bubble_chart(request):
    label_x = []
    label_y = []
    data = []

    queryset = CovidObservation.objects.values('country_id__name', 'province_id__name').annotate(Province_confirmed_case=Sum('confirmed_case')).order_by('-Province_confirmed_case')
    for entry in queryset:
        label_x.append(entry['country_id__name'])
        label_y.append(entry['province_id__name'])
        data.append(entry['Province_confirmed_case'])

    return JsonResponse(data={
        'label_x': label_x,
        'label_y': label_y,
        'data': data,
    })


# def simple_upload(request):
#     if request.method == 'POST':
#         covid_resource = CovidResource()
#         dataset = Dataset()
#         new_persons = request.FILES['myfile']
#
#         imported_data = dataset.load(new_persons.read())
#         result = covid_resource.import_data(dataset, dry_run=True)  # Test the data import
#
#         if not result.has_errors():
#             covid_resource.import_data(dataset, dry_run=False)  # Actually import now
#
#     return render(request, './index.html')


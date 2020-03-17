from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Country, Province, CovidObservation

admin.site.register(Country)
admin.site.register(Province)
admin.site.register(CovidObservation)


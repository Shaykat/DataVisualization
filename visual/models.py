import datetime
from django.db import models
from django.utils import timezone
from import_export import resources


class Country(models.Model):
    id = models.IntegerField('Country ID', primary_key=True)
    name = models.CharField('Country Name', max_length=100)

    def __str__(self):
        return self.name


class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    id = models.IntegerField('Province ID', primary_key=True)
    name = models.CharField('Province Name', max_length=100)

    def __str__(self):
        return self.name


class CovidObservation(models.Model):
    serial_num = models.IntegerField('Serial Number')
    observation_date = models.DateTimeField('Observation Date')
    last_update = models.DateTimeField('Last Update')
    confirmed_case = models.IntegerField('Confirmed Cases')
    death_case = models.IntegerField('Death Cases')
    month = models.CharField
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.serial_num)

    def was_published_recently(self):
        return self.observation_date >= timezone.now() - datetime.timedelta(days=1)

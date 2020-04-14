import datetime
from django.db import models
from django.utils import timezone


class CovidObservation(models.Model):
    serial_num = models.IntegerField('Serial Number')
    observation_date = models.DateTimeField('Observation Date')
    last_update = models.DateTimeField('Last Update', null=True, default=datetime.datetime.now())
    confirmed_case = models.IntegerField('Confirmed Cases', default=0)
    death_case = models.IntegerField('Death Cases', default=0)
    recovered_case = models.IntegerField('Recovered Cases', default=0)
    city = models.CharField('City', max_length=100, null=True, blank=True)
    province_id = models.CharField('Province', max_length=100)
    country_id = models.CharField('Country', max_length=100)

    def __str__(self):
        return str(self.serial_num)

    def was_published_recently(self):
        return self.observation_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        self.last_update = datetime.datetime.now()
        super(CovidObservation, self).save(*args, **kwargs)

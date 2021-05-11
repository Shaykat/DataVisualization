import datetime

from django.test import TestCase
from django.utils import timezone

from .models import CovidObservation


def latest_date_check(start_date, end_date):
    return start_date < end_date


class CovidObservationModelTests(TestCase):
    def test_latest_observation_date(self):
        latest_date = CovidObservation.objects.latest('observation_date').observation_date
        date = datetime.today()
        self.assertIs(latest_date_check(latest_date, date), False)

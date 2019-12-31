from unittest import TestCase

from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse

#from . import views

class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('/reports/patient/1/'))
        self.assertEquals(response.status_code, 200)

class loggedTests(TestCase):
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='nkrings', password='JunJana19')
        response = self.client.get(reverse('reports'))

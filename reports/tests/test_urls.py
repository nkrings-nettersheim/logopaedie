from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reports.views import search_patient, add_patient, edit_patient, patient

class TestUrls(SimpleTestCase):

    def test_url_search_patient_is_resolved(self):
        url = reverse('reports/search/patient/')
        self.assertEqual(resolve(url).func, search_patient)

    def test_url_add_patient_is_resolved(self):
        url = reverse('add_patient')
        self.assertEqual(resolve(url).func.view_class, add_patient)

    def test_url_edit_patient_is_resolved(self):
        url = reverse('edit_patient')
        self.assertEqual(resolve(url).func.view_class, edit_patient)

    def test_url_patient_is_resolved(self):
        url = reverse('patient')
        self.assertEqual(resolve(url).func.view_class, patient)

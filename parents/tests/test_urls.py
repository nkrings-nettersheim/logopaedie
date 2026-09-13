from django.test import SimpleTestCase
from django.urls import reverse, resolve

from parents.views import (ParentsSheetWizard, generate_qr_code, ParentsSheetListView,
                            ParentsSheetUpdateView, move_parents_sheet_to_document)


class TestParentsUrls(SimpleTestCase):

    def test_url_parents_qr_code_is_resolved(self):
        url = reverse('parents:parents_qr_code')
        self.assertEqual(resolve(url).func, generate_qr_code)

    def test_url_parents_sheet_wizard_is_resolved(self):
        url = reverse('parents:parents_sheet_wizard', args=['some-token'])
        self.assertEqual(resolve(url).func.view_class, ParentsSheetWizard)

    def test_url_success_page_is_resolved(self):
        url = reverse('parents:success_page')
        self.assertEqual(resolve(url).view_name, 'parents:success_page')

    def test_url_parents_sheet_list_is_resolved(self):
        url = reverse('parents:parents_sheet_list')
        self.assertEqual(resolve(url).func.view_class, ParentsSheetListView)

    def test_url_parents_sheet_edit_is_resolved(self):
        url = reverse('parents:parents_sheet_edit', args=['1'])
        self.assertEqual(resolve(url).func.view_class, ParentsSheetUpdateView)

    def test_url_move_parents_sheet_is_resolved(self):
        url = reverse('parents:move_parents_sheet', args=['1'])
        self.assertEqual(resolve(url).func, move_parents_sheet_to_document)

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reports.views import index, impressum, search_patient, add_patient, edit_patient, patient,\
    add_therapy, edit_therapy, therapy, add_process_report, edit_process_report, process_report, \
    delete_process_report, add_therapy_report, edit_therapy_report, therapy_report, show_therapy_report, \
    show_process_report, search_doctor_start, search_doctor, edit_doctor, add_doctor, doctor, \
    search_therapist_start, search_therapist, edit_therapist, add_therapist, therapist, search_diagnostic_group_start,\
    search_diagnostic_group, edit_diagnostic_group, add_diagnostic_group, diagnostic_group, add_ia, edit_ia, \
    upload_document, download_document, del_document, upload_document_therapy, download_document_therapy, \
    del_document_therapy, add_therapy_something, edit_therapy_something, open_reports, therapy_breaks, update_report,\
    getSessionTimer, getOpenReports, add_waitlist, edit_waitlist, delete_waitlist_item, set_waitlist_item_inactive, \
    set_waitlist_item_active, add_pa_something




class TestUrls(SimpleTestCase):

    def test_url_index_is_resolved(self):
        url = reverse('reports:index')
        self.assertEqual(resolve(url).func, index)

    def test_url_impressum_is_resolved(self):
        url = reverse('reports:impressum')
        self.assertEqual(resolve(url).func, impressum)

    def test_url_search_patient_is_resolved(self):
        url = reverse('reports:search_patient')
        self.assertEqual(resolve(url).func, search_patient)

    def test_url_add_patient_is_resolved(self):
        url = reverse('reports:add_patient')
        self.assertEqual(resolve(url).func, add_patient)

    def test_url_edit_patient_is_resolved(self):
        url = reverse('reports:edit_patient', args=['1'])
        self.assertEqual(resolve(url).func, edit_patient)

    def test_url_patient_is_resolved(self):
        url = reverse('reports:patient', args=['1'])
        self.assertEqual(resolve(url).func, patient)

    def test_url_add_therapy_is_resolved(self):
        url = reverse('reports:add_therapy')
        self.assertEqual(resolve(url).func, add_therapy)

    def test_url_edit_therapy_is_resolved(self):
        url = reverse('reports:edit_therapy', args=['1'])
        self.assertEqual(resolve(url).func, edit_therapy)

    def test_url_therapy_is_resolved(self):
        url = reverse('reports:therapy', args=['1'])
        self.assertEqual(resolve(url).func, therapy)

################################################################################################
    def test_url_add_process_report_is_resolved(self):
        url = reverse('reports:add_process_report')
        self.assertEqual(resolve(url).func, add_process_report)

    def test_url_edit_process_report_is_resolved(self):
        url = reverse('reports:edit_process_report', args=['1'])
        self.assertEqual(resolve(url).func, edit_process_report)

    def test_url_process_report_is_resolved(self):
        url = reverse('reports:process_report', args=['1'])
        self.assertEqual(resolve(url).func, process_report)

    def test_url_show_process_report_is_resolved(self):
        url = reverse('reports:show_process_report')
        self.assertEqual(resolve(url).func, show_process_report)

    def test_url_delete_process_report_is_resolved(self):
        url = reverse('reports:delete_process_report', args=['1'])
        self.assertEqual(resolve(url).func, delete_process_report)

################################################################################################
    def test_url_add_therapy_report_is_resolved(self):
        url = reverse('reports:add_therapy_report')
        self.assertEqual(resolve(url).func, add_therapy_report)

    def test_url_edit_therapy_report_is_resolved(self):
        url = reverse('reports:edit_therapy_report', args=['1'])
        self.assertEqual(resolve(url).func, edit_therapy_report)

    def test_url_therapy_report_is_resolved(self):
        url = reverse('reports:therapy_report', args=['1'])
        self.assertEqual(resolve(url).func, therapy_report)

    def test_url_show_therapy_report_is_resolved(self):
        url = reverse('reports:show_therapy_report')
        self.assertEqual(resolve(url).func, show_therapy_report)

    def test_url_search_doctor_start_is_resolved(self):
        url = reverse('reports:search_doctor_start')
        self.assertEqual(resolve(url).func, search_doctor_start)

    def test_url_search_doctor_is_resolved(self):
        url = reverse('reports:search_doctor')
        self.assertEqual(resolve(url).func, search_doctor)

    def test_url_edit_doctor_is_resolved(self):
        url = reverse('reports:edit_doctor', args=['1'])
        self.assertEqual(resolve(url).func, edit_doctor)

    def test_url_add_doctor_is_resolved(self):
        url = reverse('reports:add_doctor')
        self.assertEqual(resolve(url).func, add_doctor)

    def test_url_doctor_is_resolved(self):
        url = reverse('reports:doctor', args=['1'])
        self.assertEqual(resolve(url).func, doctor)

    def test_url_search_therapist_start_is_resolved(self):
        url = reverse('reports:search_therapist_start')
        self.assertEqual(resolve(url).func, search_therapist_start)

    def test_url_search_therapist_is_resolved(self):
        url = reverse('reports:search_therapist')
        self.assertEqual(resolve(url).func, search_therapist)

    def test_url_edit_therapist_is_resolved(self):
        url = reverse('reports:edit_therapist', args=['1'])
        self.assertEqual(resolve(url).func, edit_therapist)

    def test_url_add_therapist_is_resolved(self):
        url = reverse('reports:add_therapist')
        self.assertEqual(resolve(url).func, add_therapist)

    def test_url_therapist_is_resolved(self):
        url = reverse('reports:therapist', args=['1'])
        self.assertEqual(resolve(url).func, therapist)

################################################################################################

    def test_url_search_diagnostic_group_start_is_resolved(self):
        url = reverse('reports:search_diagnostic_group_start')
        self.assertEqual(resolve(url).func, search_diagnostic_group_start)

    def test_url_search_diagnostic_group_is_resolved(self):
        url = reverse('reports:search_diagnostic_group')
        self.assertEqual(resolve(url).func, search_diagnostic_group)

    def test_url_edit_diagnostic_group_is_resolved(self):
        url = reverse('reports:edit_diagnostic_group', args=['1'])
        self.assertEqual(resolve(url).func, edit_diagnostic_group)

    def test_url_add_diagnostic_group_is_resolved(self):
        url = reverse('reports:add_diagnostic_group')
        self.assertEqual(resolve(url).func, add_diagnostic_group)

    def test_url_diagnostic_group_is_resolved(self):
        url = reverse('reports:diagnostic_group', args=['1'])
        self.assertEqual(resolve(url).func, diagnostic_group)

################################################################################################

    def test_url_add_ia_is_resolved(self):
        url = reverse('reports:add_ia')
        self.assertEqual(resolve(url).func, add_ia)

    def test_url_edit_ia_is_resolved(self):
        url = reverse('reports:edit_ia', args=['1'])
        self.assertEqual(resolve(url).func, edit_ia)

################################################################################################

    def test_url_document_is_resolved(self):
        url = reverse('reports:document')
        self.assertEqual(resolve(url).func, upload_document)

    def test_url_download_is_resolved(self):
        url = reverse('reports:download')
        self.assertEqual(resolve(url).func, download_document)

    def test_url_del_document_is_resolved(self):
        url = reverse('reports:delete', args=['1'])
        self.assertEqual(resolve(url).func.view_class, del_document)

################################################################################################

    def test_url_document_therapy_is_resolved(self):
        url = reverse('reports:document_therapy')
        self.assertEqual(resolve(url).func, upload_document_therapy)

    def test_url_download_therapy_is_resolved(self):
        url = reverse('reports:download_therapy')
        self.assertEqual(resolve(url).func, download_document_therapy)

    def test_url_delete_therapy_is_resolved(self):
        url = reverse('reports:delete_therapy', args=['1'])
        self.assertEqual(resolve(url).func.view_class, del_document_therapy)

################################################################################################

    def test_url_add_something_is_resolved(self):
        url = reverse('reports:add_something')
        self.assertEqual(resolve(url).func, add_therapy_something)

    def test_url_edit_something_is_resolved(self):
        url = reverse('reports:edit_something', args=['1'])
        self.assertEqual(resolve(url).func, edit_therapy_something)

################################################################################################

    def test_url_open_reports_is_resolved(self):
        url = reverse('reports:open_reports')
        self.assertEqual(resolve(url).func, open_reports)

################################################################################################

    def test_url_therapy_breaks_is_resolved(self):
        url = reverse('reports:therapy_breaks')
        self.assertEqual(resolve(url).func, therapy_breaks)

    def test_url_update_report_is_resolved(self):
        url = reverse('reports:update_report', args=['1'])
        self.assertEqual(resolve(url).func, update_report)

################################################################################################

    def test_url_getSessionTimer_is_resolved(self):
        url = reverse('reports:getSessionTimer')
        self.assertEqual(resolve(url).func, getSessionTimer)

    def test_url_getOpenReports_is_resolved(self):
        url = reverse('reports:getOpenReports')
        self.assertEqual(resolve(url).func, getOpenReports)

################################################################################################

    def test_url_add_waitlist_is_resolved(self):
        url = reverse('reports:add_waitlist')
        self.assertEqual(resolve(url).func, add_waitlist)

    def test_url_edit_waitlist_is_resolved(self):
        url = reverse('reports:edit_waitlist', args=['1'])
        self.assertEqual(resolve(url).func, edit_waitlist)

    def test_url_delete_waitlist_item_is_resolved(self):
        url = reverse('reports:delete_waitlist_item', args=['1'])
        self.assertEqual(resolve(url).func, delete_waitlist_item)

    def test_url_set_waitlist_item_inactive_is_resolved(self):
        url = reverse('reports:set_waitlist_item_inactive', args=['1'])
        self.assertEqual(resolve(url).func, set_waitlist_item_inactive)

    def test_url_set_waitlist_item_active_is_resolved(self):
        url = reverse('reports:set_waitlist_item_active', args=['1'])
        self.assertEqual(resolve(url).func, set_waitlist_item_active)


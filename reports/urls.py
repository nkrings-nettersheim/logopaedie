from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),

    path('search/patient/', views.search_patient, name='search_patient'),
    path('add/patient/', views.add_patient, name='add_patient'),
    path('edit/patient/<id>/', views.edit_patient, name='edit_patient'),
    path('patient/<id>/', views.patient, name='patient'),

    path('add/therapy/', views.add_therapy, name='add_therapy'),
    path('edit/therapy/<id>/', views.edit_therapy, name='edit_therapy'),
    path('therapy/<id>/', views.therapy, name='therapy'),

    path('add/process_report/', views.add_process_report, name='add_process_report'),
    path('edit/process_report/<id>/', views.edit_process_report, name='edit_process_report'),
    path('process_report/<id>/', views.process_report, name='process_report'),
    path('show_process_report/', views.show_process_report, name='show_process_report'),
    path('delete_process_report/<id>', views.delete_process_report, name='delete_process_report'),

    path('add/therapy_report/', views.add_therapy_report, name='add_therapy_report'),
    path('edit/therapy_report/<id>/', views.edit_therapy_report, name='edit_therapy_report'),
    path('therapy_report/<id>/', views.therapy_report, name='therapy_report'),
    path('show_therapy_report/', views.show_therapy_report, name='show_therapy_report'),
    path('save_therapyreport_element/', views.save_therapyreport_element, name='save_therapyreport_element'),

    path('search/doctor/start', views.search_doctor_start, name='search_doctor_start'),
    path('search/doctor/', views.search_doctor, name='search_doctor'),
    path('edit/doctor/<id>/', views.edit_doctor, name='edit_doctor'),
    path('add/doctor/', views.add_doctor, name='add_doctor'),
    path('doctor/<id>/', views.doctor, name='doctor'),

    path('search/therapist/start', views.search_therapist_start, name='search_therapist_start'),
    path('search/therapist/', views.search_therapist, name='search_therapist'),
    path('edit/therapist/<id>/', views.edit_therapist, name='edit_therapist'),
    path('add/therapist/', views.add_therapist, name='add_therapist'),
    path('therapist/<id>/', views.therapist, name='therapist'),

    path('search/diagnostic_group/start', views.search_diagnostic_group_start, name='search_diagnostic_group_start'),
    path('search/diagnostic_group/', views.search_diagnostic_group, name='search_diagnostic_group'),
    path('edit/diagnostic_group/<id>/', views.edit_diagnostic_group, name='edit_diagnostic_group'),
    path('add/diagnostic_group/', views.add_diagnostic_group, name='add_diagnostic_group'),
    path('diagnostic_group/<id>/', views.diagnostic_group, name='diagnostic_group'),

    path('add/ia/', views.add_ia, name='add_ia'),
    path('edit/ia/<id>/', views.edit_ia, name='edit_ia'),

    path('document/', views.upload_document, name='document'),
    path('download/', views.download_document, name='download'),
    path('delete/<pk>', views.del_document.as_view(), name='delete'),

    path('document_therapy/', views.upload_document_therapy, name='document_therapy'),
    path('download_therapy/', views.download_document_therapy, name='download_therapy'),
    path('delete_therapy/<pk>', views.del_document_therapy.as_view(), name='delete_therapy'),

    path('add/something/', views.add_therapy_something, name='add_something'),
    path('edit/something/<id>/', views.edit_therapy_something, name='edit_something'),

    path('add/pa_something/', views.add_pa_something, name='add_pa_something'),
    path('edit/pa_something/<id>/', views.edit_pa_something, name='edit_pa_something'),

    path('open_reports/', views.open_reports, name='open_reports'),

    path('therapy_breaks/', views.therapy_breaks, name='therapy_breaks'),
    path('update_report/<id>', views.update_report, name='update_report'),

    path('getsessiontimer/', views.get_session_timer, name='getsessiontimer'),
    path('getOpenReports/', views.getOpenReports, name='getOpenReports'),
    path('getOpenReportsAjax/', views.getOpenReportsAjax, name='getOpenReportsAjax'),

    path('add/waitlist/', views.add_waitlist, name='add_waitlist'),
    path('edit/waitlist/<id>/', views.edit_waitlist, name='edit_waitlist'),
    path('waitlist/<status>/', views.waitlist, name='waitlist'),
    path('copy/waitlistitem/<id>/', views.copy_waitlist_item, name='copy_waitlist_item'),
    path('delete/waitlistitem/<pk>/', views.delete_waitlist_item.as_view(), name='delete_waitlist_item'),
    path('set/waitlistitem_inactive/<id>/', views.set_waitlist_item_inactive, name='set_waitlist_item_inactive'),
    path('set/waitlistitem_active/<id>/', views.set_waitlist_item_active, name='set_waitlist_item_active'),

    path('list_meta_info/', views.list_meta_info, name='list_meta_info'),

    path('shortcuts/', views.readShortcuts, name='shortcuts'),

]


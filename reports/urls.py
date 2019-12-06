from django.conf.urls import url
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
    path('add/therapy_report/', views.add_therapy_report, name='add_therapy_report'),
    path('edit/therapy_report/<id>/', views.edit_therapy_report, name='edit_therapy_report'),
    path('therapy_report/<id>/', views.therapy_report, name='therapy_report'),
    path('show_therapy_report/', views.show_therapy_report, name='show_therapy_report'),
    path('search/doctor/', views.search_doctor, name='search_doctor'),
    path('edit/doctor/<id>/', views.edit_doctor, name='edit_doctor'),
    path('add/doctor/', views.add_doctor, name='add_doctor'),
    path('doctor/<id>/', views.doctor, name='doctor'),
]

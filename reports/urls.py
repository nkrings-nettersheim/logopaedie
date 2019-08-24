from django.conf.urls import url
from django.urls import path

from . import views


app_name = 'reports'


urlpatterns = [
    path('', views.index, name='index'),
    path('search/patient/', views.search_patient, name='search_patient'),
    path('add/patient/', views.add_patient, name='add_patient'),
    path('edit/patient/<id>/', views.edit_patient, name='edit_patient'),
    path('patient/<id>/', views.patient, name='patient'),
    path('add/therapy/', views.add_therapy, name='add_therapy'),
    path('edit/therapy/<id>/', views.edit_therapy, name='edit_therapy'),
    path('therapy/<id>/', views.therapy, name='therapy'),
    path('add/therapy_report/', views.add_therapy_report, name='add_therapy_report'),
    path('edit/therapy_report/<id>/', views.edit_therapy_report, name='edit_therapy_report'),
    path('therapy_report/<id>/', views.therapy_report, name='therapy_report'),
]

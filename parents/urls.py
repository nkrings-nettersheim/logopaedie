from django.urls import path

from parents import views

app_name = 'parents'

urlpatterns = [
    path('', views.index, name='index'),
    path('parents-form/<str:token>/', views.add_parentssheet, name='parents-form'),
    path('parents-qr-code/', views.generate_qr_code, name='parents-qr-code'),
    #path('qr-code/', views.generate_qr_code, name='qr-code')
]


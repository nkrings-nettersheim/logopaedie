from django.urls import path
from django.views.generic import TemplateView

from parents.views import (ParentsSheetWizard, generate_qr_code,
                           ParentsSheetListView, ParentsSheetUpdateView, move_parents_sheet_to_document)
from parents.forms import (ParentsSheetFormStep1, ParentsSheetFormStep2, ParentsSheetFormStep3, ParentsSheetFormStep4,
                           ParentsSheetFormStep5, ParentsSheetFormStep6)

app_name = 'parents'

urlpatterns = [
    #path('', index, name='index'),
    path('parents-qr-code/', generate_qr_code, name='parents_qr_code'),
    path('parents-sheet/<str:token>/', ParentsSheetWizard.as_view([ParentsSheetFormStep1,
                                                       ParentsSheetFormStep2,
                                                       ParentsSheetFormStep3,
                                                       ParentsSheetFormStep4,
                                                       ParentsSheetFormStep5,
                                                       ParentsSheetFormStep6]), name='parents_sheet_wizard'),

    path('success/', TemplateView.as_view(template_name='parents/success.html'), name='success_page'),
    path('parents-sheet-list/', ParentsSheetListView.as_view(), name='parents_sheet_list'),
    path('parents-sheet/edit/<int:pk>/', ParentsSheetUpdateView.as_view(), name='parents_sheet_edit'),
    path('move/parents_sheet/<int:pk>/', move_parents_sheet_to_document, name='move_parents_sheet'),
]


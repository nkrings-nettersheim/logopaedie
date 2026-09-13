from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Patient, Therapy, Therapy_report, Process_report, Doctor, Therapist, InitialAssessment
from .models import Document, Document_therapy, Diagnostic_group, Wait_list, Login_Failed, Registration


class PatientAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'pa_last_name', 'pa_first_name', 'pa_date_of_birth')

class TherapyAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'recipe_date', 'patients')

class TherapyReportAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'therapy', 'report_date')

class ProcessReportAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'therapy', 'process_treatment', 'created_at')

class InitialAssessmentAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'therapy', 'ia_assessment', 'ia_date')

class RegistrationAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'reg_name', 'reg_first_name', 'reg_created')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name1', 'doctor_name2', 'doctor_city')

admin.site.site_header = "Admin Bereich Logopädische Praxis Schumacher"

admin.site.register(Patient, PatientAdmin)
admin.site.register(Therapy, TherapyAdmin)
admin.site.register(Therapy_report, TherapyReportAdmin)
admin.site.register(Process_report, ProcessReportAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Therapist)
admin.site.register(InitialAssessment, InitialAssessmentAdmin)
admin.site.register(Document)
admin.site.register(Document_therapy)
admin.site.register(Diagnostic_group)
admin.site.register(Wait_list)
admin.site.register(Login_Failed)
admin.site.register(Registration, RegistrationAdmin)

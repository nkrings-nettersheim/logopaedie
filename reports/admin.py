from django.contrib import admin
from .models import Patient, Therapy, Therapy_report, Process_report, Doctor, Therapist, InitialAssessment


class TherapyAdmin(admin.ModelAdmin):
    list_display = ('recipe_date', 'patients')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name1', 'doctor_name2', 'doctor_city')

admin.site.site_header = "Admin Bereich Logopädie Klein"

admin.site.register(Patient)
admin.site.register(Therapy, TherapyAdmin)
admin.site.register(Therapy_report)
admin.site.register(Process_report)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Therapist)
admin.site.register(InitialAssessment)

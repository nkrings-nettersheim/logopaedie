from django.contrib import admin
from .models import Patient, Therapy, Process_report, Therapy_report


class TherapyAdmin(admin.ModelAdmin):
    list_display = ('recipe_date', 'patients')

admin.site.register(Patient)
admin.site.register(Therapy, TherapyAdmin)
admin.site.register(Process_report)
admin.site.register(Therapy_report)
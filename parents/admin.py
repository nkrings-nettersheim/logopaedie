from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from parents.models import Parents_sheet

admin.site.register(Parents_sheet, SimpleHistoryAdmin)

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from parents.models import Parents_sheet


class ParentsSheetAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'child_last_name', 'child_first_name', 'sheet_created')


admin.site.register(Parents_sheet, ParentsSheetAdmin)

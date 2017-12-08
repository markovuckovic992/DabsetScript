# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from backend.models import ActionLogs

# Register your models here.
class ActionLogsAdmin(admin.ModelAdmin):
    list_display = ['lead__domain', 'field_thats_changed', 'old_value', 'new_value']
    search_fields = ['lead__domain', 'field_thats_changed', 'old_value', 'new_value']

admin.site.register(ActionLogs, ActionLogsAdmin)

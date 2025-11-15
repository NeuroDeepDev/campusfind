from django.contrib import admin
from audit.models import Audit


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('action', 'affected_table', 'affected_id', 'changed_by', 'created_at')
    list_filter = ('action', 'affected_table', 'created_at')
    search_fields = ('action', 'affected_table')
    readonly_fields = ('created_at',)

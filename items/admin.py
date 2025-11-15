from django.contrib import admin
from items.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'status', 'category', 'location', 'reported_by', 'reported_date')
    list_filter = ('status', 'item_type', 'category', 'location', 'reported_date')
    search_fields = ('name', 'description', 'category__name')
    readonly_fields = ('reported_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Item Info', {
            'fields': ('name', 'description', 'category', 'location', 'item_type')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Evidence', {
            'fields': ('evidence_file',)
        }),
        ('Reporter', {
            'fields': ('reported_by', 'reported_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

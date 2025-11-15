from django.contrib import admin
from claims.models import Claim


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimed_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item__name', 'claimed_by__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Claim Info', {
            'fields': ('item', 'claimed_by', 'claim_description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Evidence', {
            'fields': ('evidence_file',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

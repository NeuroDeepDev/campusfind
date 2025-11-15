from django.contrib import admin
from locations.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('building_name', 'building_code', 'created_at')
    search_fields = ('building_name', 'building_code')
    readonly_fields = ('created_at',)

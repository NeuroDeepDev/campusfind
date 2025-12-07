from django.contrib import admin
from .models import Student, Admin as AdminModel, Category, Location, Item, Report, Claim, Audit


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'dept', 'year', 'user')
    search_fields = ('name', 'email')


@admin.register(AdminModel)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'name', 'email', 'user')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_id', 'building', 'area')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'category', 'status', 'location')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'item', 'reporter', 'report_type', 'report_date')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_id', 'item', 'claimer', 'status', 'claim_date')
    list_filter = ('status',)


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('audit_id', 'op_type', 'op_by', 'op_date')

from django.contrib import admin
from users.models import Student, Admin


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'student_id', 'is_active', 'is_verified', 'created_at')
    list_filter = ('is_active', 'is_verified', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'student_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Info', {
            'fields': ('email', 'first_name', 'last_name', 'student_id', 'phone', 'profile_picture')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Info', {
            'fields': ('email', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

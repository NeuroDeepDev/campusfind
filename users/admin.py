from django.contrib import admin
from users.models import Student, Admin


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'student_id', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name', 'student_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Student Details', {
            'fields': ('student_id', 'phone', 'profile_picture')
        }),
        ('Status', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

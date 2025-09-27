from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import DriverDocument

User = get_user_model()

# Сначала отменяем регистрацию стандартной модели User, если она была зарегистрирована
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'is_phone_verified', 'is_staff')
    list_filter = ('role', 'is_phone_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone',
                'role', 'is_phone_verified', 'firebase_uid'
            )
        }),
        ('Местоположение', {
            'fields': ('current_latitude', 'current_longitude', 'last_location_update'),
            'classes': ('collapse',)
        }),
        ('Резюме', {
            'fields': ('position', 'experience', 'education', 'skills', 'photo'),
            'classes': ('collapse',)
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(DriverDocument)
class DriverDocumentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'document_type', 'number', 'issue_date', 'expiry_date', 'created_by')
    list_filter = ('document_type', 'issue_date', 'expiry_date')
    search_fields = ('driver__first_name', 'driver__last_name', 'number', 'issuing_authority')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('driver', 'document_type', 'number', 'file')
        }),
        ('Детали документа', {
            'fields': ('issue_date', 'expiry_date', 'issuing_authority', 'description')
        }),
        ('Системная информация', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если это создание нового объекта
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

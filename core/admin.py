from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Notification, Waybill

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'user', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'user__email')
    ordering = ('-created_at',)

@admin.register(Waybill)
class WaybillAdmin(admin.ModelAdmin):
    list_display = ('number_link', 'date', 'vehicle_link', 'driver_link', 
                   'departure_point', 'destination_point', 'cargo_weight', 
                   'created_at', 'print_button')
    list_filter = ('date', 'vehicle', 'driver', 'created_at')
    search_fields = ('number', 'departure_point', 'destination_point', 
                    'cargo_description', 'driver__username', 'driver__first_name', 
                    'driver__last_name', 'vehicle__number')
    ordering = ('-date', '-created_at')
    raw_id_fields = ('driver', 'vehicle', 'created_by')
    date_hierarchy = 'date'
    readonly_fields = ('number', 'created_at', 'updated_at', 'created_by')
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'date', 'vehicle', 'driver')
        }),
        ('Маршрут и груз', {
            'fields': ('departure_point', 'destination_point', 
                      'cargo_description', 'cargo_weight')
        }),
        ('Служебная информация', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если это новый объект
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        # Отправляем уведомления
        obj.notify_driver()
        obj.notify_created_by()
    
    def number_link(self, obj):
        url = reverse('admin:core_waybill_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.number)
    number_link.short_description = 'Номер КАТа'
    
    def vehicle_link(self, obj):
        url = reverse('admin:logistics_vehicle_change', args=[obj.vehicle.pk])
        return format_html('<a href="{}">{}</a>', url, obj.vehicle)
    vehicle_link.short_description = 'Транспорт'
    
    def driver_link(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.driver.pk])
        return format_html('<a href="{}">{}</a>', url, obj.driver)
    driver_link.short_description = 'Водитель'
    
    def print_button(self, obj):
        url = reverse('core:waybill-print', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" target="_blank">'
            '<i class="fas fa-print"></i> Печать</a>',
            url
        )
    print_button.short_description = 'Печать'
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Notification, Waybill, ChecklistTemplate, TripChecklist, ChecklistItem, ChecklistItemPhoto

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'user', 'read', 'created_at')
    list_filter = ('type', 'read', 'created_at')
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


@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_required', 'order', 'is_active')
    list_filter = ('category', 'is_required', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('category', 'order', 'title')
    list_editable = ('order', 'is_required', 'is_active')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'title', 'description')
        }),
        ('Настройки', {
            'fields': ('is_required', 'order', 'is_active')
        }),
    )


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 0
    readonly_fields = ('template', 'checked_by', 'checked_at')
    fields = ('template', 'is_checked', 'is_ok', 'notes', 'checked_by', 'checked_at', 'photo')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('template')


@admin.register(TripChecklist)
class TripChecklistAdmin(admin.ModelAdmin):
    list_display = ('trip', 'status', 'completion_percentage_display', 'is_fully_signed', 'created_at')
    list_filter = ('status', 'created_at', 'completed_at')
    search_fields = ('trip__title', 'trip__vehicle__number', 'trip__driver__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'completion_percentage')
    inlines = [ChecklistItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('trip', 'status', 'completion_percentage')
        }),
        ('Подписи водителя', {
            'fields': ('driver_signature', 'driver_signed_at')
        }),
        ('Подписи механика', {
            'fields': ('mechanic', 'mechanic_signature', 'mechanic_signed_at')
        }),
        ('Подписи зам директора', {
            'fields': ('deputy_director', 'deputy_director_signature', 'deputy_director_signed_at')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'completed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def completion_percentage_display(self, obj):
        percentage = obj.completion_percentage
        if percentage == 100:
            color = 'green'
        elif percentage >= 50:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} %</span>',
            color, percentage
        )
    completion_percentage_display.short_description = 'Прогресс'


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'template', 'is_checked', 'is_ok', 'checked_by', 'checked_at')
    list_filter = ('is_checked', 'is_ok', 'template__category', 'checked_at')
    search_fields = ('checklist__trip__title', 'template__title', 'notes')
    ordering = ('-checked_at',)
    readonly_fields = ('checked_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('checklist', 'template')
        }),
        ('Статус проверки', {
            'fields': ('is_checked', 'is_ok', 'notes', 'photo')
        }),
        ('Служебная информация', {
            'fields': ('checked_by', 'checked_at'),
            'classes': ('collapse',)
        }),
    )


class ChecklistItemPhotoInline(admin.TabularInline):
    model = ChecklistItemPhoto
    extra = 0
    readonly_fields = ('uploaded_by', 'uploaded_at')
    fields = ('image', 'description', 'uploaded_by', 'uploaded_at')


@admin.register(ChecklistItemPhoto)
class ChecklistItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('item', 'image_preview', 'description', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('item__checklist__trip__title', 'item__template__title', 'description')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at', 'image_preview')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('item', 'image', 'image_preview', 'description')
        }),
        ('Служебная информация', {
            'fields': ('uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Превью'

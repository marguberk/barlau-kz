from django.contrib import admin
from .models import Vehicle, VehiclePhoto, Task, TaskFile, Expense, WaybillDocument

class VehiclePhotoInline(admin.TabularInline):
    model = VehiclePhoto
    extra = 1
    fields = ('photo', 'description', 'is_main', 'uploaded_by')
    readonly_fields = ('uploaded_at',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'brand', 'model', 'year', 'driver', 'has_photos')
    list_filter = ('brand', 'year', 'status')
    search_fields = ('number', 'brand', 'model')
    raw_id_fields = ('driver', 'created_by')
    inlines = [VehiclePhotoInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('number', 'brand', 'model', 'year', 'color', 'description', 'vehicle_type', 'status')
        }),
        ('Технические характеристики', {
            'fields': ('vin_number', 'engine_number', 'chassis_number', 'engine_capacity', 'fuel_type', 'fuel_consumption')
        }),
        ('Габариты и масса', {
            'fields': ('length', 'width', 'height', 'max_weight', 'cargo_capacity')
        }),
        ('GPS мониторинг', {
            'fields': ('gps_device_id', 'gps_imei', 'gps_phone', 'gps_enabled', 'gps_latitude', 'gps_longitude'),
            'classes': ('collapse',)
        }),
        ('Связи', {
            'fields': ('driver', 'created_by')
        }),
    )
    
    def has_photos(self, obj):
        return obj.photos.exists() or bool(obj.photo)
    has_photos.boolean = True
    has_photos.short_description = 'Есть фото'

class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 0
    readonly_fields = ('uploaded_at', 'file_size', 'file_type')
    fields = ('file', 'original_name', 'uploaded_by', 'uploaded_at', 'file_size', 'file_type')

@admin.register(VehiclePhoto)
class VehiclePhotoAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'description', 'is_main', 'uploaded_by', 'uploaded_at')
    list_filter = ('is_main', 'uploaded_at', 'vehicle__brand')
    search_fields = ('vehicle__number', 'vehicle__brand', 'description')
    raw_id_fields = ('vehicle', 'uploaded_by')
    readonly_fields = ('uploaded_at',)
    date_hierarchy = 'uploaded_at'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'assigned_to', 'vehicle', 'due_date', 'created_by')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('assigned_to', 'vehicle', 'created_by')
    filter_horizontal = ('assignees',)
    date_hierarchy = 'created_at'
    inlines = [TaskFileInline]

@admin.register(TaskFile)
class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('task', 'original_name', 'file_type', 'file_size', 'uploaded_by', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('original_name', 'task__title')
    raw_id_fields = ('task', 'uploaded_by')
    readonly_fields = ('uploaded_at', 'file_size', 'file_type')
    date_hierarchy = 'uploaded_at'

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'vehicle', 'date', 'created_by')
    list_filter = ('category', 'date', 'vehicle')
    search_fields = ('description',)
    raw_id_fields = ('vehicle', 'created_by')
    date_hierarchy = 'date'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'ACCOUNTANT':
            return qs
        return qs.filter(created_by=request.user)

@admin.register(WaybillDocument)
class WaybillDocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'vehicle', 'driver', 'departure_point', 'destination_point')
    list_filter = ('date', 'vehicle', 'driver')
    search_fields = ('number', 'cargo_description')
    raw_id_fields = ('vehicle', 'driver', 'created_by')
    date_hierarchy = 'date'

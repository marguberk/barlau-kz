from rest_framework import serializers
from .models import Vehicle, Task, Expense, WaybillDocument, VehiclePhoto, VehicleDocument, VehicleMaintenance
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'phone']

class VehiclePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiclePhoto
        fields = '__all__'

class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDocument
        fields = '__all__'

class VehicleMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMaintenance
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    driver_details = UserSerializer(source='driver', read_only=True)
    photos = VehiclePhotoSerializer(many=True, read_only=True)
    documents = VehicleDocumentSerializer(many=True, read_only=True)
    maintenance_records = VehicleMaintenanceSerializer(many=True, read_only=True)
    main_photo_url = serializers.SerializerMethodField()

    def get_main_photo_url(self, obj):
        main = obj.photos.filter(is_main=True).first()
        if main and main.photo:
            return main.photo.url
        main = obj.photos.first()
        if main and main.photo:
            return main.photo.url
        return None
    
    class Meta:
        model = Vehicle
        fields = ['id', 'number', 'brand', 'model', 'year', 'color', 'description', 'vehicle_type', 'status', 
                 'vin_number', 'engine_number', 'chassis_number', 'engine_capacity', 'fuel_type', 'fuel_consumption',
                 'length', 'width', 'height', 'max_weight', 'cargo_capacity',
                 'driver', 'driver_details', 'created_at', 'updated_at', 'created_by',
                 'photos', 'documents', 'maintenance_records', 'main_photo_url']

class VehicleLocationSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)
    latitude = serializers.DecimalField(source='driver.current_latitude', max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(source='driver.current_longitude', max_digits=9, decimal_places=6)
    last_update = serializers.DateTimeField(source='driver.last_location_update')
    
    class Meta:
        model = Vehicle
        fields = ['id', 'number', 'brand', 'model', 'driver_name', 'latitude', 'longitude', 'last_update']

class TaskSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    assigned_user_details = UserSerializer(source='assigned_to', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class TaskLocationSerializer(serializers.ModelSerializer):
    vehicle_number = serializers.CharField(source='vehicle.number', read_only=True)
    driver_name = serializers.CharField(source='vehicle.driver.get_full_name', read_only=True)
    latitude = serializers.DecimalField(source='vehicle.driver.current_latitude', max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(source='vehicle.driver.current_longitude', max_digits=9, decimal_places=6)
    last_update = serializers.DateTimeField(source='vehicle.driver.last_location_update')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'vehicle_number', 'driver_name', 'latitude', 'longitude', 'last_update']

class ExpenseSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseReportSerializer(serializers.Serializer):
    category = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    count = serializers.IntegerField()

class WaybillDocumentSerializer(serializers.ModelSerializer):
    driver_details = UserSerializer(source='driver', read_only=True)
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = WaybillDocument
        fields = '__all__'

class FinancialReportSerializer(serializers.Serializer):
    period = serializers.DictField()
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    expenses_by_category = serializers.ListField()
    total_tasks = serializers.IntegerField()
    tasks_by_status = serializers.ListField()
    expenses_by_vehicle = serializers.ListField() 
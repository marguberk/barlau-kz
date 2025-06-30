from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import Notification, Waybill, Trip, DriverLocation, ChecklistTemplate, TripChecklist, ChecklistItem, ChecklistItemPhoto
from logistics.models import Vehicle

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 'last_name', 
            'role', 'role_display', 'is_active', 'is_archived', 'position', 'photo', 
            'date_joined', 'last_login', 'full_name',
            # Биографические поля
            'about_me', 'experience', 'education', 'key_skills', 'languages', 
            'hobbies', 'certifications', 'achievements', 'courses', 'publications',
            'recommendations', 'desired_salary', 'age', 'location', 'skype', 
            'linkedin', 'portfolio_url'
        ]
        read_only_fields = ['date_joined', 'last_login']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'email', 'phone',
            'first_name', 'last_name', 'role', 'position'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
            
        # Проверяем уникальность телефона
        phone = attrs.get('phone')
        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "Пользователь с таким номером телефона уже существует"})
            
        # Проверяем уникальность email
        email = attrs.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует"})
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({"detail": "Ошибка при создании пользователя. Возможно, такой пользователь уже существует."})

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'phone', 'first_name', 'last_name',
            'role', 'position', 'photo'
        ]
        
    def validate_phone(self, value):
        instance = getattr(self, 'instance', None)
        if instance and value and User.objects.exclude(pk=instance.pk).filter(phone=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует")
        return value
        
    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        if instance and value and User.objects.exclude(pk=instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

class VehicleSerializer(serializers.ModelSerializer):
    main_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ['id', 'number', 'brand', 'model', 'year', 'main_photo_url']

    def get_main_photo_url(self, obj):
        main_photo = obj.photos.filter(is_main=True).first() or obj.photos.first()
        if main_photo and main_photo.photo:
            return main_photo.photo.url
        return None

class NotificationSerializer(serializers.ModelSerializer):
    time_since = serializers.SerializerMethodField()
    created_at_display = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'link', 'read', 'created_at', 'time_since', 'created_at_display']

    def get_time_since(self, obj):
        if not obj.created_at:
            return ''
        else:
            return timesince(obj.created_at, now()) + " назад"

    def get_created_at_display(self, obj):
        if not obj.created_at:
            return ''
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

class WaybillSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    driver_details = UserSerializer(source='driver', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = Waybill
        fields = [
            'id', 'number', 'date', 'vehicle', 'vehicle_details',
            'driver', 'driver_details', 'departure_point', 'destination_point',
            'cargo_description', 'cargo_weight', 'created_at', 'updated_at',
            'created_by', 'created_by_details'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo']
        
    def validate_photo(self, value):
        if value:
            # Проверяем размер файла (максимум 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Размер файла не должен превышать 5MB")
            
            # Проверяем тип файла
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Поддерживаются только форматы: JPEG, PNG")
                
        return value 

class TripSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    trailer_details = VehicleSerializer(source='trailer', read_only=True)
    driver_details = UserSerializer(source='driver', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    current_location = serializers.ReadOnlyField()
    route_info = serializers.ReadOnlyField()
    vehicle_info = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    cargo_type_display = serializers.CharField(source='get_cargo_type_display', read_only=True)
    freight_payment_type_display = serializers.CharField(source='get_freight_payment_type_display', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'title', 'status', 'status_display',
            'vehicle', 'vehicle_details', 'trailer', 'trailer_details',
            'driver', 'driver_details', 'created_by', 'created_by_details',
            'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude',
            'start_address', 'end_address', 'route_info',
            'cargo_description', 'cargo_type', 'cargo_type_display', 'cargo_weight',
            'freight_amount', 'freight_payment_type', 'freight_payment_type_display',
            'planned_start_date', 'planned_end_date', 'actual_start_date', 'actual_end_date',
            'notes', 'date', 'created_at', 'updated_at',
            'current_location', 'vehicle_info'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class DriverLocationSerializer(serializers.ModelSerializer):
    driver_details = UserSerializer(source='driver', read_only=True)
    trip_details = TripSerializer(source='trip', read_only=True)

    class Meta:
        model = DriverLocation
        fields = [
            'id', 'driver', 'driver_details', 'latitude', 'longitude', 'timestamp', 'trip', 'trip_details'
        ]
        read_only_fields = ['timestamp']


class ChecklistTemplateSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = ChecklistTemplate
        fields = [
            'id', 'category', 'category_display', 'title', 'description',
            'is_required', 'order', 'is_active'
        ]


class ChecklistItemPhotoSerializer(serializers.ModelSerializer):
    uploaded_by_details = UserSerializer(source='uploaded_by', read_only=True)
    
    class Meta:
        model = ChecklistItemPhoto
        fields = [
            'id', 'image', 'description', 'uploaded_by', 'uploaded_by_details', 'uploaded_at'
        ]
        read_only_fields = ['uploaded_at']


class ChecklistItemSerializer(serializers.ModelSerializer):
    template_details = ChecklistTemplateSerializer(source='template', read_only=True)
    checked_by_details = UserSerializer(source='checked_by', read_only=True)
    photos = ChecklistItemPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = ChecklistItem
        fields = [
            'id', 'template', 'template_details', 'is_checked', 'is_ok', 
            'notes', 'checked_by', 'checked_by_details', 'checked_at', 'photos'
        ]
        read_only_fields = ['checked_at']

    def update(self, instance, validated_data):
        # Автоматически устанавливаем пользователя при проверке
        if validated_data.get('is_checked') and not instance.checked_by:
            validated_data['checked_by'] = self.context['request'].user
        return super().update(instance, validated_data)


class TripChecklistSerializer(serializers.ModelSerializer):
    trip_details = TripSerializer(source='trip', read_only=True)
    mechanic_details = UserSerializer(source='mechanic', read_only=True)
    deputy_director_details = UserSerializer(source='deputy_director', read_only=True)
    items = ChecklistItemSerializer(many=True, read_only=True)
    completion_percentage = serializers.ReadOnlyField()
    is_fully_signed = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = TripChecklist
        fields = [
            'id', 'trip', 'trip_details', 'status', 'status_display',
            'driver_signature', 'driver_signed_at', 
            'mechanic', 'mechanic_details', 'mechanic_signature', 'mechanic_signed_at',
            'deputy_director', 'deputy_director_details', 'deputy_director_signature', 'deputy_director_signed_at',
            'notes', 'created_at', 'updated_at', 'completed_at',
            'items', 'completion_percentage', 'is_fully_signed'
        ]
        read_only_fields = ['created_at', 'updated_at']


class TripChecklistCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания чек-листа с автоматическим заполнением пунктов"""
    
    class Meta:
        model = TripChecklist
        fields = ['trip', 'notes']
    
    def create(self, validated_data):
        # Создаем чек-лист
        checklist = super().create(validated_data)
        
        # Получаем все активные шаблоны
        templates = ChecklistTemplate.objects.filter(is_active=True).order_by('category', 'order')
        
        # Создаем пункты чек-листа на основе шаблонов
        checklist_items = []
        for template in templates:
            checklist_items.append(
                ChecklistItem(
                    checklist=checklist,
                    template=template
                )
            )
        
        # Массовое создание пунктов
        ChecklistItem.objects.bulk_create(checklist_items)
        
        return checklist 
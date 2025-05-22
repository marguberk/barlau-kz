from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import Notification, Waybill, Trip, DriverLocation
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
            'date_joined', 'last_login', 'full_name'
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
    class Meta:
        model = Vehicle
        fields = ['id', 'number', 'brand', 'model', 'year']

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
    driver_details = UserSerializer(source='driver', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'vehicle', 'vehicle_details', 'driver', 'driver_details',
            'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude',
            'cargo_description', 'date', 'created_at'
        ]
        read_only_fields = ['created_at']

class DriverLocationSerializer(serializers.ModelSerializer):
    driver_details = UserSerializer(source='driver', read_only=True)
    trip_details = TripSerializer(source='trip', read_only=True)

    class Meta:
        model = DriverLocation
        fields = [
            'id', 'driver', 'driver_details', 'latitude', 'longitude', 'timestamp', 'trip', 'trip_details'
        ]
        read_only_fields = ['timestamp'] 
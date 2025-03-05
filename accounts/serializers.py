from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone', 'first_name', 'last_name',
            'role', 'is_phone_verified', 'current_latitude', 'current_longitude',
            'last_location_update', 'position', 'experience', 'education',
            'skills', 'photo'
        )
        read_only_fields = ('is_phone_verified', 'firebase_uid')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'phone',
            'first_name', 'last_name', 'role'
        )

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
        fields = (
            'email', 'phone', 'first_name', 'last_name', 'position',
            'experience', 'education', 'skills', 'photo'
        )
        
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

class DriverLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('current_latitude', 'current_longitude', 'last_location_update')

class UserResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'position', 'experience',
            'education', 'skills', 'photo'
        ) 
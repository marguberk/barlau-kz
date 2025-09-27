from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import DriverDocument

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone', 'first_name', 'last_name',
            'role', 'role_display', 'is_active', 'is_archived', 'date_joined', 'is_phone_verified', 
            'current_latitude', 'current_longitude', 'last_location_update', 
            'position', 'experience', 'education', 'skills', 'photo',
            'desired_salary', 'age', 'location', 'skype', 'linkedin', 'portfolio_url',
            'about_me', 'key_skills', 'achievements', 'courses', 'publications',
            'recommendations', 'hobbies', 'certifications', 'languages', 'recommendation_file'
        )
        read_only_fields = ('is_phone_verified', 'firebase_uid', 'date_joined')

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

import base64
import io
import uuid
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

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
    
    def update(self, instance, validated_data):
        # Обработка удаления фото
        photo_data = validated_data.get('photo')
        if photo_data == 'null':
            # Если передано 'null', удаляем фото
            validated_data['photo'] = None
            if instance.photo:
                instance.photo.delete(save=False)
        
        return super().update(instance, validated_data)

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


class DriverDocumentSerializer(serializers.ModelSerializer):
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DriverDocument
        fields = (
            'id', 'driver', 'driver_name', 'document_type', 'document_type_display',
            'number', 'issue_date', 'expiry_date', 'issuing_authority', 'description',
            'file', 'file_url', 'created_at', 'updated_at', 'created_by'
        )
        read_only_fields = ('created_at', 'updated_at', 'created_by')
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data) 
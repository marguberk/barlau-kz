from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    DriverLocationUpdateSerializer, UserResumeSerializer
)
from django.utils import timezone

User = get_user_model()

class IsUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'update_location':
            return DriverLocationUpdateSerializer
        elif self.action == 'resume':
            return UserResumeSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsUserOrAdmin()]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        return queryset
    
    @action(detail=True, methods=['patch'])
    def update_location(self, request, pk=None):
        user = self.get_object()
        if user.role != User.Role.DRIVER:
            return Response(
                {"error": "Только водители могут обновлять местоположение"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(last_location_update=timezone.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def resume(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            print(f'Django: Обновление профиля пользователя {request.user.username}')
            print(f'Django: Полученные данные: {request.data}')
            
            # Обрабатываем base64 фото отдельно
            photo_data = request.data.get('photo')
            if photo_data and isinstance(photo_data, str) and photo_data.startswith('data:image'):
                try:
                    import base64
                    import io
                    import uuid
                    from django.core.files.uploadedfile import InMemoryUploadedFile
                    
                    # Убираем префикс data:image/...;base64,
                    format, imgstr = photo_data.split(';base64,')
                    ext = format.split('/')[-1]
                    
                    # Декодируем base64
                    image_data = base64.b64decode(imgstr)
                    
                    # Создаем InMemoryUploadedFile
                    photo_file = InMemoryUploadedFile(
                        file=io.BytesIO(image_data),
                        field_name='photo',
                        name=f'profile_photo_{uuid.uuid4().hex[:8]}.{ext}',
                        content_type=f'image/{ext}',
                        size=len(image_data),
                        charset=None
                    )
                    
                    # Создаем копию данных без base64 фото
                    data_without_photo = request.data.copy()
                    data_without_photo['photo'] = photo_file
                    
                    serializer = UserUpdateSerializer(request.user, data=data_without_photo, partial=True)
                except Exception as e:
                    print(f'Django: Ошибка обработки base64 фото: {e}')
                    # Если не удалось обработать фото, обновляем без него
                    data_without_photo = request.data.copy()
                    data_without_photo.pop('photo', None)
                    serializer = UserUpdateSerializer(request.user, data=data_without_photo, partial=True)
            else:
                serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
            
            if serializer.is_valid():
                try:
                    serializer.save()
                    print(f'Django: Профиль успешно обновлен')
                    return Response(serializer.data)
                except Exception as e:
                    print(f'Django: Ошибка сохранения профиля: {e}')
                    return Response(
                        {'error': f'Ошибка сохранения: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                print(f'Django: Ошибки валидации: {serializer.errors}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

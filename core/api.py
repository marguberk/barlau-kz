from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.db import transaction, models
from .serializers import (
    UserUpdateSerializer, UserPhotoSerializer, TripSerializer, DriverLocationSerializer,
    ChecklistTemplateSerializer, TripChecklistSerializer, TripChecklistCreateSerializer, ChecklistItemSerializer
)
from .models import Notification, Waybill, Trip, DriverLocation, ChecklistTemplate, TripChecklist, ChecklistItem, ChecklistItemPhoto
from logistics.models import Task, Expense, Vehicle, VehiclePhoto
from rest_framework import status
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from accounts.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import serializers

User = get_user_model()

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Обновление профиля текущего пользователя"""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_photo(request):
    """Загрузка фото профиля"""
    serializer = UserPhotoSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_stats(request):
    """Получение статистики для профиля пользователя"""
    user = request.user
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Базовая статистика
    stats = {
        'tasks': {
            'total': Task.objects.filter(assigned_to=user).count(),
            'new': Task.objects.filter(assigned_to=user, status='NEW').count(),
            'in_progress': Task.objects.filter(assigned_to=user, status='IN_PROGRESS').count(),
            'completed': Task.objects.filter(assigned_to=user, status='COMPLETED').count()
        },
        'notifications': {
            'total': Notification.objects.filter(user=user).count(),
            'unread': Notification.objects.filter(user=user, read=False).count(),
            'today': Notification.objects.filter(
                user=user,
                created_at__gte=today
            ).count()
        }
    }
    
    # Статистика для водителей
    if user.role == 'DRIVER':
        stats['waybills'] = {
            'total': Waybill.objects.filter(driver=user).count(),
            'today': Waybill.objects.filter(driver=user, date=today).count(),
            'week': Waybill.objects.filter(driver=user, date__gte=week_ago).count(),
            'month': Waybill.objects.filter(driver=user, date__gte=month_ago).count()
        }
    
    # Статистика для бухгалтеров и снабженцев
    if user.role in ['ACCOUNTANT', 'SUPPLIER']:
        stats['expenses'] = {
            'total': Expense.objects.filter(created_by=user).count(),
            'pending': Expense.objects.filter(created_by=user, status='PENDING').count(),
            'approved': Expense.objects.filter(created_by=user, status='APPROVED').count(),
            'rejected': Expense.objects.filter(created_by=user, status='REJECTED').count()
        }
    
    return Response(stats) 

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def trips_api(request, pk=None):
    """Получить список поездок, создать новую или удалить"""
    user = request.user
    print(f"[DEBUG] trips_api called by user: {user.username} (role: {user.role})")
    print(f"[DEBUG] User authenticated: {user.is_authenticated}")
    print(f"[DEBUG] User is_superuser: {user.is_superuser}")
    print(f"[DEBUG] Request method: {request.method}")
    
    if request.method == 'GET':
        if user.role in ['SUPERADMIN', 'DIRECTOR', 'ADMIN'] or user.is_superuser:
            trips = Trip.objects.all().order_by('-date')
        else:
            trips = Trip.objects.filter(driver=user).order_by('-date')
        
        print(f"[DEBUG] Found {trips.count()} trips for user {user.username}")
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Проверяем права на создание поездок
        if not (user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response({'detail': 'У вас нет прав для создания поездок'}, status=status.HTTP_403_FORBIDDEN)
        
        # Убираем флаг создания чек-листа из данных запроса
        request_data = request.data.copy()
        requires_checklist = request_data.pop('create_checklist', True)  # По умолчанию требуется чек-лист
        
        # Отладочная информация
        print(f"[DEBUG] Create trip request data: {request.data}")
        print(f"[DEBUG] Requires checklist: {requires_checklist}")
        print(f"[DEBUG] Type of requires_checklist: {type(requires_checklist)}")
        
        serializer = TripSerializer(data=request_data)
        if serializer.is_valid():
            trip = serializer.save()
            
            # Устанавливаем статус в зависимости от необходимости чек-листа
            if requires_checklist:
                trip.requires_checklist = True
                trip.status = 'PENDING_CHECKLIST'
                trip.save()
                
                # Создаем уведомление водителю о необходимости заполнить чек-лист
                from .models import Notification
                Notification.create_system_notification(
                    user=trip.driver,
                    title="Требуется заполнить чек-лист",
                    message=f"Для поездки '{trip.title}' необходимо заполнить чек-лист перед началом движения.",
                    link=f"/dashboard/checklist/create/{trip.id}/"
                )
                
                # Уведомляем диспетчеров и админов
                from accounts.models import User
                dispatchers_and_admins = User.objects.filter(
                    role__in=['ADMIN', 'SUPERADMIN', 'DISPATCHER'],
                    is_active=True
                ).exclude(id=trip.driver.id)
                
                for admin_user in dispatchers_and_admins:
                    Notification.create_system_notification(
                        user=admin_user,
                        title="Новая поездка ожидает чек-лист",
                        message=f"Поездка '{trip.title}' создана и ожидает заполнения чек-листа водителем {trip.driver.get_full_name()}.",
                        link=f"/dashboard/trips/{trip.id}/"
                    )
            else:
                trip.requires_checklist = False
                trip.status = 'READY'
                trip.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        # Ожидаем trips_api(request, pk=...)
        trip_id = pk or request.GET.get('id') or request.data.get('id')
        if not trip_id:
            return Response({'detail': 'Не указан id поездки'}, status=400)
        try:
            trip = Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:
            return Response({'detail': 'Поездка не найдена'}, status=404)
        # Только админ или водитель своей поездки
        if not (user.is_superuser or user.role in ['SUPERADMIN', 'ADMIN'] or trip.driver == user):
            return Response({'detail': 'Нет прав на удаление'}, status=403)
        trip.delete()
        return Response({'detail': 'Поездка удалена'})

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, CsrfExemptSessionAuthentication])
@permission_classes([IsAuthenticated])
def driver_locations_api(request):
    """Получить историю геолокаций или отправить новую точку (оптимизированная версия)"""
    user = request.user
    
    if request.method == 'GET':
        # Временно отключаем кеширование для избежания ошибок
        # cache_key = f'driver_locations_{user.id}_{user.role}'
        # cached_data = cache.get(cache_key)
        
        # if cached_data is not None:
        #     return Response(cached_data)
        
        # Оптимизированный запрос с select_related для уменьшения количества SQL запросов
        if user.role in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'DISPATCHER'] or user.is_superuser:
            # Для админов, директоров и диспетчеров - показываем только последние локации каждого водителя (последние 30 минут)
            thirty_minutes_ago = timezone.now() - timedelta(minutes=30)
            all_locations = DriverLocation.objects.select_related('driver').filter(
                timestamp__gte=thirty_minutes_ago
            ).order_by('driver_id', '-timestamp')
            
            # Группируем по водителю и берем последнюю локацию для каждого (совместимо с SQLite)
            driver_latest = {}
            for location in all_locations:
                if location.driver_id not in driver_latest:
                    driver_latest[location.driver_id] = location
            
            locations = list(driver_latest.values())[:20]
        else:
            # Для водителей - только их собственные локации за последний час
            one_hour_ago = timezone.now() - timedelta(hours=1)
            locations = DriverLocation.objects.select_related('driver').filter(
                driver=user,
                timestamp__gte=one_hour_ago
            ).order_by('-timestamp')[:10]
        
        serializer = DriverLocationSerializer(locations, many=True)
        
        # Кэшируем на 2 секунды (временно отключено)
        # cache.set(cache_key, serializer.data, 2)
        
        return Response(serializer.data)
        
    elif request.method == 'POST':
        # Проверяем, что пользователь - водитель
        if user.role != 'DRIVER':
            return Response({
                'detail': f'Только водители могут отправлять локации. Ваша роль: {user.role}'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Оптимизированное создание локации
        data = request.data.copy()
        data['driver'] = user.id
        
        print(f"[DEBUG] Creating location for driver {user.username} (ID: {user.id})")
        print(f"[DEBUG] Location data: {data}")
        
        # Используем транзакцию для быстрой записи
        with transaction.atomic():
            serializer = DriverLocationSerializer(data=data)
            if serializer.is_valid():
                location = serializer.save()
                print(f"[DEBUG] Location saved successfully: {location.id}")
                # Очищаем кэш для мгновенного обновления (временно отключено)
                # cache.clear()  # Очищаем весь кэш для простоты
                # Возвращаем созданную локацию с данными водителя
                response_serializer = DriverLocationSerializer(location)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"[DEBUG] Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def employee_pdf_api(request, pk):
    """API endpoint для скачивания PDF резюме сотрудника (с авторизацией)"""
    try:
        # Получаем сотрудника
        employee = get_object_or_404(User, pk=pk)
        
        # Проверяем права доступа
        if not (request.user.role in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'MANAGER'] or 
                request.user.is_superuser or 
                request.user.id == employee.id):
            return Response({
                'detail': 'У вас нет прав для просмотра этого резюме'
            }, status=status.HTTP_403_FORBIDDEN)

        # Подготавливаем контекст
        context = {
            'employee': employee,
            'company_name': getattr(settings, 'COMPANY_NAME', 'BARLAU.KZ'),
            'company_address': getattr(settings, 'COMPANY_ADDRESS', 'г. Алматы'),
            'company_phone': getattr(settings, 'COMPANY_PHONE', '+7 777 123 4567'),
            'company_email': getattr(settings, 'COMPANY_EMAIL', 'info@barlau.kz'),
            'STATIC_URL': request.build_absolute_uri(settings.STATIC_URL),
            'MEDIA_URL': request.build_absolute_uri(settings.MEDIA_URL),
        }

        # Рендерим HTML
        template = get_template('core/employee_pdf.html')
        html_string = template.render(context)

        # Создаем PDF ответ
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{employee.get_full_name()}_resume.pdf"'

        try:
            # Попробуем импортировать weasyprint
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            # Конфигурация шрифтов
            font_config = FontConfiguration()

            # Создаем HTML объект
            html = HTML(
                string=html_string,
                base_url=request.build_absolute_uri('/'),
            )

            # Генерируем PDF
            html.write_pdf(
                response,
                font_config=font_config,
                presentational_hints=True,
                optimize_size=('fonts', 'images'),
            )

        except ImportError:
            # Если weasyprint не установлен, возвращаем HTML
            response = HttpResponse(html_string, content_type='text/html')
            response['Content-Disposition'] = f'inline; filename="{employee.get_full_name()}_resume.html"'

        return response

    except Exception as e:
        return Response({
            'detail': f'Ошибка при генерации PDF: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def employee_pdf_public(request, pk):
    """Публичный API endpoint для скачивания PDF резюме сотрудника (без авторизации)"""
    try:
        # Получаем сотрудника
        employee = get_object_or_404(User, pk=pk)

        # Подготавливаем контекст
        context = {
            'employee': employee,
            'company_name': getattr(settings, 'COMPANY_NAME', 'BARLAU.KZ'),
            'company_address': getattr(settings, 'COMPANY_ADDRESS', 'г. Алматы'),
            'company_phone': getattr(settings, 'COMPANY_PHONE', '+7 777 123 4567'),
            'company_email': getattr(settings, 'COMPANY_EMAIL', 'info@barlau.kz'),
            'STATIC_URL': request.build_absolute_uri(settings.STATIC_URL),
            'MEDIA_URL': request.build_absolute_uri(settings.MEDIA_URL),
        }

        # Рендерим HTML
        template = get_template('core/employee_pdf.html')
        html_string = template.render(context)

        # Создаем PDF ответ
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{employee.get_full_name()}_resume.pdf"'

        try:
            # Попробуем импортировать weasyprint
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            # Конфигурация шрифтов
            font_config = FontConfiguration()

            # Создаем HTML объект
            html = HTML(
                string=html_string,
                base_url=request.build_absolute_uri('/'),
            )

            # Генерируем PDF
            html.write_pdf(
                response,
                font_config=font_config,
                presentational_hints=True,
                optimize_size=('fonts', 'images'),
            )

        except ImportError:
            # Если weasyprint не установлен, возвращаем HTML
            response = HttpResponse(html_string, content_type='text/html')
            response['Content-Disposition'] = f'inline; filename="{employee.get_full_name()}_resume.html"'

        return response

    except Exception as e:
        return Response({
            'detail': f'Ошибка при генерации PDF: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vehicles_api(request):
    """API для получения списка грузовиков"""
    try:
        # Временно отключаем проверку прав для тестирования
        # if not (request.user.role in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'MANAGER', 'DISPATCHER'] or 
        #         request.user.is_superuser):
        #     return Response({
        #         'detail': 'У вас нет прав для просмотра списка грузовиков'
        #     }, status=status.HTTP_403_FORBIDDEN)

        # Получаем все активные грузовики
        vehicles = Vehicle.objects.filter(is_archived=False).select_related('driver').prefetch_related('photos')
        
        vehicles_data = []
        for vehicle in vehicles:
            # Получаем основное фото
            main_photo = vehicle.photos.filter(is_main=True).first()
            if not main_photo:
                main_photo = vehicle.photos.first()
            
            # Определяем статус
            status_display = vehicle.get_status_display()
            status_color = {
                'ACTIVE': '#10B981',      # зеленый
                'INACTIVE': '#6B7280',    # серый
                'MAINTENANCE': '#F59E0B'  # оранжевый
            }.get(vehicle.status, '#6B7280')
            
            vehicle_data = {
                'id': vehicle.id,
                'number': vehicle.number,
                'brand': vehicle.brand,
                'model': vehicle.model,
                'year': vehicle.year,
                'color': vehicle.color,
                'vehicle_type': vehicle.vehicle_type,
                'vehicle_type_display': vehicle.get_vehicle_type_display(),
                'status': vehicle.status,
                'status_display': status_display,
                'status_color': status_color,
                'driver': {
                    'id': vehicle.driver.id,
                    'name': vehicle.driver.get_full_name(),
                    'phone': vehicle.driver.phone,
                    'photo': request.build_absolute_uri(vehicle.driver.photo.url) if vehicle.driver and vehicle.driver.photo else None
                } if vehicle.driver else None,
                'photo': request.build_absolute_uri(main_photo.photo.url) if main_photo else None,
                'fuel_type': vehicle.fuel_type,
                'fuel_type_display': vehicle.get_fuel_type_display() if vehicle.fuel_type else None,
                'fuel_consumption': float(vehicle.fuel_consumption) if vehicle.fuel_consumption else None,
                'cargo_capacity': float(vehicle.cargo_capacity) if vehicle.cargo_capacity else None,
                'max_weight': float(vehicle.max_weight) if vehicle.max_weight else None,
                'description': vehicle.description,
                # Дополнительные технические характеристики
                'vin_number': vehicle.vin_number,
                'engine_number': vehicle.engine_number,
                'chassis_number': vehicle.chassis_number,
                'engine_capacity': float(vehicle.engine_capacity) if vehicle.engine_capacity else None,
                'length': float(vehicle.length) if vehicle.length else None,
                'width': float(vehicle.width) if vehicle.width else None,
                'height': float(vehicle.height) if vehicle.height else None,
                'created_at': vehicle.created_at.isoformat(),
                'updated_at': vehicle.updated_at.isoformat(),
            }
            vehicles_data.append(vehicle_data)
        
        return Response({
            'vehicles': vehicles_data,
            'count': len(vehicles_data)
        })

    except Exception as e:
        return Response({
            'detail': f'Ошибка при получении списка грузовиков: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class TripViewSet(viewsets.ModelViewSet):
    """ViewSet для управления поездками"""
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'driver', 'vehicle', 'cargo_type', 'freight_payment_type']
    search_fields = ['title', 'start_address', 'end_address', 'cargo_description', 'notes']
    ordering_fields = ['planned_start_date', 'created_at', 'updated_at']
    ordering = ['-planned_start_date']

    def get_queryset(self):
        """Получить список поездок в зависимости от роли пользователя"""
        user = self.request.user
        queryset = Trip.objects.select_related(
            'vehicle', 'trailer', 'driver', 'created_by'
        ).prefetch_related(
            'vehicle__photos', 'trailer__photos'
        )
        
        if user.role in ['SUPERADMIN', 'DIRECTOR', 'ADMIN', 'DISPATCHER'] or user.is_superuser:
            return queryset
        elif user.role == 'DRIVER':
            return queryset.filter(driver=user)
        else:
            # Для других ролей показываем только активные поездки
            return queryset.filter(status='ACTIVE')

    def perform_create(self, serializer):
        """Создание поездки с автоматическим назначением создателя"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def start_trip(self, request, pk=None):
        """Начать поездку (с проверкой чек-листа если требуется)"""
        trip = self.get_object()
        user = request.user
        
        # Проверяем права (водитель может начать только свою поездку)
        if not (user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser or trip.driver == user):
            return Response(
                {'detail': 'У вас нет прав для начала этой поездки'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем текущий статус поездки
        if trip.status == 'ACTIVE':
            return Response(
                {'detail': 'Поездка уже активна'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if trip.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {'detail': f'Нельзя начать поездку со статусом "{trip.get_status_display()}"'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Если поездка требует чек-лист, проверяем его наличие и статус
        if trip.requires_checklist:
            if trip.status == 'PENDING_CHECKLIST':
                return Response(
                    {'detail': 'Сначала необходимо создать и заполнить чек-лист для этой поездки'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверяем наличие чек-листа
            if not hasattr(trip, 'checklist'):
                return Response(
                    {'detail': 'Для этой поездки не создан чек-лист'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверяем статус чек-листа
            if trip.checklist.status not in ['COMPLETED', 'APPROVED']:
                return Response(
                    {'detail': f'Чек-лист должен быть завершен перед началом поездки. Текущий статус: {trip.checklist.get_status_display()}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверяем, что все подписи собраны
            if not trip.checklist.is_fully_signed:
                return Response(
                    {'detail': 'Чек-лист должен быть подписан всеми ответственными лицами'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Начинаем поездку
        trip.status = 'ACTIVE'
        trip.actual_start_date = timezone.now()
        trip.save()
        
        # Отправляем уведомления
        from .models import Notification
        from accounts.models import User
        
        # Уведомляем водителя
        if trip.driver != user:
            Notification.create_system_notification(
                user=trip.driver,
                title="Поездка начата",
                message=f"Поездка '{trip.title}' была начата.",
                link=f"/dashboard/trips/{trip.id}/"
            )
        
        # Уведомляем админов и диспетчеров
        admins_and_dispatchers = User.objects.filter(
            role__in=['ADMIN', 'SUPERADMIN', 'DISPATCHER'],
            is_active=True
        ).exclude(id=user.id)
        
        for admin_user in admins_and_dispatchers:
            Notification.create_system_notification(
                user=admin_user,
                title="Поездка начата",
                message=f"Поездка '{trip.title}' начата водителем {trip.driver.get_full_name()}.",
                link=f"/dashboard/trips/{trip.id}/"
            )
        
        serializer = self.get_serializer(trip)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete_trip(self, request, pk=None):
        """Завершить поездку"""
        trip = self.get_object()
        user = request.user
        
        # Проверяем права
        if not (user == trip.driver or user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'У вас нет прав для завершения этой поездки'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if trip.status != 'ACTIVE':
            return Response(
                {'detail': 'Поездка не активна'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.status = 'COMPLETED'
        trip.actual_end_date = timezone.now()
        trip.save()
        
        serializer = self.get_serializer(trip)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel_trip(self, request, pk=None):
        """Отменить поездку"""
        trip = self.get_object()
        user = request.user
        
        # Проверяем права (только админ может отменять поездки)
        if not (user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'У вас нет прав для отмены поездки'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if trip.status == 'COMPLETED':
            return Response(
                {'detail': 'Нельзя отменить завершенную поездку'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.status = 'CANCELLED'
        trip.save()
        
        serializer = self.get_serializer(trip)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Получить список активных поездок (включая запланированные и в процессе)"""
        active_trips = self.get_queryset().filter(status__in=['ACTIVE', 'PLANNED', 'PENDING_CHECKLIST', 'READY', 'IN_PROGRESS'])
        serializer = self.get_serializer(active_trips, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_trips(self, request):
        """Получить поездки текущего пользователя"""
        user = request.user
        if user.role != 'DRIVER':
            return Response(
                {'detail': 'Только водители могут просматривать свои поездки'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        my_trips = Trip.objects.filter(driver=user).select_related(
            'vehicle', 'trailer', 'created_by'
        ).prefetch_related('vehicle__photos', 'trailer__photos')
        
        serializer = self.get_serializer(my_trips, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_checklist(self, request, pk=None):
        """Отправить чек-лист поездки на проверку"""
        trip = self.get_object()
        user = request.user
        
        # Проверяем права доступа
        if not (user == trip.driver or user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'У вас нет прав для отправки чек-листа этой поездки'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем наличие чек-листа
        try:
            checklist = trip.checklist
        except TripChecklist.DoesNotExist:
            return Response(
                {'detail': 'Чек-лист для этой поездки не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Проверяем, что все пункты заполнены
        if checklist.completion_percentage < 100:
            return Response(
                {'detail': f'Чек-лист заполнен только на {checklist.completion_percentage}%. Необходимо заполнить все пункты.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Переводим в статус "Завершен"
        checklist.status = 'COMPLETED'
        checklist.completed_at = timezone.now()
        checklist.driver_signature = f"{user.first_name} {user.last_name}"
        checklist.driver_signed_at = timezone.now()
        checklist.save()
        
        # Создаем уведомления для диспетчеров и админов
        from accounts.models import User
        dispatchers_and_admins = User.objects.filter(
            role__in=['ADMIN', 'SUPERADMIN', 'DISPATCHER', 'DIRECTOR'],
            is_active=True
        )
        
        for admin_user in dispatchers_and_admins:
            Notification.create_system_notification(
                user=admin_user,
                title="Чек-лист готов к проверке",
                message=f"Водитель {user.get_full_name()} завершил заполнение чек-листа для поездки '{trip.title}'. Требуется проверка и одобрение.",
                link=f"/dashboard/checklist/{checklist.id}/"
            )
        
        return Response({
            'detail': 'Чек-лист отправлен на проверку',
            'checklist_status': checklist.status
        })

    @action(detail=True, methods=['post'])
    def approve_checklist(self, request, pk=None):
        """Одобрить чек-лист поездки"""
        trip = self.get_object()
        user = request.user
        
        # Проверяем права доступа
        if not (user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER', 'DIRECTOR'] or user.is_superuser):
            return Response(
                {'detail': 'У вас нет прав для одобрения чек-листов'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем наличие чек-листа
        try:
            checklist = trip.checklist
        except TripChecklist.DoesNotExist:
            return Response(
                {'detail': 'Чек-лист для этой поездки не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Проверяем статус чек-листа
        if checklist.status != 'COMPLETED':
            return Response(
                {'detail': 'Можно одобрить только завершенный чек-лист'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Одобряем чек-лист
        checklist.status = 'APPROVED'
        checklist.deputy_director = user
        checklist.deputy_director_signature = f"{user.first_name} {user.last_name}"
        checklist.deputy_director_signed_at = timezone.now()
        checklist.save()
        
        # Обновляем статус поездки
        trip.status = 'READY'
        trip.save()
        
        # Создаем уведомление водителю
        Notification.create_system_notification(
            user=trip.driver,
            title="Чек-лист одобрен",
            message=f"Ваш чек-лист для поездки '{trip.title}' одобрен. Поездка готова к отправке!",
            link=f"/dashboard/trips/{trip.id}/"
        )
        
        return Response({
            'detail': 'Чек-лист одобрен',
            'trip_status': trip.status,
            'checklist_status': checklist.status
        })


class ChecklistTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра шаблонов чек-листа"""
    queryset = ChecklistTemplate.objects.filter(is_active=True).order_by('category', 'order')
    serializer_class = ChecklistTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_required']


class TripChecklistViewSet(viewsets.ModelViewSet):
    """ViewSet для управления чек-листами поездок"""
    serializer_class = TripChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'trip__driver', 'trip__vehicle']
    search_fields = ['trip__title', 'trip__vehicle__number', 'notes']
    ordering_fields = ['created_at', 'updated_at', 'completed_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Получить чек-листы в зависимости от роли пользователя"""
        user = self.request.user
        queryset = TripChecklist.objects.select_related(
            'trip', 'trip__vehicle', 'trip__driver', 'mechanic', 'deputy_director'
        ).prefetch_related('items__template')
        
        if user.role in ['SUPERADMIN', 'DIRECTOR', 'ADMIN', 'DISPATCHER'] or user.is_superuser:
            return queryset
        elif user.role == 'DRIVER':
            return queryset.filter(trip__driver=user)
        elif user.role == 'MECHANIC':
            # Механики видят чек-листы, где они назначены или все активные
            return queryset.filter(
                models.Q(mechanic=user) | models.Q(status__in=['PENDING', 'IN_PROGRESS'])
            )
        else:
            # Другие роли видят только завершенные чек-листы
            return queryset.filter(status__in=['COMPLETED', 'APPROVED'])

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return TripChecklistCreateSerializer
        return TripChecklistSerializer

    def perform_create(self, serializer):
        """Создание чек-листа с автоматическим заполнением пунктов"""
        # Проверяем права на создание
        user = self.request.user
        if not (user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER'] or user.is_superuser):
            raise permissions.PermissionDenied('У вас нет прав для создания чек-листов')
        
        # Проверяем, что для этой поездки еще нет чек-листа
        trip = serializer.validated_data['trip']
        if TripChecklist.objects.filter(trip=trip).exists():
            raise serializers.ValidationError('Для этой поездки уже существует чек-лист')
        
        serializer.save()

    @action(detail=True, methods=['post'])
    def sign_driver(self, request, pk=None):
        """Подпись водителя"""
        checklist = self.get_object()
        user = request.user
        
        # Проверяем, что пользователь - водитель этой поездки
        if user != checklist.trip.driver:
            return Response(
                {'detail': 'Только водитель может подписать чек-лист'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        signature = request.data.get('signature', user.get_full_name())
        checklist.driver_signature = signature
        checklist.driver_signed_at = timezone.now()
        checklist.save()
        
        serializer = self.get_serializer(checklist)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def sign_mechanic(self, request, pk=None):
        """Подпись механика"""
        checklist = self.get_object()
        user = request.user
        
        # Проверяем права (механик или админ)
        if not (user.role in ['MECHANIC', 'SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'Только механик может подписать чек-лист'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        signature = request.data.get('signature', user.get_full_name())
        checklist.mechanic = user
        checklist.mechanic_signature = signature
        checklist.mechanic_signed_at = timezone.now()
        checklist.save()
        
        serializer = self.get_serializer(checklist)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def sign_deputy_director(self, request, pk=None):
        """Подпись заместителя директора"""
        checklist = self.get_object()
        user = request.user
        
        # Проверяем права (зам директор или админ)
        if not (user.role in ['DEPUTY_DIRECTOR', 'DIRECTOR', 'SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'Только заместитель директора может подписать чек-лист'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        signature = request.data.get('signature', user.get_full_name())
        checklist.deputy_director = user
        checklist.deputy_director_signature = signature
        checklist.deputy_director_signed_at = timezone.now()
        
        # Если все подписи собраны, помечаем как завершенный
        if checklist.is_fully_signed:
            checklist.status = 'COMPLETED'
            checklist.completed_at = timezone.now()
        
        checklist.save()
        
        serializer = self.get_serializer(checklist)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Отправить чек-лист на проверку (водитель завершил заполнение)"""
        checklist = self.get_object()
        user = request.user
        
        # Проверяем права доступа - только водитель этой поездки
        if checklist.trip.driver != user and not (user.role in ['SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'У вас нет прав для отправки этого чек-листа'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем, что все пункты заполнены
        if checklist.completion_percentage < 100:
            return Response(
                {'detail': f'Чек-лист заполнен только на {checklist.completion_percentage}%. Необходимо заполнить все пункты.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Переводим в статус "Завершен"
        checklist.status = 'COMPLETED'
        checklist.completed_at = timezone.now()
        checklist.driver_signature = f"{user.first_name} {user.last_name}"
        checklist.driver_signed_at = timezone.now()
        checklist.save()
        
        # Создаем уведомления для диспетчеров и админов
        from accounts.models import User
        dispatchers_and_admins = User.objects.filter(
            role__in=['ADMIN', 'SUPERADMIN', 'DISPATCHER', 'DIRECTOR'],
            is_active=True
        )
        
        for admin_user in dispatchers_and_admins:
            Notification.create_system_notification(
                user=admin_user,
                title="Чек-лист готов к проверке",
                message=f"Водитель {user.get_full_name()} завершил заполнение чек-листа для поездки '{checklist.trip.title}'. Требуется проверка и одобрение.",
                link=f"/dashboard/checklist/?trip={checklist.trip.id}"
            )
        
        serializer = self.get_serializer(checklist)
        return Response({
            'detail': 'Чек-лист отправлен на проверку',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Утверждение чек-листа"""
        checklist = self.get_object()
        user = request.user
        
        # Проверяем права (только директор или админ)
        if not (user.role in ['DIRECTOR', 'SUPERADMIN', 'ADMIN'] or user.is_superuser):
            return Response(
                {'detail': 'Только директор может утвердить чек-лист'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if checklist.status != 'COMPLETED':
            return Response(
                {'detail': 'Чек-лист должен быть завершен перед утверждением'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        checklist.status = 'APPROVED'
        checklist.deputy_director = user
        checklist.deputy_director_signature = f"{user.first_name} {user.last_name}"
        checklist.deputy_director_signed_at = timezone.now()
        checklist.save()
        
        # Создаем уведомление водителю
        Notification.create_system_notification(
            user=checklist.trip.driver,
            title="Чек-лист одобрен",
            message=f"Ваш чек-лист для поездки '{checklist.trip.title}' одобрен. Поездка готова к отправке!",
            link=f"/dashboard/trips/{checklist.trip.id}/"
        )
        
        serializer = self.get_serializer(checklist)
        return Response({
            'detail': 'Чек-лист одобрен',
            'data': serializer.data
        })


class ChecklistItemViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пунктами чек-листа"""
    serializer_class = ChecklistItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_checked', 'is_ok', 'template__category', 'checklist__status']
    search_fields = ['template__title', 'notes']

    def get_queryset(self):
        """Получить пункты чек-листа в зависимости от роли пользователя"""
        user = self.request.user
        queryset = ChecklistItem.objects.select_related(
            'checklist', 'checklist__trip', 'template', 'checked_by'
        )
        
        if user.role in ['SUPERADMIN', 'DIRECTOR', 'ADMIN', 'DISPATCHER'] or user.is_superuser:
            return queryset
        elif user.role == 'DRIVER':
            return queryset.filter(checklist__trip__driver=user)
        elif user.role == 'MECHANIC':
            return queryset.filter(
                models.Q(checklist__mechanic=user) | 
                models.Q(checklist__status__in=['PENDING', 'IN_PROGRESS'])
            )
        else:
            return queryset.filter(checklist__status__in=['COMPLETED', 'APPROVED'])

    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        """Отметить пункт как проверенный"""
        item = self.get_object()
        user = request.user
        
        # Проверяем права на проверку
        checklist = item.checklist
        can_check = (
            user == checklist.trip.driver or
            user.role in ['MECHANIC', 'SUPERADMIN', 'ADMIN'] or
            user.is_superuser
        )
        
        if not can_check:
            return Response(
                {'detail': 'У вас нет прав для проверки этого пункта'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        item.is_checked = True
        item.is_ok = request.data.get('is_ok', True)
        item.notes = request.data.get('notes', '')
        item.checked_by = user
        item.checked_at = timezone.now()
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def uncheck(self, request, pk=None):
        """Снять отметку с пункта"""
        item = self.get_object()
        user = request.user
        
        # Проверяем права
        checklist = item.checklist
        can_uncheck = (
            user == checklist.trip.driver or
            user.role in ['MECHANIC', 'SUPERADMIN', 'ADMIN'] or
            user.is_superuser
        )
        
        if not can_uncheck:
            return Response(
                {'detail': 'У вас нет прав для изменения этого пункта'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        item.is_checked = False
        item.is_ok = True
        item.notes = ''
        item.checked_by = None
        item.checked_at = None
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def toggle(self, request, pk=None):
        """Переключить состояние пункта чек-листа"""
        item = self.get_object()
        user = request.user
        
        # Проверяем права
        checklist = item.checklist
        can_toggle = (
            user == checklist.trip.driver or
            user.role in ['MECHANIC', 'SUPERADMIN', 'ADMIN'] or
            user.is_superuser
        )
        
        if not can_toggle:
            return Response(
                {'detail': 'У вас нет прав для изменения этого пункта'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Проверяем, что чек-лист в правильном статусе
        if checklist.status not in ['PENDING', 'IN_PROGRESS']:
            return Response(
                {'detail': 'Нельзя изменять пункты утвержденного чек-листа'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Переключаем состояние
        new_checked_state = request.data.get('is_checked', not item.is_checked)
        
        item.is_checked = new_checked_state
        if new_checked_state:
            item.is_ok = request.data.get('is_ok', True)
            item.notes = request.data.get('notes', item.notes)
            item.checked_by = user
            item.checked_at = timezone.now()
        else:
            item.is_ok = True
            item.notes = ''
            item.checked_by = None
            item.checked_at = None
        
        item.save()
        
        serializer = self.get_serializer(item)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_trip_checklist(request, trip_id):
    """Получить чек-лист для конкретной поездки"""
    user = request.user
    
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return Response({'detail': 'Поездка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем права доступа
    if not (user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER'] or 
            user.is_superuser or 
            trip.driver == user):
        return Response({'detail': 'У вас нет прав для просмотра этого чек-листа'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Проверяем, есть ли чек-лист для этой поездки
    try:
        checklist = TripChecklist.objects.select_related('trip', 'trip__driver', 'trip__vehicle').prefetch_related('items__template').get(trip=trip)
        serializer = TripChecklistSerializer(checklist)
        return Response(serializer.data)
    except TripChecklist.DoesNotExist:
        return Response({'detail': 'Чек-лист для этой поездки не найден'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_checklist_for_trip(request, trip_id):
    """Создать чек-лист для поездки перед её началом"""
    user = request.user
    
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        return Response({'detail': 'Поездка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем права: водитель может создать чек-лист только для своей поездки
    # Диспетчеры и админы могут создавать для любых поездок
    if not (user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER'] or 
            user.is_superuser or 
            trip.driver == user):
        return Response({'detail': 'У вас нет прав для создания чек-листа для этой поездки'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Проверяем, что поездка в правильном статусе
    if trip.status != 'PENDING_CHECKLIST':
        return Response({'detail': f'Нельзя создать чек-лист для поездки со статусом "{trip.get_status_display()}"'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Проверяем, что чек-лист еще не создан
    if hasattr(trip, 'checklist'):
        return Response({'detail': 'Чек-лист для этой поездки уже существует'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Создаем чек-лист
    checklist_serializer = TripChecklistCreateSerializer(data={'trip': trip.id})
    if checklist_serializer.is_valid():
        checklist = checklist_serializer.save()
        
        # Изменяем статус поездки
        trip.status = 'READY'
        trip.save()
        
        # Уведомляем всех заинтересованных лиц
        from .models import Notification
        from accounts.models import User
        
        # Уведомляем водителя
        Notification.create_system_notification(
            user=trip.driver,
            title="Чек-лист создан",
            message=f"Чек-лист для поездки '{trip.title}' создан. Заполните все пункты перед началом движения.",
            link=f"/dashboard/checklist/{checklist.id}/"
        )
        
        # Уведомляем админов и директоров
        directors_and_admins = User.objects.filter(
            role__in=['DIRECTOR', 'SUPERADMIN', 'ADMIN'],
            is_active=True
        )
        
        for admin_user in directors_and_admins:
            Notification.create_system_notification(
                user=admin_user,
                title="Создан новый чек-лист",
                message=f"Создан чек-лист для поездки '{trip.title}'. Водитель: {trip.driver.get_full_name()}.",
                link=f"/dashboard/checklist/{checklist.id}/"
            )
        
        return Response({
            'detail': 'Чек-лист успешно создан',
            'checklist_id': checklist.id,
            'trip_status': trip.status
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(checklist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def generate_checklist_pdf(request, checklist_id):
    """Сгенерировать PDF чек-листа"""
    user = request.user
    
    try:
        from .models import TripChecklist
        checklist = TripChecklist.objects.select_related('trip', 'trip__driver', 'trip__vehicle').get(id=checklist_id)
    except TripChecklist.DoesNotExist:
        return Response({'detail': 'Чек-лист не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    # Проверяем права доступа
    if not (user.role in ['SUPERADMIN', 'ADMIN', 'DIRECTOR', 'DISPATCHER'] or 
            user.is_superuser or 
            checklist.trip.driver == user):
        return Response({'detail': 'У вас нет прав для просмотра этого чек-листа'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    try:
        from django.template.loader import get_template
        from django.http import HttpResponse
        from django.conf import settings
        
        # Подготавливаем контекст для PDF
        context = {
            'checklist': checklist,
            'trip': checklist.trip,
            'items_by_category': {},
            'company_name': getattr(settings, 'COMPANY_NAME', 'BARLAU.KZ'),
            'company_address': getattr(settings, 'COMPANY_ADDRESS', 'г. Алматы'),
            'STATIC_URL': request.build_absolute_uri(settings.STATIC_URL),
        }
        
        # Группируем пункты по категориям
        for item in checklist.items.select_related('template').all():
            category = item.template.get_category_display()
            if category not in context['items_by_category']:
                context['items_by_category'][category] = []
            context['items_by_category'][category].append(item)
        
        # Рендерим HTML шаблон
        template = get_template('core/checklist_pdf.html')
        html_string = template.render(context)
        
        # Создаем PDF ответ
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="checklist_{checklist.trip.title}_{checklist.id}.pdf"'
        
        try:
            # Попробуем использовать weasyprint для генерации PDF
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            font_config = FontConfiguration()
            html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
            html.write_pdf(response, font_config=font_config, presentational_hints=True)
            
        except ImportError:
            # Если weasyprint не установлен, возвращаем HTML
            response = HttpResponse(html_string, content_type='text/html')
            response['Content-Disposition'] = f'inline; filename="checklist_{checklist.trip.title}_{checklist.id}.html"'
        
        return response
        
    except Exception as e:
        return Response({
            'detail': f'Ошибка при генерации PDF: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def update_checklist_item(request, item_id):
    """Обновление пункта чек-листа"""
    try:
        item = get_object_or_404(ChecklistItem, id=item_id)
        
        # Проверяем права доступа
        user = request.user
        if not (user.is_superuser or 
                user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER'] or 
                item.checklist.trip.driver == user):
            return Response({'detail': 'Нет прав для редактирования'}, status=status.HTTP_403_FORBIDDEN)
        
        # Обновляем поля
        data = request.data
        if 'is_checked' in data:
            item.is_checked = data['is_checked']
        if 'is_ok' in data:
            item.is_ok = data['is_ok']
        if 'notes' in data:
            item.notes = data['notes']
        
        if item.is_checked:
            item.checked_by = user
            item.checked_at = timezone.now()
        
        item.save()
        
        # Обновляем статус чек-листа
        checklist = item.checklist
        if checklist.status == 'PENDING':
            checklist.status = 'IN_PROGRESS'
            checklist.save()
        
        return Response({
            'id': item.id,
            'is_checked': item.is_checked,
            'is_ok': item.is_ok,
            'notes': item.notes,
            'checked_at': item.checked_at,
            'checked_by': item.checked_by.get_full_name() if item.checked_by else None
        })
        
    except Exception as e:
        print(f"[ERROR] Error updating checklist item: {e}")
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def upload_checklist_photos(request, item_id):
    """Загрузка фото для пункта чек-листа"""
    try:
        from .models import ChecklistItemPhoto
        
        item = get_object_or_404(ChecklistItem, id=item_id)
        
        # Проверяем права доступа
        user = request.user
        if not (user.is_superuser or 
                user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER'] or 
                item.checklist.trip.driver == user):
            return Response({'detail': 'Нет прав для загрузки фото'}, status=status.HTTP_403_FORBIDDEN)
        
        photos = request.FILES.getlist('photos')
        if not photos:
            return Response({'error': 'Не выбраны файлы для загрузки'}, status=400)
        
        uploaded_photos = []
        for photo in photos:
            photo_obj = ChecklistItemPhoto.objects.create(
                item=item,
                image=photo,
                uploaded_by=user
            )
            uploaded_photos.append({
                'id': photo_obj.id,
                'image': photo_obj.image.url,
                'description': photo_obj.description,
                'uploaded_at': photo_obj.uploaded_at
            })
        
        return Response({'photos': uploaded_photos})
        
    except Exception as e:
        print(f"[ERROR] Error uploading photos: {e}")
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def delete_checklist_photo(request, photo_id):
    """Удаление фото пункта чек-листа"""
    try:
        from .models import ChecklistItemPhoto
        
        photo = get_object_or_404(ChecklistItemPhoto, id=photo_id)
        
        # Проверяем права доступа
        user = request.user
        if not (user.is_superuser or 
                user.role in ['SUPERADMIN', 'ADMIN', 'DISPATCHER'] or 
                photo.item.checklist.trip.driver == user or
                photo.uploaded_by == user):
            return Response({'detail': 'Нет прав для удаления фото'}, status=status.HTTP_403_FORBIDDEN)
        
        photo.delete()
        return Response({'message': 'Фото удалено'})
        
    except Exception as e:
        print(f"[ERROR] Error deleting photo: {e}")
        return Response({'error': str(e)}, status=500) 
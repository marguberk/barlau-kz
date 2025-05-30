from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, View, CreateView, UpdateView, FormView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.conf import settings
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from datetime import timedelta
from django.core.files.base import ContentFile
from django.template.loader import get_template
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import models
import random
import string
from django.urls import reverse_lazy
import tempfile
import pandas as pd
from io import BytesIO
import os
from django.db.models import Q
from django import forms
from accounts.models import User
from rest_framework.pagination import PageNumberPagination

from logistics.models import Task, Vehicle
from .models import Notification, Waybill, Trip
from logistics.models import Expense
from .serializers import NotificationSerializer, WaybillSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserPhotoSerializer
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django import forms
from django.http import HttpResponseForbidden
from logistics.models import Vehicle, VehiclePhoto, VehicleDocument

User = get_user_model()


class IsDirectorOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Директор может только просматривать
            return request.user.is_authenticated and (
                request.user.role in ['DIRECTOR', 'SUPERADMIN'] or request.user.is_superuser
            )
        # Только суперадмин может создавать/изменять/удалять
        return request.user.role in ['SUPERADMIN'] or request.user.is_superuser


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirectorOrSuperAdmin]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    filterset_fields = ['role', 'is_active', 'is_archived']
    ordering_fields = ['date_joined', 'last_login', 'id', 'first_name', 'role']
    ordering = ['-date_joined', 'id']

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined', 'id')

        # Фильтрация по архивным сотрудникам
        is_archived = self.request.query_params.get('is_archived', None)
        if is_archived is not None:
            is_archived = is_archived.lower() == 'true'
            queryset = queryset.filter(is_archived=is_archived)
        else:
            # По умолчанию показываем только неархивированных сотрудников
            queryset = queryset.filter(is_archived=False)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        is_active = request.data.get('is_active', not user.is_active)
        user.is_active = is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Архивировать или разархивировать сотрудника"""
        if not request.user.role in [
                'SUPERADMIN'] and not request.user.is_superuser:
            return Response(
                {"detail": "У вас нет прав для архивирования сотрудников"},
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object()
        is_archived = request.data.get('is_archived', not user.is_archived)
        user.is_archived = is_archived
        user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def upload_photo(self, request, pk=None):
        user = self.get_object()
        serializer = UserPhotoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        """Изменить роль пользователя"""
        if not request.user.role in ['SUPERADMIN']:
            return Response(
                {"detail": "У вас нет прав для изменения ролей"},
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object()
        new_role = request.data.get('role')

        if not new_role or new_role not in dict(User.Role.choices).keys():
            return Response(
                {"detail": "Указана неверная роль"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = new_role
        user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт списка сотрудников в Excel"""
        import xlsxwriter
        from io import BytesIO
        from django.http import HttpResponse

        # Создаем новый файл Excel
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Сотрудники')

        # Форматы
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#4B5563',
            'font_color': 'white',
            'border': 1
        })

        date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})

        # Заголовки
        headers = [
            'ID', 'Имя', 'Фамилия', 'Email', 'Телефон', 'Роль',
            'Должность', 'Статус', 'Дата регистрации', 'Последний вход'
        ]

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)  # Ширина колонки

        # Данные
        queryset = self.filter_queryset(self.get_queryset())

        for row, user in enumerate(queryset, start=1):
            worksheet.write(row, 0, user.id)
            worksheet.write(row, 1, user.first_name)
            worksheet.write(row, 2, user.last_name)
            worksheet.write(row, 3, user.email)
            worksheet.write(row, 4, str(user.phone))
            worksheet.write(row, 5, user.get_role_display())
            worksheet.write(row, 6, user.position or '')
            worksheet.write(
                row, 7, 'Активен' if user.is_active else 'Неактивен')
            worksheet.write(
                row,
                8,
                user.date_joined.strftime('%d.%m.%Y'),
                date_format)
            if user.last_login:
                worksheet.write(
                    row, 9, user.last_login.strftime('%d.%m.%Y'), date_format)

        workbook.close()

        # Отправляем файл
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
        return response

# Create your views here.


class NotificationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination

    def get_permissions(self):
        """
        Переопределяем получение разрешений для возврата тестовых данных неавторизованным пользователям
        """
        if self.request.method == 'GET' and settings.DEBUG:
            return []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        Переопределяем метод для обеспечения корректной работы с анонимными пользователями
        """
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
            
        if not self.request.user.is_authenticated and settings.DEBUG:
            # Для неавторизованных пользователей в режиме отладки возвращаем все уведомления
            queryset = Notification.objects.all()
        elif not self.request.user.is_authenticated:
            return Notification.objects.none()
        else:
            queryset = Notification.objects.filter(user=self.request.user)
            
        notif_type = self.request.query_params.get('type')
        unread = self.request.query_params.get('unread')
        if notif_type and notif_type != 'all':
            queryset = queryset.filter(type=notif_type)
        if unread == 'true':
            queryset = queryset.filter(read=False)
        return queryset

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Отметить все уведомления как прочитанные"""
        self.get_queryset().update(read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Отметить уведомление как прочитанное"""
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Получить количество непрочитанных уведомлений"""
        count = self.get_queryset().filter(read=False).count()
        return Response({'count': count})

    @action(detail=False, methods=['post'])
    def create_test(self, request):
        """Создать тестовое уведомление для отладки"""
        types = [Notification.Type.TASK, Notification.Type.WAYBILL,
                 Notification.Type.EXPENSE, Notification.Type.SYSTEM]
        import random
        test_type = random.choice(types)

        notification = Notification.objects.create(
            user=request.user,
            type=test_type,
            title=f"Тестовое уведомление {test_type}",
            message=f"Это тестовое уведомление типа {test_type} для проверки функциональности",
            read=False
        )

        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def delete_all(self, request):
        """Удалить все уведомления пользователя"""
        count, _ = Notification.objects.filter(user=request.user).delete()
        return Response({'deleted': count}, status=status.HTTP_204_NO_CONTENT)


class PublicNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Публичный API для уведомлений без аутентификации
    Возвращает только базовую информацию для демонстрации
    """
    serializer_class = NotificationSerializer
    permission_classes = []  # Нет требования аутентификации
    
    def get_queryset(self):
        """
        Возвращаем последние 10 уведомлений для демонстрации
        """
        print(f"[DEBUG] PublicNotificationViewSet.get_queryset() called")
        queryset = Notification.objects.all().order_by('-created_at')
        print(f"[DEBUG] Total notifications in DB: {queryset.count()}")
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Переопределяем list для ограничения количества уведомлений
        """
        print(f"[DEBUG] PublicNotificationViewSet.list() called")
        queryset = self.get_queryset()[:10]  # Берем только последние 10
        print(f"[DEBUG] Queryset slice: {len(list(queryset))}")
        serializer = self.get_serializer(queryset, many=True)
        print(f"[DEBUG] Serialized data: {len(serializer.data)}")
        return Response({
            'count': len(serializer.data),
            'next': None,
            'previous': None,
            'results': serializer.data
        })


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'home'

        if self.request.user.is_authenticated:
            # Получаем статистику
            if self.request.user.role == 'DRIVER':
                tasks_count = Task.objects.filter(
                    assigned_to=self.request.user,
                    status__in=['NEW', 'IN_PROGRESS']
                ).count()
                # Активные поездки - все поездки водителя
                active_trips_count = Trip.objects.filter(
                    driver=self.request.user
                ).count()
            elif self.request.user.role in ['DIRECTOR', 'SUPERADMIN']:
                tasks_count = Task.objects.filter(
                    status__in=['NEW', 'IN_PROGRESS']
                ).count()
                # Активные поездки - все существующие поездки
                active_trips_count = Trip.objects.all().count()
            else:
                tasks_count = Task.objects.filter(
                    created_by=self.request.user,
                    status__in=['NEW', 'IN_PROGRESS']
                ).count()
                # Активные поездки - все существующие поездки
                active_trips_count = Trip.objects.all().count()

            context['tasks_count'] = tasks_count
            context['active_trips_count'] = active_trips_count

            # Получаем последние задачи (только невыполненные)
            if self.request.user.role == 'DRIVER':
                tasks = Task.objects.filter(
                    assigned_to=self.request.user
                ).exclude(status='COMPLETED')
            elif self.request.user.role in ['DIRECTOR', 'ADMIN', 'SUPERADMIN']:
                tasks = Task.objects.exclude(status='COMPLETED')
            else:
                tasks = Task.objects.filter(
                    created_by=self.request.user
                ).exclude(status='COMPLETED')

            context['recent_tasks'] = tasks.select_related(
                'assigned_to', 'vehicle'
            ).order_by('-created_at')[:10]

            # Получаем активные поездки (поездки на сегодня) с транспортом
            from logistics.models import Vehicle
            today = timezone.now().date()
            
            if self.request.user.role == 'DRIVER':
                # Для водителя - его поездки на сегодня
                active_trips = Trip.objects.filter(
                    driver=self.request.user,
                    date=today
                ).select_related('vehicle', 'driver')[:5]
            else:
                # Для остальных - все поездки на сегодня
                active_trips = Trip.objects.filter(
                    date=today
                ).select_related('vehicle', 'driver')[:5]
            
            context['active_trips'] = active_trips
            
            # Также получаем активные транспортные средства для отображения
            if self.request.user.role == 'DRIVER':
                active_vehicles = Vehicle.objects.filter(
                    driver=self.request.user,
                    status='ACTIVE'
                ).select_related('driver')
            else:
                active_vehicles = Vehicle.objects.filter(
                    status='ACTIVE',
                    driver__isnull=False
                ).select_related('driver')[:5]  # Ограничиваем до 5 для дашборда
            
            context['active_vehicles'] = active_vehicles

            # Получаем количество непрочитанных уведомлений
            notifications_count = Notification.objects.filter(
                user=self.request.user,
                read=False
            ).count()
            context['unread_notifications'] = notifications_count
            context['notifications_count'] = notifications_count

        # Основные разделы приложения
        context['main_sections'] = [
            {
                'icon': 'tasks',
                'name': 'Задачи',
                'url': '/tasks/'
            },
            {
                'icon': 'truck',
                'name': 'Транспорт',
                'url': '/vehicles/'
            },
            {
                'icon': 'map-marker-alt',
                'name': 'Карта',
                'url': '/map/'
            },
            {
                'icon': 'file-alt',
                'name': 'КАТы',
                'url': '/waybills/'
            },
            {
                'icon': 'users',
                'name': 'Сотрудники',
                'url': '/employees/'
            },
            {
                'icon': 'wallet',
                'name': 'Финансы',
                'url': '/finance/'
            },
            {
                'icon': 'calculator',
                'name': 'Расходы',
                'url': '/expenses/'
            },
            {
                'icon': 'info-circle',
                'name': 'О нас',
                'url': '/about/'
            }
        ]

        # Быстрые действия в зависимости от роли
        quick_actions = []

        if self.request.user.is_authenticated:
            if self.request.user.role in [
                    'DIRECTOR', 'SUPERADMIN', 'ACCOUNTANT']:
                quick_actions.extend([
                    {
                        'icon': 'plus-circle',
                        'name': 'Новая задача',
                        'description': 'Создать новую задачу',
                        'url': '/tasks/add/'
                    },
                    {
                        'icon': 'user-plus',
                        'name': 'Добавить сотрудника',
                        'description': 'Зарегистрировать нового сотрудника',
                        'url': '/employees/add/'
                    }
                ])

            if self.request.user.role == 'DRIVER':
                quick_actions.extend([
                    {
                        'icon': 'location-arrow',
                        'name': 'Обновить локацию',
                        'description': 'Обновить текущее местоположение',
                        'url': '/map/'
                    },
                    {
                        'icon': 'file-signature',
                        'name': 'Новый КАТ',
                        'description': 'Создать путевой лист',
                        'url': '/waybills/add/'
                    }
                ])

            if self.request.user.role in ['ACCOUNTANT', 'SUPPLIER']:
                quick_actions.extend([
                    {
                        'icon': 'receipt',
                        'name': 'Новый расход',
                        'description': 'Добавить новый расход',
                        'url': '/expenses/add/'
                    },
                    {
                        'icon': 'file-invoice',
                        'name': 'Отчет',
                        'description': 'Сформировать финансовый отчет',
                        'url': '/finance/'
                    }
                ])

        context['quick_actions'] = quick_actions

        return context


class AboutPageView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['company_info'] = {
            'name': 'Barlau.kz',
            'description': 'Система управления логистической компанией',
            'features': [
                {
                    'icon': 'truck',
                    'title': 'Управление транспортом',
                    'description': 'Отслеживание местоположения и состояния транспортных средств в реальном времени'
                },
                {
                    'icon': 'tasks',
                    'title': 'Управление задачами',
                    'description': 'Создание и отслеживание задач для водителей и других сотрудников'
                },
                {
                    'icon': 'file-alt',
                    'title': 'Путевые листы',
                    'description': 'Электронные КАТы и документооборот'
                },
                {
                    'icon': 'calculator',
                    'title': 'Учет расходов',
                    'description': 'Контроль и анализ расходов на топливо и обслуживание'
                }
            ],
            'contacts': {
                'address': 'г. Алматы, ул. Примерная, 123',
                'phone': '+7 700 123-45-67',
                'email': 'info@barlau.kz',
                'working_hours': 'Пн-Пт: 9:00 - 18:00'
            }
        }

        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Получаем статистику по задачам
        tasks = Task.objects.filter(assigned_to=user)
        context['tasks_count'] = tasks.count()
        context['new_tasks_count'] = tasks.filter(status='NEW').count()
        context['in_progress_tasks_count'] = tasks.filter(
            status='IN_PROGRESS').count()
        context['completed_tasks_count'] = tasks.filter(
            status='COMPLETED').count()

        # Статистика по путевым листам для водителей
        if user.role == 'DRIVER':
            today = timezone.now().date()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)

            waybills = Waybill.objects.filter(driver=user)
            context['waybills_count'] = waybills.count()
            context['today_waybills_count'] = waybills.filter(
                date=today).count()
            context['week_waybills_count'] = waybills.filter(
                date__gte=week_ago).count()
            context['month_waybills_count'] = waybills.filter(
                date__gte=month_ago).count()

        # Статистика по расходам для бухгалтеров и снабженцев
        if user.role in ['ACCOUNTANT', 'SUPPLIER']:
            expenses = Expense.objects.filter(created_by=user)
            context['expenses_count'] = expenses.count()
            context['pending_expenses_count'] = expenses.filter(
                status='PENDING').count()
            context['approved_expenses_count'] = expenses.filter(
                status='APPROVED').count()
            context['rejected_expenses_count'] = expenses.filter(
                status='REJECTED').count()

        # Уведомления
        from datetime import datetime, time
        today_min = datetime.combine(timezone.now().date(), time.min)
        today_max = datetime.combine(timezone.now().date(), time.max)

        notifications = Notification.objects.filter(user=user)
        context['notifications_count'] = notifications.count()
        context['unread_notifications_count'] = notifications.filter(
            read=False).count()
        context['today_notifications_count'] = notifications.filter(
            created_at__range=(today_min, today_max)
        ).count()

        # Последние действия
        context['recent_actions'] = self.get_recent_actions(user)

        return context

    def get_recent_actions(self, user):
        # Здесь можно добавить логику получения последних действий пользователя
        # Например, из логов, истории действий и т.д.

        # Пример:
        actions = []

        # Последние задачи
        recent_tasks = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user)
        ).order_by('-updated_at')[:3]

        for task in recent_tasks:
            if task.created_by == user:
                actions.append({
                    'icon': 'plus-circle',
                    'description': f'Создана задача "{task.title}"',
                    'timestamp': task.created_at
                })
            else:
                actions.append({
                    'icon': 'tasks',
                    'description': f'Назначена задача "{task.title}"',
                    'timestamp': task.updated_at
                })

        # Последние уведомления
        recent_notifications = Notification.objects.filter(
            user=user
        ).order_by('-created_at')[:3]

        for notification in recent_notifications:
            actions.append({
                'icon': 'bell',
                'description': notification.title,
                'timestamp': notification.created_at
            })

        # Сортируем по времени
        actions.sort(key=lambda x: x['timestamp'], reverse=True)

        return actions[:5]  # Возвращаем максимум 5 действий


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_notifications'] = Notification.objects.filter(
            user=self.request.user,
            read=False
        ).count()
        return context


class TasksView(LoginRequiredMixin, TemplateView):
    template_name = 'core/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'tasks'

        # Загружаем задачи из базы данных для начального рендеринга страницы
        from logistics.models import Task

        # Получаем модель пользователя
        User = get_user_model()

        # Получаем все задачи
        tasks = Task.objects.all().select_related(
            'assigned_to', 'vehicle', 'created_by')

        # Фильтрация по ролям:
        # - Водители видят только свои задачи
        # - Директора, Админы и Суперадмины видят все задачи
        # - Остальные роли видят задачи, которые создали или которые им назначены
        if self.request.user.role == 'DRIVER':
            tasks = tasks.filter(assigned_to=self.request.user)
        elif self.request.user.role in ['DIRECTOR', 'ADMIN', 'SUPERADMIN']:
            # Показываем все задачи без фильтрации
            pass
        else:
            # Для остальных ролей - задачи которые создали или им назначены
            tasks = tasks.filter(
                models.Q(created_by=self.request.user) | 
                models.Q(assigned_to=self.request.user)
            )

        context['initial_tasks'] = tasks
        return context


class TaskCreateView(LoginRequiredMixin, View):
    template_name = 'core/task_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')

        # Проверяем права доступа
        if not request.user.role in [
                'DIRECTOR', 'SUPERADMIN', 'TECH'] and not request.user.is_superuser:
            return redirect('core:tasks')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Получаем список сотрудников для поля выбора исполнителя
        User = get_user_model()
        employees = User.objects.filter(is_active=True)

        # Получаем список транспорта для поля выбора
        from logistics.models import Vehicle
        vehicles = Vehicle.objects.all()

        context = {
            'employees': employees,
            'vehicles': vehicles,
            'form_title': 'Новая задача',
            'active_page': 'tasks'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        from logistics.models import Task, Vehicle

        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        assigned_to_id = request.POST.get('assigned_to')
        vehicle_id = request.POST.get('vehicle')

        # Валидация
        if not title or not description or not priority or not due_date:
            messages.error(
                request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('core:task-add')

        # Создаем задачу
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            created_by=request.user
        )

        # Если выбран исполнитель
        if assigned_to_id:
            User = get_user_model()
            try:
                task.assigned_to = User.objects.get(id=assigned_to_id)
            except User.DoesNotExist:
                pass

        # Если выбран транспорт
        if vehicle_id:
            try:
                task.vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                pass

        try:
            task.save()
            # --- Уведомления ---
            print('[DEBUG] Перед созданием уведомления о задаче', task.created_by, task)
            from core.models import Notification
            # Уведомление только для исполнителя, если он назначен и это не создатель
            if task.assigned_to and task.assigned_to != task.created_by:
                Notification.create_task_notification(task.assigned_to, task)
            messages.success(request, 'Задача успешно создана')
            # Перенаправляем на страницу со всеми задачами
            return redirect('core:tasks')
        except Exception as e:
            # Обрабатываем возможные ошибки при создании задачи
            messages.error(request, f'Ошибка при создании задачи: {str(e)}')

            # Готовим контекст для повторного отображения формы
            User = get_user_model()
            employees = User.objects.filter(is_active=True)
            vehicles = Vehicle.objects.all()

            context = {
                'employees': employees,
                'vehicles': vehicles,
                'form_title': 'Новая задача',
                'active_page': 'tasks',
                'form_data': {
                    'title': title,
                    'description': description,
                    'priority': priority,
                    'due_date': due_date,
                    'assigned_to_id': assigned_to_id,
                    'vehicle_id': vehicle_id
                }
            }
            return render(request, self.template_name, context)


class TaskUpdateView(LoginRequiredMixin, View):
    template_name = 'core/task_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')

        # Проверяем существование задачи
        from logistics.models import Task
        try:
            self.task = Task.objects.get(id=kwargs['pk'])
        except Task.DoesNotExist:
            messages.error(request, 'Задача не найдена')
            return redirect('core:tasks')

        # Проверяем права доступа
        if not (request.user.role in ['DIRECTOR', 'SUPERADMIN', 'TECH'] or
                request.user == self.task.created_by or
                request.user == self.task.assigned_to):
            messages.error(
                request, 'У вас нет прав для редактирования этой задачи')
            return redirect('core:tasks')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        # Получаем список сотрудников для поля выбора исполнителя
        User = get_user_model()
        employees = User.objects.filter(is_active=True)

        # Получаем список транспорта для поля выбора
        from logistics.models import Vehicle
        vehicles = Vehicle.objects.all()

        context = {
            'task': self.task,
            'employees': employees,
            'vehicles': vehicles,
            'form_title': f'Редактирование задачи "{self.task.title}"',
            'active_page': 'tasks'
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        assigned_to_id = request.POST.get('assigned_to')
        vehicle_id = request.POST.get('vehicle')

        # Валидация
        if not title or not description or not priority or not due_date:
            messages.error(
                request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('core:task-edit', pk=pk)

        # Обновляем задачу
        task = self.task
        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date

        # Если выбран исполнитель
        if assigned_to_id:
            User = get_user_model()
            try:
                new_assigned_to = User.objects.get(id=assigned_to_id)
                if task.assigned_to != new_assigned_to:
                    old_assigned_to = task.assigned_to
                    task.assigned_to = new_assigned_to
                    # Уведомление больше не создаём здесь, оно теперь только в API
            except User.DoesNotExist:
                pass
        else:
            task.assigned_to = None

        # Если выбран транспорт
        if vehicle_id:
            from logistics.models import Vehicle
            try:
                task.vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                pass
        else:
            task.vehicle = None

        task.save()

        messages.success(request, 'Задача успешно обновлена')
        return redirect('core:tasks')


class TaskArchiveView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')

        # Проверяем существование задачи
        from logistics.models import Task
        try:
            self.task = Task.objects.get(id=kwargs['pk'])
        except Task.DoesNotExist:
            messages.error(request, 'Задача не найдена')
            return redirect('core:tasks')

        # Проверяем права доступа
        if not (request.user.role in ['DIRECTOR', 'SUPERADMIN', 'TECH'] or
                request.user == self.task.created_by):
            messages.error(request, 'У вас нет прав для архивации этой задачи')
            return redirect('core:tasks')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        # Архивируем задачу
        self.task.status = 'CANCELLED'
        self.task.save()

        messages.success(request, 'Задача отменена и перемещена в архив')
        return redirect('core:tasks')


class ExpensesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'expenses'
        return context


class FinanceView(LoginRequiredMixin, TemplateView):
    template_name = 'core/finance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'finance'

        # Проверяем доступ к финансовой информации
        context['can_view_finance'] = self.request.user.role in [
            'DIRECTOR', 'SUPERADMIN', 'ACCOUNTANT'
        ]

        return context


class EmployeesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/employees.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Разрешаем всем аутентифицированным пользователям просматривать
        # страницу сотрудников
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем список активных сотрудников
        context['employees'] = User.objects.filter(
            is_active=True).order_by(
            'last_name', 'first_name')
        context['active_page'] = 'employees'
        context['can_manage_employees'] = self.request.user.role in [
            'DIRECTOR', 'SUPERADMIN'] or self.request.user.is_superuser
        return context


class WaybillViewSet(viewsets.ModelViewSet):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    filterset_fields = ['vehicle', 'driver', 'date']
    search_fields = [
        'number',
        'departure_point',
        'destination_point',
        'cargo_description']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'DRIVER':
            return queryset.filter(driver=self.request.user)
        return queryset

    @action(detail=True, methods=['get'])
    def print(self, request, pk=None):
        waybill = self.get_object()

        # Подготовка контекста для шаблона
        context = {
            'waybill': waybill,
            'company_name': 'Ваша компания',
            'company_address': 'Адрес компании',
            'company_phone': 'Телефон компании',
        }

        # Рендеринг HTML
        html_string = render_to_string('core/waybill_pdf.html', context)

        # Создание PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf') as output:
            HTML(string=html_string).write_pdf(output.name)
            output.seek(0)
            response = HttpResponse(
                output.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="waybill-{
                waybill.number}.pdf"'
            return response

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """
        Экспорт путевых листов в Excel
        """
        # Получаем отфильтрованный queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Создаем DataFrame
        data = []
        for waybill in queryset:
            data.append({
                'Номер': waybill.number,
                'Дата': waybill.date,
                'Транспорт': f"{waybill.vehicle.brand} {waybill.vehicle.model} ({waybill.vehicle.number})",
                'Водитель': f"{waybill.driver.first_name} {waybill.driver.last_name}",
                'Пункт отправления': waybill.departure_point,
                'Пункт назначения': waybill.destination_point,
                'Описание груза': waybill.cargo_description,
                'Вес груза (кг)': waybill.cargo_weight,
                'Создан': waybill.created_at,
                'Создатель': f"{waybill.created_by.first_name} {waybill.created_by.last_name}" if waybill.created_by else ""
            })

        df = pd.DataFrame(data)

        # Создаем Excel файл
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Путевые листы', index=False)

            # Автоматическая настройка ширины столбцов
            worksheet = writer.sheets['Путевые листы']
            for i, col in enumerate(df.columns):
                column_width = max(
                    df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)

        # Подготавливаем ответ
        output.seek(0)
        filename = f"waybills_export_{
            timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response


class WaybillListView(LoginRequiredMixin, TemplateView):
    template_name = 'core/waybills.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'waybills'
        return context


class WaybillPrintView(LoginRequiredMixin, DetailView):
    model = Waybill

    def get(self, request, *args, **kwargs):
        waybill = self.get_object()

        # Проверяем права доступа
        if not (request.user.is_superuser or request.user == waybill.driver or
                request.user == waybill.created_by or request.user.role in ['DIRECTOR', 'ACCOUNTANT']):
            return HttpResponse('Доступ запрещен', status=403)

        # Подготовка контекста для шаблона
        context = {
            'waybill': waybill,
            'company_name': settings.COMPANY_NAME,
            'company_address': settings.COMPANY_ADDRESS,
            'company_phone': settings.COMPANY_PHONE,
        }

        # Рендеринг HTML
        html_string = render_to_string('core/waybill_pdf.html', context)

        # Создание PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf') as output:
            HTML(string=html_string).write_pdf(output.name)
            output.seek(0)
            response = HttpResponse(
                output.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="waybill-{
                waybill.number}.pdf"'
            return response


class WaybillCreateView(LoginRequiredMixin, CreateView):
    model = Waybill
    template_name = 'core/waybill_form.html'
    fields = ['date', 'vehicle', 'driver', 'departure_point', 'destination_point',
              'cargo_description', 'cargo_weight']
    success_url = reverse_lazy('core:waybills')

    def dispatch(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not (request.user.is_superuser or request.user.role in [
                'DIRECTOR', 'SUPERADMIN', 'DRIVER']):
            return HttpResponseForbidden(
                'У вас нет прав для создания путевых листов')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ограничиваем выбор водителей только водителями
        form.fields['driver'].queryset = User.objects.filter(
            role='DRIVER', is_active=True)
        # Если пользователь - водитель, устанавливаем его как водителя по
        # умолчанию
        if self.request.user.role == 'DRIVER':
            form.fields['driver'].initial = self.request.user
            form.fields['driver'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        # Устанавливаем создателя путевого листа
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'waybills'
        context['title'] = 'Создание путевого листа'
        return context


class WaybillUpdateView(LoginRequiredMixin, UpdateView):
    model = Waybill
    template_name = 'core/waybill_form.html'
    fields = ['date', 'vehicle', 'driver', 'departure_point', 'destination_point',
              'cargo_description', 'cargo_weight']

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')

        # Проверяем существование транспорта
        from logistics.models import Vehicle
        try:
            self.vehicle = Vehicle.objects.get(id=kwargs['pk'])
        except Vehicle.DoesNotExist:
            messages.error(request, 'Транспорт не найден')
            return redirect('core:vehicles')

        # Проверяем права доступа
        if not request.user.role in [
                'DIRECTOR', 'SUPERADMIN', 'TECH'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для редактирования транспорта')
            return redirect('core:vehicles')

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ограничиваем выбор водителей только водителями
        form.fields['driver'].queryset = User.objects.filter(
            role='DRIVER', is_active=True)
        # Если пользователь - водитель, блокируем изменение водителя
        if self.request.user.role == 'DRIVER':
            form.fields['driver'].widget.attrs['readonly'] = True
        return form

    def get_success_url(self):
        return reverse_lazy('core:waybills')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'waybills'
        context['title'] = 'Редактирование путевого листа'
        return context


class WaybillDeleteView(LoginRequiredMixin, View):
    """
    Представление для удаления путевого листа
    """

    def dispatch(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.role not in [
                'DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для удаления путевых листов')
            return redirect('core:waybills')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        waybill = get_object_or_404(Waybill, pk=pk)
        waybill_number = waybill.number

        try:
            waybill.delete()
            messages.success(
                request, f'Путевой лист №{waybill_number} успешно удален')
        except Exception as e:
            messages.error(
                request,
                f'Ошибка при удалении путевого листа: {
                    str(e)}')

        return redirect('core:waybills')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EmployeePDFView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/employee_pdf.html'

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        # Подготавливаем контекст
        context = {
            'employee': user,
            'company_name': settings.COMPANY_NAME,
            'company_address': settings.COMPANY_ADDRESS,
            'company_phone': settings.COMPANY_PHONE,
            'company_email': settings.COMPANY_EMAIL,
            'STATIC_URL': request.build_absolute_uri(settings.STATIC_URL),
            'MEDIA_URL': request.build_absolute_uri(settings.MEDIA_URL),
        }

        # Рендерим HTML
        template = get_template(self.template_name)
        html_string = template.render(context)

        # Создаем PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{
            user.get_full_name()}_resume.pdf"'

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

        return response


class EmployeeFormView(LoginRequiredMixin, View):
    template_name = 'core/employee_form.html'

    def get_employee(self, pk=None):
        if pk:
            return get_object_or_404(User, pk=pk)
        return None

    def get(self, request, pk=None):
        employee = self.get_employee(pk)
        roles = User.Role.choices
        return render(request, self.template_name, {
            'employee': employee,
            'roles': roles,
        })

    def post(self, request, pk=None):
        employee = self.get_employee(pk)

        if employee:
            # Обновление существующего сотрудника
            form_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'position': request.POST.get('position'),
                'role': request.POST.get('role'),
                'age': request.POST.get('age'),
                'desired_salary': request.POST.get('desired_salary'),
                'location': request.POST.get('location'),
                'skype': request.POST.get('skype'),
                'linkedin': request.POST.get('linkedin'),
                'portfolio_url': request.POST.get('portfolio_url'),
                'about_me': request.POST.get('about_me'),
                'experience': request.POST.get('experience'),
                'education': request.POST.get('education'),
                'key_skills': request.POST.get('key_skills'),
                'achievements': request.POST.get('achievements'),
                'courses': request.POST.get('courses'),
                'publications': request.POST.get('publications'),
                'recommendations': request.POST.get('recommendations'),
                'hobbies': request.POST.get('hobbies'),
            }

            for field, value in form_data.items():
                if value:
                    setattr(employee, field, value)

            if 'photo' in request.FILES:
                employee.photo = request.FILES['photo']

            employee.save()
            messages.success(request, 'Сотрудник успешно обновлен')
        else:
            # Создание нового сотрудника
            employee = User.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                position=request.POST.get('position'),
                role=request.POST.get('role'),
                age=request.POST.get('age'),
                desired_salary=request.POST.get('desired_salary'),
                location=request.POST.get('location'),
                skype=request.POST.get('skype'),
                linkedin=request.POST.get('linkedin'),
                portfolio_url=request.POST.get('portfolio_url'),
                about_me=request.POST.get('about_me'),
                experience=request.POST.get('experience'),
                education=request.POST.get('education'),
                key_skills=request.POST.get('key_skills'),
                achievements=request.POST.get('achievements'),
                courses=request.POST.get('courses'),
                publications=request.POST.get('publications'),
                recommendations=request.POST.get('recommendations'),
                hobbies=request.POST.get('hobbies'),
            )

            if 'photo' in request.FILES:
                employee.photo = request.FILES['photo']
                employee.save()

            messages.success(request, 'Сотрудник успешно создан')

        return redirect('core:employees')


@method_decorator(csrf_exempt, name='dispatch')
class EmployeePhotoUploadView(LoginRequiredMixin, View):
    """Представление для загрузки фотографий сотрудников через AJAX."""

    def post(self, request, pk):
        if not request.user.role in [
                'SUPERADMIN'] and not request.user.is_superuser:
            return JsonResponse(
                {'error': 'У вас нет прав для выполнения этого действия'}, status=403)

        employee = get_object_or_404(User, pk=pk)

        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            # Проверка типа файла
            if not photo.content_type.startswith('image/'):
                return JsonResponse(
                    {'error': 'Загружаемый файл должен быть изображением'}, status=400)

            # Проверка размера файла (максимум 5 МБ)
            if photo.size > 5 * 1024 * 1024:
                return JsonResponse(
                    {'error': 'Размер файла не должен превышать 5 МБ'}, status=400)

            # Сохраняем фото
            employee.photo = photo
            employee.save()

            return JsonResponse({
                'success': True,
                'message': 'Фото успешно загружено',
                'photo_url': employee.photo.url
            })
        else:
            return JsonResponse({'error': 'Файл не был загружен'}, status=400)


class EmployeeListView(LoginRequiredMixin, View):
    template_name = 'core/employee_list.html'

    def get(self, request):
        # Проверяем права доступа
        if not request.user.role in [
                'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для просмотра списка сотрудников')
            return redirect('core:home')

        # Получаем список сотрудников
        employees = User.objects.all().order_by('last_name', 'first_name')

        # Фильтрация по роли, если указана
        role = request.GET.get('role')
        if role:
            employees = employees.filter(role=role)

        # Поиск по имени, фамилии или email
        search = request.GET.get('search')
        if search:
            employees = employees.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(position__icontains=search)
            )

        return render(request, self.template_name, {
            'employees': employees,
            'roles': User.Role.choices,
            'current_role': role,
            'search': search
        })


class EmployeeCreateView(View):
    template_name = 'core/employee_form.html'

    def get(self, request):
        # Проверка прав доступа
        if not request.user.is_authenticated or request.user.role not in [
                'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для добавления сотрудников')
            return redirect('core:index')

        # Получение списка ролей для формы
        roles = User.Role.choices

        context = {
            'roles': roles,
            'is_new': True,
            'title': 'Добавление нового сотрудника'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Проверка прав доступа
        if not request.user.is_authenticated or request.user.role not in [
                'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для добавления сотрудников')
            return redirect('core:index')

        # Получение данных из формы
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        position = request.POST.get('position', '')
        role = request.POST.get('role', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Базовая валидация
        errors = {}
        if not first_name:
            errors['first_name'] = 'Имя обязательно для заполнения'
        if not last_name:
            errors['last_name'] = 'Фамилия обязательна для заполнения'
        if not email:
            errors['email'] = 'Email обязателен для заполнения'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Пользователь с таким email уже существует'
        # Валидация пароля
        if password or password2:
            if password != password2:
                errors['password2'] = 'Пароли не совпадают'
            elif len(password) < 6:
                errors['password'] = 'Пароль должен быть не короче 6 символов'

        # Если есть ошибки, возвращаем форму с ошибками
        if errors:
            context = {
                'errors': errors,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'position': position,
                'selected_role': role,
                'roles': User.Role.choices,
                'is_new': True,
                'title': 'Добавление нового сотрудника'
            }
            return render(request, self.template_name, context)

        # Создание нового пользователя
        username = email.split('@')[0]
        # Генерация уникального имени пользователя
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Используем введённый пароль или генерируем
        if password and password2 and password == password2:
            final_password = password
        else:
            final_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=final_password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            position=position,
            role=role
        )

        # Дополнительные поля из формы
        user.desired_salary = request.POST.get('desired_salary', '')
        # Обработка числового поля age - если пустое, устанавливаем None
        age_value = request.POST.get('age', '').strip()
        try:
            user.age = int(age_value) if age_value else None
        except ValueError:
            user.age = None
        user.location = request.POST.get('location', '')
        user.skills = request.POST.get('skills', '')
        user.experience = request.POST.get('experience', '')
        user.education = request.POST.get('education', '')
        user.certifications = request.POST.get('certifications', '')
        user.languages = request.POST.get('languages', '')
        user.hobbies = request.POST.get('hobbies', '')

        # Обработка загрузки фото
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        # Обработка загрузки файла рекомендации
        if 'recommendation_file' in request.FILES:
            user.recommendation_file = request.FILES['recommendation_file']

        user.save()

        messages.success(
            request, f'Сотрудник {user.get_full_name()} успешно создан. Логин: {username}, пароль: {final_password}')
        return redirect('core:employees')


class EmployeeEditView(View):
    template_name = 'core/employee_form.html'

    def get(self, request, pk):
        # Проверка прав доступа
        if not request.user.is_authenticated or request.user.role not in [
                'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для редактирования сотрудников')
            return redirect('core:index')

        # Получение сотрудника
        try:
            employee = User.objects.get(pk=pk)
        except User.DoesNotExist:
            messages.error(request, 'Сотрудник не найден')
            return redirect('core:employees')

        # Получение списка ролей для формы
        roles = User.Role.choices

        context = {
            'employee': employee,
            'roles': roles,
            'is_new': False,
            'title': f'Редактирование сотрудника: {employee.get_full_name()}'
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        # Проверка прав доступа
        if not request.user.is_authenticated or request.user.role not in [
                'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для редактирования сотрудников')
            return redirect('core:index')

        # Получение сотрудника
        try:
            employee = User.objects.get(pk=pk)
        except User.DoesNotExist:
            messages.error(request, 'Сотрудник не найден')
            return redirect('core:employees')

        # Получение данных из формы
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        position = request.POST.get('position', '')
        role = request.POST.get('role', '')

        # Базовая валидация
        errors = {}
        if not first_name:
            errors['first_name'] = 'Имя обязательно для заполнения'
        if not last_name:
            errors['last_name'] = 'Фамилия обязательна для заполнения'
        if not email:
            errors['email'] = 'Email обязателен для заполнения'
        elif User.objects.filter(email=email).exclude(pk=pk).exists():
            errors['email'] = 'Пользователь с таким email уже существует'

        # Если есть ошибки, возвращаем форму с ошибками
        if errors:
            context = {
                'employee': employee,
                'errors': errors,
                'roles': User.Role.choices,
                'is_new': False,
                'title': f'Редактирование сотрудника: {employee.get_full_name()}'
            }
            return render(request, self.template_name, context)

        # Обновление данных сотрудника
        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone = phone
        employee.position = position
        employee.role = role

        # Дополнительные поля из формы
        employee.desired_salary = request.POST.get('desired_salary', '')
        # Обработка числового поля age - если пустое, устанавливаем None
        age_value = request.POST.get('age', '').strip()
        try:
            employee.age = int(age_value) if age_value else None
        except ValueError:
            employee.age = None
        employee.location = request.POST.get('location', '')
        employee.skills = request.POST.get('skills', '')
        employee.experience = request.POST.get('experience', '')
        employee.education = request.POST.get('education', '')
        employee.certifications = request.POST.get('certifications', '')
        employee.languages = request.POST.get('languages', '')
        employee.hobbies = request.POST.get('hobbies', '')

        # Обработка загрузки фото
        if 'photo' in request.FILES:
            # Если было предыдущее фото, удаляем его
            if employee.photo:
                try:
                    old_photo_path = employee.photo.path
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                except Exception as e:
                    # Логирование ошибки, но продолжаем выполнение
                    print(f"Ошибка при удалении старого фото: {e}")

            employee.photo = request.FILES['photo']

        # Обработка загрузки файла рекомендации
        if 'recommendation_file' in request.FILES:
            # Если был предыдущий файл, удаляем его
            if employee.recommendation_file:
                try:
                    old_file_path = employee.recommendation_file.path
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                except Exception as e:
                    # Логирование ошибки, но продолжаем выполнение
                    print(
                        f"Ошибка при удалении старого файла рекомендации: {e}")

            employee.recommendation_file = request.FILES['recommendation_file']

        employee.save()

        messages.success(
            request, f'Данные сотрудника {
                employee.get_full_name()} успешно обновлены')
        return redirect('core:employees')


class EmployeeDeleteView(View):
    def delete(self, request, pk):
        # Проверка прав доступа - только суперадмины
        if not request.user.is_authenticated or request.user.role != 'SUPERADMIN':
            return JsonResponse({'error': 'У вас нет прав для удаления сотрудников'}, status=403)

        # Получение сотрудника
        try:
            employee = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Сотрудник не найден'}, status=404)

        # Проверка, что не удаляем самого себя
        if employee == request.user:
            return JsonResponse({'error': 'Нельзя удалить самого себя'}, status=400)

        # Проверка, что не удаляем других суперадминов (опционально)
        if employee.role == 'SUPERADMIN':
            return JsonResponse({'error': 'Нельзя удалить суперадминистратора'}, status=400)

        try:
            employee_name = employee.get_full_name()
            employee.delete()
            
            # Логируем действие
            print(f"[INFO] Сотрудник {employee_name} (ID: {pk}) удален пользователем {request.user.username}")
            
            return JsonResponse({'success': True, 'message': f'Сотрудник {employee_name} успешно удален'})
        
        except Exception as e:
            print(f"[ERROR] Ошибка при удалении сотрудника: {e}")
            return JsonResponse({'error': 'Ошибка при удалении сотрудника'}, status=500)


class VehiclesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/vehicles.html'

    def get(self, request, *args, **kwargs):
        return redirect('core:trucks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'vehicles'
        return context


class VehicleForm(forms.Form):
    # Основная информация
    number = forms.CharField(max_length=20, required=True)
    vehicle_type = forms.ChoiceField(choices=[
        ('CAR', 'Легковой'),
        ('TRUCK', 'Грузовой'),
        ('SPECIAL', 'Спецтехника')
    ], required=True)
    brand = forms.CharField(max_length=100, required=True)
    model = forms.CharField(max_length=100, required=True)
    year = forms.IntegerField(required=True, min_value=1900, max_value=2100)
    color = forms.CharField(max_length=50, required=False)
    status = forms.ChoiceField(choices=[
        ('ACTIVE', 'Активен'),
        ('INACTIVE', 'Неактивен'),
        ('MAINTENANCE', 'На обслуживании')
    ], required=True)
    driver = forms.ModelChoiceField(queryset=None, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    # Технические характеристики
    vin_number = forms.CharField(max_length=50, required=False)
    engine_number = forms.CharField(max_length=50, required=False)
    chassis_number = forms.CharField(max_length=50, required=False)
    engine_capacity = forms.FloatField(required=False)
    fuel_type = forms.ChoiceField(choices=[
        ('', 'Не указан'),
        ('DIESEL', 'Дизель'),
        ('PETROL', 'Бензин'),
        ('GAS', 'Газ'),
        ('HYBRID', 'Гибрид'),
        ('ELECTRIC', 'Электро')
    ], required=False)
    fuel_consumption = forms.FloatField(required=False)
    length = forms.FloatField(required=False)
    width = forms.FloatField(required=False)
    height = forms.FloatField(required=False)
    max_weight = forms.IntegerField(required=False)
    cargo_capacity = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        drivers = kwargs.pop('drivers', None)
        super().__init__(*args, **kwargs)
        if drivers is not None:
            self.fields['driver'].queryset = drivers


class VehicleCreateView(LoginRequiredMixin, View):
    template_name = 'core/vehicle_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.role in [
                'DIRECTOR', 'MANAGER', 'SUPERADMIN'] or request.user.is_superuser):
            return HttpResponseForbidden(
                "У вас нет прав для создания транспорта")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Получаем список водителей для поля выбора
        User = get_user_model()
        drivers = User.objects.filter(is_active=True, role='DRIVER')

        form = VehicleForm(drivers=drivers)
        return render(request, self.template_name, {
            'form': form,
            'drivers': drivers,
            'title': 'Добавление транспорта',
            'action': 'create'
        })

    def post(self, request):
        print('[DEBUG] post VehicleCreateView')
        User = get_user_model()
        drivers = User.objects.filter(is_active=True, role='DRIVER')
        import os
        from django.core.files.base import File
        from django.core.files.storage import default_storage

        form = VehicleForm(request.POST, request.FILES, drivers=drivers)
        if not form.is_valid():
            print('[DEBUG] Форма транспорта невалидна:', form.errors)
            context = {
                'form': form,
                'drivers': drivers,
                'title': 'Добавление транспорта',
                'action': 'create'}
            return render(request, self.template_name, context)
        print('[DEBUG] Форма транспорта валидна')
        # Если валидно, создаем транспорт без файлов сначала
        data = form.cleaned_data
        vehicle = Vehicle(
            number=data['number'],
            vehicle_type=data['vehicle_type'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            color=data.get('color'),
            status=data['status'],
            driver=data.get('driver'),
            description=data.get('description'),
            vin_number=data.get('vin_number'),
            engine_number=data.get('engine_number'),
            chassis_number=data.get('chassis_number'),
            engine_capacity=data.get('engine_capacity'),
            fuel_type=data.get('fuel_type'),
            fuel_consumption=data.get('fuel_consumption'),
            length=data.get('length'),
            width=data.get('width'),
            height=data.get('height'),
            max_weight=data.get('max_weight'),
            cargo_capacity=data.get('cargo_capacity'),
            created_by=request.user
        )
        vehicle.save()
        print('[DEBUG] Транспорт сохранён:', vehicle)

        # --- Основное фото ---
        main_photo_path = request.POST.get('main_photo_path')
        if main_photo_path:
            with default_storage.open(main_photo_path, 'rb') as f:
                VehiclePhoto.objects.create(
                    vehicle=vehicle,
                    photo=File(f, name=os.path.basename(main_photo_path)),
                    is_main=True,
                    uploaded_by=request.user
                )
        elif 'main_photo' in request.FILES:
            VehiclePhoto.objects.create(
                vehicle=vehicle,
                photo=request.FILES['main_photo'],
                is_main=True,
                uploaded_by=request.user
            )

        # --- Дополнительные фото ---
        additional_photos_paths = request.POST.get('additional_photos_paths', '')
        for path in filter(None, additional_photos_paths.split(',')):
            with default_storage.open(path, 'rb') as f:
                VehiclePhoto.objects.create(
                    vehicle=vehicle,
                    photo=File(f, name=os.path.basename(path)),
                    is_main=False,
                    uploaded_by=request.user
                )
        for photo in request.FILES.getlist('additional_photos'):
            VehiclePhoto.objects.create(
                vehicle=vehicle,
                photo=photo,
                is_main=False,
                uploaded_by=request.user
            )

        # --- Технический паспорт ---
        technical_passport_expiry = request.POST.get('registration_expiry_date') or None
        technical_passport_path = request.POST.get('technical_passport_path')
        if technical_passport_path:
            with default_storage.open(technical_passport_path, 'rb') as f:
                doc = VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='REGISTRATION',
                    file=File(f, name=os.path.basename(technical_passport_path)),
                    created_by=request.user,
                    issue_date=timezone.now().date(),
                    expiry_date=technical_passport_expiry
                )
                print(f'[DEBUG] Создан документ: {doc}, expiry_date={doc.expiry_date}')
                create_expiry_notification(vehicle, 'REGISTRATION', doc.expiry_date)
        elif 'technical_passport' in request.FILES:
            doc = VehicleDocument.objects.create(
                vehicle=vehicle,
                document_type='REGISTRATION',
                file=request.FILES['technical_passport'],
                created_by=request.user,
                issue_date=timezone.now().date(),
                expiry_date=technical_passport_expiry
            )
            print(f'[DEBUG] Создан документ: {doc}, expiry_date={doc.expiry_date}')
            create_expiry_notification(vehicle, 'REGISTRATION', doc.expiry_date)

        # --- Страховка ---
        insurance_expiry = request.POST.get('insurance_expiry_date') or None
        insurance_path = request.POST.get('insurance_path')
        if insurance_path:
            with default_storage.open(insurance_path, 'rb') as f:
                doc = VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='INSURANCE',
                    file=File(f, name=os.path.basename(insurance_path)),
                    created_by=request.user,
                    issue_date=timezone.now().date(),
                    expiry_date=insurance_expiry
                )
                print(f'[DEBUG] Создан документ: {doc}, expiry_date={doc.expiry_date}')
                create_expiry_notification(vehicle, 'INSURANCE', doc.expiry_date)
        elif 'insurance' in request.FILES:
            doc = VehicleDocument.objects.create(
                vehicle=vehicle,
                document_type='INSURANCE',
                file=request.FILES['insurance'],
                created_by=request.user,
                issue_date=timezone.now().date(),
                expiry_date=insurance_expiry
            )
            print(f'[DEBUG] Создан документ: {doc}, expiry_date={doc.expiry_date}')
            create_expiry_notification(vehicle, 'INSURANCE', doc.expiry_date)

        # --- Техосмотр ---
        technical_inspection_expiry = request.POST.get('technical_inspection_expiry_date') or None
        if 'technical_inspection' in request.FILES:
            doc = VehicleDocument.objects.create(
                vehicle=vehicle,
                document_type='TECHNICAL_INSPECTION',
                file=request.FILES['technical_inspection'],
                created_by=request.user,
                issue_date=timezone.now().date(),
                expiry_date=technical_inspection_expiry
            )
            print(f'[DEBUG] Создан документ: {doc}, expiry_date={doc.expiry_date}')
            create_expiry_notification(vehicle, 'TECHNICAL_INSPECTION', doc.expiry_date)

        # --- Дополнительные документы ---
        additional_documents_paths = request.POST.get('additional_documents_paths', '')
        for path in filter(None, additional_documents_paths.split(',')):
            with default_storage.open(path, 'rb') as f:
                VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='OTHER',
                    file=File(f, name=os.path.basename(path)),
                    created_by=request.user,
                    issue_date=timezone.now().date()
                )
        for doc in request.FILES.getlist('additional_documents'):
            VehicleDocument.objects.create(
                vehicle=vehicle,
                document_type='OTHER',
                file=doc,
                created_by=request.user,
                issue_date=timezone.now().date()
            )

        # --- Уведомления ---
        print('[DEBUG] Перед созданием уведомления о транспорте', request.user, vehicle)
        from core.models import Notification
        Notification.create_vehicle_notification(request.user, vehicle)
        if vehicle.driver and vehicle.driver != request.user:
            Notification.create_vehicle_notification(vehicle.driver, vehicle)
        messages.success(request, 'Транспорт успешно добавлен')
        return redirect('core:trucks')

        # --- После создания всех документов ---
        from django.db import models
        # from django.utils import timezone  # Удаляю этот импорт, чтобы не было ошибки
        notify_days = [30, 14, 7, 1]
        today = timezone.now().date()
        recipients = User.objects.filter(is_active=True).filter(
            models.Q(role__in=['DIRECTOR', 'SUPERADMIN']) | models.Q(is_superuser=True)
        ).distinct()
        for doc in VehicleDocument.objects.filter(vehicle=vehicle, expiry_date__isnull=False):
            if not doc.expiry_date:
                continue
            days_left = (doc.expiry_date - today).days
            print(f'[DEBUG] Документ: {doc.document_type}, expiry_date: {doc.expiry_date}, days_left: {days_left}')
            if 0 <= days_left <= 30:
                doc_type = dict(doc.DOCUMENT_TYPE_CHOICES).get(doc.document_type, doc.document_type)
                for user in recipients:
                    if not Notification.objects.filter(user=user, type=Notification.Type.DOCUMENT, message__contains=doc.expiry_date.strftime('%d.%m.%Y')).exists():
                        print(f'[DEBUG] Создаю уведомление для {user.email} по документу {doc_type} ({doc.expiry_date})')
                        Notification.objects.create(
                            user=user,
                            type=Notification.Type.DOCUMENT,
                            title='Скоро истекает срок документа',
                            message=f'У {vehicle.brand} {vehicle.model} ({vehicle.number}) истекает срок: {doc_type} — {doc.expiry_date.strftime('%d.%m.%Y')}',
                            link=f'/trucks/{vehicle.id}/'
                        )

        vehicle.refresh_from_db()
        notify_days = [30, 14, 7, 1]
        today = timezone.now().date()
        recipients = User.objects.filter(is_active=True).filter(
            models.Q(role__in=['DIRECTOR', 'SUPERADMIN']) | models.Q(is_superuser=True)
        ).distinct()
        for doc in VehicleDocument.objects.filter(vehicle=vehicle, expiry_date__isnull=False):
            if not doc.expiry_date:
                continue
            days_left = (doc.expiry_date - today).days
            print(f'[DEBUG] Документ: {doc.document_type}, expiry_date: {doc.expiry_date}, days_left: {days_left}')
            if 0 <= days_left <= 30:
                doc_type = dict(doc.DOCUMENT_TYPE_CHOICES).get(doc.document_type, doc.document_type)
                for user in recipients:
                    if not Notification.objects.filter(user=user, type=Notification.Type.DOCUMENT, message__contains=doc.expiry_date.strftime('%d.%m.%Y')).exists():
                        print(f'[DEBUG] Создаю уведомление для {user.email} по документу {doc_type} ({doc.expiry_date})')
                        Notification.objects.create(
                            user=user,
                            type=Notification.Type.DOCUMENT,
                            title='Скоро истекает срок документа',
                            message=f'У {vehicle.brand} {vehicle.model} ({vehicle.number}) истекает срок: {doc_type} — {doc.expiry_date.strftime('%d.%m.%Y')}',
                            link=f'/trucks/{vehicle.id}/'
                        )

        return redirect('core:trucks')


class VehicleUpdateView(LoginRequiredMixin, View):
    template_name = 'core/vehicle_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')

        # Проверяем существование транспорта
        from logistics.models import Vehicle
        try:
            self.vehicle = Vehicle.objects.get(id=kwargs['pk'])
        except Vehicle.DoesNotExist:
            messages.error(request, 'Транспорт не найден')
            return redirect('core:vehicles')

        # Проверяем права доступа
        if not request.user.role in [
                'DIRECTOR', 'SUPERADMIN', 'TECH'] and not request.user.is_superuser:
            messages.error(
                request, 'У вас нет прав для редактирования транспорта')
            return redirect('core:vehicles')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        # Получаем список водителей для поля выбора
        User = get_user_model()
        drivers = User.objects.filter(is_active=True, role='DRIVER')

        # Создаем форму и заполняем её данными из существующего транспорта
        from django import forms

        class VehicleForm(forms.Form):
            # Основная информация
            number = forms.CharField(
                max_length=20,
                required=True,
                initial=self.vehicle.number)
            vehicle_type = forms.ChoiceField(choices=[
                ('CAR', 'Легковой'),
                ('TRUCK', 'Грузовой'),
                ('SPECIAL', 'Спецтехника')
            ], required=True, initial=self.vehicle.vehicle_type)
            brand = forms.CharField(
                max_length=100,
                required=True,
                initial=self.vehicle.brand)
            model = forms.CharField(
                max_length=100,
                required=True,
                initial=self.vehicle.model)
            year = forms.IntegerField(
                required=True,
                min_value=1900,
                max_value=2100,
                initial=self.vehicle.year)
            color = forms.CharField(
                max_length=50,
                required=False,
                initial=self.vehicle.color)
            status = forms.ChoiceField(choices=[
                ('ACTIVE', 'Активен'),
                ('INACTIVE', 'Неактивен'),
                ('MAINTENANCE', 'На обслуживании')
            ], required=True, initial=self.vehicle.status)
            driver = forms.ModelChoiceField(
                queryset=drivers, required=False, initial=self.vehicle.driver)
            description = forms.CharField(
                widget=forms.Textarea,
                required=False,
                initial=self.vehicle.description)

            # Технические характеристики
            vin_number = forms.CharField(
                max_length=50,
                required=False,
                initial=self.vehicle.vin_number)
            engine_number = forms.CharField(
                max_length=50,
                required=False,
                initial=self.vehicle.engine_number)
            chassis_number = forms.CharField(
                max_length=50, required=False, initial=self.vehicle.chassis_number)
            engine_capacity = forms.FloatField(
                required=False, initial=self.vehicle.engine_capacity)
            fuel_type = forms.ChoiceField(choices=[
                ('', 'Не указан'),
                ('DIESEL', 'Дизель'),
                ('PETROL', 'Бензин'),
                ('GAS', 'Газ'),
                ('HYBRID', 'Гибрид'),
                ('ELECTRIC', 'Электро')
            ], required=False, initial=self.vehicle.fuel_type)
            fuel_consumption = forms.FloatField(
                required=False, initial=self.vehicle.fuel_consumption)
            length = forms.FloatField(
                required=False, initial=self.vehicle.length)
            width = forms.FloatField(
                required=False, initial=self.vehicle.width)
            height = forms.FloatField(
                required=False, initial=self.vehicle.height)
            max_weight = forms.IntegerField(
                required=False, initial=self.vehicle.max_weight)
            cargo_capacity = forms.IntegerField(
                required=False, initial=self.vehicle.cargo_capacity)

            # Файловые поля обрабатываются вручную через request.FILES

        form = VehicleForm()

        context = {
            'form': form,
            'vehicle': self.vehicle,
            'drivers': drivers,
            'title': f'Редактирование {self.vehicle.brand} {self.vehicle.model} ({self.vehicle.number})',
            'action': 'update',
            'active_page': 'vehicles'
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        from logistics.models import Vehicle, VehiclePhoto, VehicleDocument
        from django import forms
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import os

        User = get_user_model()
        drivers = User.objects.filter(is_active=True, role='DRIVER')

        class VehicleForm(forms.Form):
            # Основная информация
            number = forms.CharField(max_length=20, required=True)
            vehicle_type = forms.ChoiceField(choices=[
                ('CAR', 'Легковой'),
                ('TRUCK', 'Грузовой'),
                ('SPECIAL', 'Спецтехника')
            ], required=True)
            brand = forms.CharField(max_length=100, required=True)
            model = forms.CharField(max_length=100, required=True)
            year = forms.IntegerField(
                required=True, min_value=1900, max_value=2100)
            color = forms.CharField(max_length=50, required=False)
            status = forms.ChoiceField(choices=[
                ('ACTIVE', 'Активен'),
                ('INACTIVE', 'Неактивен'),
                ('MAINTENANCE', 'На обслуживании')
            ], required=True)
            driver = forms.ModelChoiceField(queryset=drivers, required=False)
            description = forms.CharField(
                widget=forms.Textarea, required=False)

            # Технические характеристики
            vin_number = forms.CharField(max_length=50, required=False)
            engine_number = forms.CharField(max_length=50, required=False)
            chassis_number = forms.CharField(max_length=50, required=False)
            engine_capacity = forms.FloatField(required=False)
            fuel_type = forms.ChoiceField(choices=[
                ('', 'Не указан'),
                ('DIESEL', 'Дизель'),
                ('PETROL', 'Бензин'),
                ('GAS', 'Газ'),
                ('HYBRID', 'Гибрид'),
                ('ELECTRIC', 'Электро')
            ], required=False)
            fuel_consumption = forms.FloatField(required=False)
            length = forms.FloatField(required=False)
            width = forms.FloatField(required=False)
            height = forms.FloatField(required=False)
            max_weight = forms.IntegerField(required=False)
            cargo_capacity = forms.IntegerField(required=False)

            # Файловые поля обрабатываются вручную через request.FILES

        form = VehicleForm(request.POST, request.FILES)

        # Проверяем, не пришел ли запрос на удаление фото или документа
        delete_photo_id = request.POST.get('delete_photo')
        if delete_photo_id:
            try:
                photo = VehiclePhoto.objects.get(
                    id=delete_photo_id, vehicle=self.vehicle)
                photo.delete()
                messages.success(request, 'Фотография успешно удалена')
                return redirect('core:vehicle-edit', pk=pk)
            except VehiclePhoto.DoesNotExist:
                pass

        delete_document_id = request.POST.get('delete_document')
        if delete_document_id:
            try:
                document = VehicleDocument.objects.get(
                    id=delete_document_id, vehicle=self.vehicle)
                document.delete()
                messages.success(request, 'Документ успешно удален')
                return redirect('core:vehicle-edit', pk=pk)
            except VehicleDocument.DoesNotExist:
                pass

        if form.is_valid():
            number = form.cleaned_data['number']
            vehicle_type = form.cleaned_data['vehicle_type']
            brand = form.cleaned_data['brand']
            model = form.cleaned_data['model']
            year = form.cleaned_data['year']
            color = form.cleaned_data['color']
            status = form.cleaned_data['status']
            driver = form.cleaned_data['driver']
            description = form.cleaned_data['description']

            # Технические параметры
            vin_number = form.cleaned_data['vin_number']
            engine_number = form.cleaned_data['engine_number']
            chassis_number = form.cleaned_data['chassis_number']
            engine_capacity = form.cleaned_data['engine_capacity']
            fuel_type = form.cleaned_data['fuel_type']
            fuel_consumption = form.cleaned_data['fuel_consumption']
            length = form.cleaned_data['length']
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            max_weight = form.cleaned_data['max_weight']
            cargo_capacity = form.cleaned_data['cargo_capacity']

            # Проверка уникальности номера (исключая текущий транспорт)
            if Vehicle.objects.filter(number=number).exclude(id=pk).exists():
                form.add_error(
                    'number', 'Транспорт с таким номером уже существует')
                context = {
                    'form': form,
                    'vehicle': self.vehicle,
                    'drivers': drivers,
                    'title': f'Редактирование {self.vehicle.brand} {self.vehicle.model} ({self.vehicle.number})',
                    'action': 'update',
                    'active_page': 'vehicles'
                }
                return render(request, self.template_name, context)

            # Обновляем транспорт
            vehicle = self.vehicle
            vehicle.number = number
            vehicle.vehicle_type = vehicle_type
            vehicle.brand = brand
            vehicle.model = model
            vehicle.year = year
            vehicle.color = color
            vehicle.status = status
            vehicle.description = description
            vehicle.vin_number = vin_number
            vehicle.engine_number = engine_number
            vehicle.chassis_number = chassis_number
            vehicle.engine_capacity = engine_capacity
            vehicle.fuel_type = fuel_type
            vehicle.fuel_consumption = fuel_consumption
            vehicle.length = length
            vehicle.width = width
            vehicle.height = height
            vehicle.max_weight = max_weight
            vehicle.cargo_capacity = cargo_capacity
            vehicle.updated_at = timezone.now()

            # Обновляем водителя
            old_driver = vehicle.driver
            if driver:
                vehicle.driver = driver
            else:
                vehicle.driver = None

            vehicle.save()

            # Обрабатываем основное фото
            main_photo = form.cleaned_data.get('main_photo')
            if main_photo:
                # Если уже есть фото, заменяем его
                if vehicle.main_photo:
                    # При необходимости, можно удалить старое фото
                    # default_storage.delete(vehicle.main_photo.path)
                    pass

                vehicle.main_photo = main_photo
                vehicle.save()

            # Обрабатываем дополнительные фотографии
            additional_photos = request.FILES.getlist('additional_photos')
            if additional_photos:
                for photo_file in additional_photos:
                    VehiclePhoto.objects.create(
                        vehicle=vehicle,
                        photo=photo_file
                    )

            # Обрабатываем документы
            technical_passport = form.cleaned_data.get('technical_passport')
            if technical_passport:
                # Если уже есть документ, заменяем его
                if vehicle.technical_passport:
                    # При необходимости, можно удалить старый документ
                    # default_storage.delete(vehicle.technical_passport.path)
                    pass

                vehicle.technical_passport = technical_passport
                vehicle.save()

            insurance = form.cleaned_data.get('insurance')
            if insurance:
                # Если уже есть документ, заменяем его
                if vehicle.insurance:
                    # При необходимости, можно удалить старый документ
                    # default_storage.delete(vehicle.insurance.path)
                    pass

                vehicle.insurance = insurance
                vehicle.save()

            # Обрабатываем техосмотр
            technical_inspection = request.FILES.get('technical_inspection')
            if technical_inspection:
                VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='TECHNICAL_INSPECTION',
                    file=technical_inspection,
                    issue_date=timezone.now().date()
                )

            # Обрабатываем регистрацию
            registration = request.FILES.get('registration')
            if registration:
                VehicleDocument.objects.create(
                    vehicle=vehicle,
                    document_type='REGISTRATION',
                    file=registration,
                    issue_date=timezone.now().date()
                )

            # Обрабатываем дополнительные документы
            additional_documents = request.FILES.getlist('additional_documents')
            if additional_documents:
                for doc_file in additional_documents:
                    VehicleDocument.objects.create(
                        vehicle=vehicle,
                        document_type='OTHER',
                        file=doc_file,
                        issue_date=timezone.now().date()
                    )

            messages.success(request, f'Транспорт {number} успешно обновлен')
            return redirect('core:vehicles')

        # Если форма не прошла валидацию
        context = {
            'form': form,
            'vehicle': self.vehicle,
            'drivers': drivers,
            'title': f'Редактирование {self.vehicle.brand} {self.vehicle.model} ({self.vehicle.number})',
            'action': 'update',
            'active_page': 'vehicles'
        }
        return render(request, self.template_name, context)


class VehicleArchiveView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')

        # Проверяем существование транспорта
        from logistics.models import Vehicle
        try:
            self.vehicle = Vehicle.objects.get(id=kwargs['pk'])
        except Vehicle.DoesNotExist:
            messages.error(request, 'Транспорт не найден')
            return redirect('core:vehicles')

        # Проверяем права доступа
        if not request.user.role in [
                'DIRECTOR', 'SUPERADMIN', 'TECH'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для архивации транспорта')
            return redirect('core:vehicles')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        # Архивация транспорта - удаляем связь с водителем
        if self.vehicle.driver:
            old_driver = self.vehicle.driver
            self.vehicle.driver = None
            self.vehicle.save()

            # Уведомляем водителя
            Notification.create_system_notification(
                old_driver,
                'Транспорт отозван',
                f'Транспорт {
                    self.vehicle.brand} {
                    self.vehicle.model} ({
                    self.vehicle.number}) отозван'
            )

        messages.success(request, 'Транспорт отвязан от водителя')
        return redirect('core:vehicles')


def logout_view(request):
    logout(request)
    return redirect('login')


class MapView(TemplateView):
    template_name = 'core/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'map'

        # Проверяем, является ли пользователь водителем
        is_driver = False
        can_see_all_employees = False

        if self.request.user.is_authenticated:
            is_driver = self.request.user.role == 'DRIVER'
            can_see_all_employees = self.request.user.role in [
                'ADMIN', 'DIRECTOR', 'DISPATCHER']

        context['is_driver'] = is_driver
        context['can_see_all_employees'] = can_see_all_employees

        return context

    # Убираем требование аутентификации, чтобы страница была доступна всем
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'core/profile_edit.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user

        # Обновление основной информации
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.position = request.POST.get('position', user.position)

        # Обработка фото
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()

        messages.success(request, 'Профиль успешно обновлен')
        return redirect('core:profile')


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'core/change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Проверка правильности текущего пароля
        if not user.check_password(old_password):
            messages.error(request, 'Неверный текущий пароль')
            return render(request, self.template_name)

        # Проверка совпадения новых паролей
        if new_password1 != new_password2:
            messages.error(request, 'Новые пароли не совпадают')
            return render(request, self.template_name)

        # Проверка сложности пароля (можно добавить дополнительные правила)
        if len(new_password1) < 8:
            messages.error(
                request, 'Пароль должен содержать не менее 8 символов')
            return render(request, self.template_name)

        # Смена пароля
        user.set_password(new_password1)
        user.save()

        # Обновление сессии для предотвращения выхода пользователя
        update_session_auth_hash(request, user)

        messages.success(request, 'Пароль успешно изменен')
        return redirect('core:profile')


class TrucksView(LoginRequiredMixin, TemplateView):
    template_name = 'core/trucks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # помечаем активную страницу и передаем список грузовиков
        context['active_page'] = 'trucks'
        context['trucks'] = Vehicle.objects.all().order_by('brand', 'model')
        return context


class TruckDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'core/truck_detail.html'
    context_object_name = 'truck'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # помечаем активную страницу
        context['active_page'] = 'trucks'
        return context


class VehicleDeleteView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.role in [
                'DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            if request.method == 'DELETE':
                return JsonResponse({'error': 'У вас нет прав для удаления транспорта'}, status=403)
            messages.error(request, 'У вас нет прав для удаления транспорта')
            return redirect('core:trucks')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, pk):
        """Обработка AJAX DELETE запроса"""
        try:
            vehicle = Vehicle.objects.get(id=pk)
            
            # Дополнительные проверки безопасности
            if request.user.role != 'SUPERADMIN' and not request.user.is_superuser:
                return JsonResponse({'error': 'Недостаточно прав для удаления транспорта'}, status=403)
            
            # Проверяем, есть ли связанные задачи
            if hasattr(vehicle, 'task_set') and vehicle.task_set.filter(status__in=['NEW', 'IN_PROGRESS']).exists():
                return JsonResponse({'error': 'Нельзя удалить транспорт с активными задачами'}, status=400)
            
            vehicle_info = f"{vehicle.brand} {vehicle.model} ({vehicle.number})"
            vehicle.delete()
            
            # Логирование
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Vehicle deleted by {request.user.email}: {vehicle_info}")
            
            return JsonResponse({'success': True, 'message': f'Транспорт {vehicle_info} успешно удален'})
            
        except Vehicle.DoesNotExist:
            return JsonResponse({'error': 'Транспорт не найден'}, status=404)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error deleting vehicle by {request.user.email}: {str(e)}")
            return JsonResponse({'error': f'Ошибка при удалении транспорта: {str(e)}'}, status=500)

    def post(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
            number = vehicle.number
            vehicle.delete()
            messages.success(request, f'Транспорт {number} успешно удален')
        except Vehicle.DoesNotExist:
            messages.error(request, 'Транспорт не найден')
        except Exception as e:
            messages.error(
                request,
                f'Ошибка при удалении транспорта: {
                    str(e)}')

        return redirect('core:trucks')


@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(View):
    def post(self, request):
        if not request.FILES:
            return JsonResponse({'error': 'Файл не предоставлен'}, status=400)
        file = list(request.FILES.values())[0]
        file_type = file.content_type
        allowed_types = getattr(settings, 'ALLOWED_DOCUMENT_TYPES', []) + getattr(settings, 'ALLOWED_IMAGE_TYPES', [])
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)
        if file_type not in allowed_types:
            return JsonResponse({'error': 'Недопустимый тип файла'}, status=400)
        if file.size > max_size:
            return JsonResponse({'error': f'Размер файла превышает {max_size // (1024*1024)}MB'}, status=400)
        ext = os.path.splitext(file.name)[1]
        filename = f"{os.urandom(8).hex()}{ext}"
        if file_type in getattr(settings, 'ALLOWED_IMAGE_TYPES', []):
            upload_dir = 'uploads/images/'
        else:
            upload_dir = 'uploads/documents/'
        path = os.path.join(upload_dir, filename)
        saved_path = default_storage.save(path, ContentFile(file.read()))
        return JsonResponse({'path': saved_path, 'url': default_storage.url(saved_path)})


class NotificationManualForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Получатель')
    type = forms.ChoiceField(choices=Notification.Type.choices, label='Тип')
    title = forms.CharField(max_length=100, label='Заголовок')
    message = forms.CharField(widget=forms.Textarea, label='Текст')
    link = forms.CharField(max_length=255, label='Ссылка', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full rounded-lg border-gray-300'
        self.fields['user'].widget.attrs['placeholder'] = 'Выберите пользователя'
        self.fields['type'].widget.attrs['placeholder'] = 'Тип'
        self.fields['title'].widget.attrs['placeholder'] = 'Заголовок'
        self.fields['message'].widget.attrs['placeholder'] = 'Текст уведомления'
        self.fields['message'].widget.attrs['rows'] = 4
        self.fields['link'].widget.attrs['placeholder'] = 'https://...'

class NotificationManualCreateView(LoginRequiredMixin, FormView):
    template_name = 'core/notification_manual_create.html'
    form_class = NotificationManualForm
    success_url = '/dashboard/notifications/'

    def form_valid(self, form):
        Notification.objects.create(
            user=form.cleaned_data['user'],
            type=form.cleaned_data['type'],
            title=form.cleaned_data['title'],
            message=form.cleaned_data['message'],
            link=form.cleaned_data['link']
        )
        messages.success(self.request, 'Уведомление отправлено!')
        return super().form_valid(form)

def create_expiry_notification(vehicle, document_type, expiry_date):
    print('[DEBUG] create_expiry_notification вызвана', vehicle, document_type, expiry_date)
    from django.db import models
    from core.models import Notification
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from logistics.models import VehicleDocument
    from django.utils import timezone
    from datetime import datetime, date
    if not expiry_date:
        print('[DEBUG] expiry_date отсутствует, уведомление не будет создано')
        return
    print('[DEBUG] expiry_date type:', type(expiry_date))
    if isinstance(expiry_date, str):
        try:
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            print('[DEBUG] expiry_date преобразована из строки:', expiry_date)
        except Exception as e:
            print('[DEBUG] Ошибка преобразования expiry_date:', e)
            return
    today = timezone.now().date()
    days_left = (expiry_date - today).days
    print(f'[DEBUG] today={today}, expiry_date={expiry_date}, days_left={days_left}')
    if 0 <= days_left <= 30:
        recipients = User.objects.filter(is_active=True).filter(
            models.Q(role__in=['DIRECTOR', 'SUPERADMIN']) | models.Q(is_superuser=True)
        ).distinct()
        print('[DEBUG] Найдено реципиентов:', recipients.count())
        for user in recipients:
            print(f'[DEBUG] Реципиент: id={user.id}, username={user.username}, email={user.email}, role={getattr(user, "role", None)}, is_superuser={getattr(user, "is_superuser", None)}')
        doc_type = dict(VehicleDocument.DOCUMENT_TYPE_CHOICES).get(document_type, document_type)
        for user in recipients:
            exists = Notification.objects.filter(user=user, type=Notification.Type.DOCUMENT, message__contains=expiry_date.strftime('%d.%m.%Y')).exists()
            print(f'[DEBUG] Проверяю уведомление для {user.email}: exists={exists}')
            if not exists:
                Notification.objects.create(
                    user=user,
                    type=Notification.Type.DOCUMENT,
                    title='Скоро истекает срок документа',
                    message=f'У {vehicle.brand} {vehicle.model} ({vehicle.number}) истекает срок: {doc_type} — {expiry_date.strftime('%d.%m.%Y')}',
                    link=f'/trucks/{vehicle.id}/'
                )
                print(f'[DEBUG] Уведомление создано для {user.email}')
    else:
        print('[DEBUG] days_left вне диапазона 0-30, уведомление не создается')


class TestEmployeesView(View):
    """Временное представление для отладки проблемы с отображением сотрудников"""
    
    def get(self, request):
        from django.http import HttpResponse
        from accounts.models import User
        
        html = "<h1>Тест сотрудников</h1>"
        html += f"<p>Пользователь: {request.user if request.user.is_authenticated else 'Не авторизован'}</p>"
        
        employees = User.objects.filter(is_active=True).order_by('last_name', 'first_name')
        
        html += f"<p>Всего активных пользователей: {employees.count()}</p>"
        html += "<hr><h2>Список всех активных пользователей:</h2>"
        
        for emp in employees:
            html += f"<div style='border: 1px solid #ccc; margin: 5px; padding: 10px;'>"
            html += f"<strong>ID:</strong> {emp.id}<br>"
            html += f"<strong>Username:</strong> {emp.username}<br>"
            html += f"<strong>Имя:</strong> '{emp.first_name}'<br>"
            html += f"<strong>Фамилия:</strong> '{emp.last_name}'<br>"
            html += f"<strong>Email:</strong> {emp.email}<br>"
            html += f"<strong>get_full_name():</strong> '{emp.get_full_name()}'<br>"
            html += f"<strong>Роль:</strong> {emp.role}<br>"
            html += f"<strong>Должность:</strong> {emp.position}<br>"
            html += f"<strong>Активен:</strong> {emp.is_active}<br>"
            html += f"<strong>Создан:</strong> {emp.date_joined}<br>"
            html += f"</div>"
        
        html += "<hr><h2>Фильтр как в EmployeesView:</h2>"
        employees_filtered = User.objects.filter(is_active=True).order_by('last_name', 'first_name')
        html += f"<p>Результат фильтра: {employees_filtered.count()} сотрудников</p>"
        
        return HttpResponse(html)

@csrf_exempt
def public_notifications_test(request):
    """Простая тестовая функция для проверки публичного API"""
    try:
        notifications = Notification.objects.all().order_by('-created_at')[:10]
        data = []
        for notif in notifications:
            data.append({
                'id': notif.id,
                'title': notif.title,
                'message': notif.message,
                'type': notif.type,
                'created_at': notif.created_at.isoformat(),
                'user': notif.user.username
            })
        
        return JsonResponse({
            'count': len(data),
            'results': data,
            'debug': f'Total notifications in DB: {Notification.objects.count()}'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'debug': 'Exception occurred'
        })

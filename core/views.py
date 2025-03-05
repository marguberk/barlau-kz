from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, View, CreateView, UpdateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.conf import settings
from django.contrib.auth import get_user_model
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

from logistics.models import Task, Vehicle
from .models import Notification, Waybill
from logistics.models import Expense
from .serializers import NotificationSerializer, WaybillSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserPhotoSerializer

User = get_user_model()

class IsDirectorOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.role in ['DIRECTOR', 'SUPERADMIN'] or request.user.is_superuser

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsDirectorOrSuperAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
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
        if not request.user.role in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
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
        if not request.user.role in ['DIRECTOR', 'SUPERADMIN']:
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
            worksheet.write(row, 7, 'Активен' if user.is_active else 'Неактивен')
            worksheet.write(row, 8, user.date_joined.strftime('%d.%m.%Y'), date_format)
            if user.last_login:
                worksheet.write(row, 9, user.last_login.strftime('%d.%m.%Y'), date_format)
        
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

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Отметить все уведомления как прочитанные"""
        self.get_queryset().update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Отметить уведомление как прочитанное"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Получить количество непрочитанных уведомлений"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'count': count})

class HomeView(TemplateView):
    template_name = 'core/home_mobile.html'
    
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
                vehicles_count = Vehicle.objects.filter(
                    driver=self.request.user
                ).count()
            elif self.request.user.role in ['DIRECTOR', 'SUPERADMIN']:
                tasks_count = Task.objects.filter(
                    status__in=['NEW', 'IN_PROGRESS']
                ).count()
                vehicles_count = Vehicle.objects.filter(
                    driver__isnull=False
                ).count()
            else:
                tasks_count = Task.objects.filter(
                    created_by=self.request.user,
                    status__in=['NEW', 'IN_PROGRESS']
                ).count()
                vehicles_count = Vehicle.objects.filter(
                    driver__isnull=False
                ).count()
            
            context['tasks_count'] = tasks_count
            context['vehicles_count'] = vehicles_count
            
            # Получаем последние задачи
            if self.request.user.role == 'DRIVER':
                tasks = Task.objects.filter(assigned_to=self.request.user)
            elif self.request.user.role in ['DIRECTOR', 'SUPERADMIN']:
                tasks = Task.objects.all()
            else:
                tasks = Task.objects.filter(created_by=self.request.user)
                
            context['recent_tasks'] = tasks.select_related(
                'assigned_to', 'vehicle'
            ).order_by('-created_at')[:5]
            
            # Получаем количество непрочитанных уведомлений
            context['unread_notifications'] = Notification.objects.filter(
                user=self.request.user,
                is_read=False
            ).count()
        
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
            if self.request.user.role in ['DIRECTOR', 'SUPERADMIN', 'ACCOUNTANT']:
                quick_actions.extend([
                    {
                        'icon': 'plus-circle',
                        'name': 'Новая задача',
                        'description': 'Создать новую задачу',
                        'url': '/tasks/create/'
                    },
                    {
                        'icon': 'user-plus',
                        'name': 'Добавить сотрудника',
                        'description': 'Зарегистрировать нового сотрудника',
                        'url': '/employees/create/'
                    }
                ])
            
            if self.request.user.role == 'DRIVER':
                quick_actions.extend([
                    {
                        'icon': 'location-arrow',
                        'name': 'Обновить локацию',
                        'description': 'Обновить текущее местоположение',
                        'url': '/map/update-location/'
                    },
                    {
                        'icon': 'file-signature',
                        'name': 'Новый КАТ',
                        'description': 'Создать путевой лист',
                        'url': '/waybills/create/'
                    }
                ])
            
            if self.request.user.role in ['ACCOUNTANT', 'SUPPLIER']:
                quick_actions.extend([
                    {
                        'icon': 'receipt',
                        'name': 'Новый расход',
                        'description': 'Добавить новый расход',
                        'url': '/expenses/create/'
                    },
                    {
                        'icon': 'file-invoice',
                        'name': 'Отчет',
                        'description': 'Сформировать финансовый отчет',
                        'url': '/finance/report/'
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
        context['in_progress_tasks_count'] = tasks.filter(status='IN_PROGRESS').count()
        context['completed_tasks_count'] = tasks.filter(status='COMPLETED').count()

        # Статистика по путевым листам для водителей
        if user.role == 'DRIVER':
            today = timezone.now().date()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)
            
            waybills = Waybill.objects.filter(driver=user)
            context['waybills_count'] = waybills.count()
            context['today_waybills_count'] = waybills.filter(date=today).count()
            context['week_waybills_count'] = waybills.filter(date__gte=week_ago).count()
            context['month_waybills_count'] = waybills.filter(date__gte=month_ago).count()

        # Статистика по расходам для бухгалтеров и снабженцев
        if user.role in ['ACCOUNTANT', 'SUPPLIER']:
            expenses = Expense.objects.filter(created_by=user)
            context['expenses_count'] = expenses.count()
            context['pending_expenses_count'] = expenses.filter(status='PENDING').count()
            context['approved_expenses_count'] = expenses.filter(status='APPROVED').count()
            context['rejected_expenses_count'] = expenses.filter(status='REJECTED').count()

        # Статистика по уведомлениям
        notifications = Notification.objects.filter(user=user)
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        context['notifications_count'] = notifications.count()
        context['unread_notifications_count'] = notifications.filter(is_read=False).count()
        context['today_notifications_count'] = notifications.filter(created_at__gte=today_start).count()

        # Последние действия
        recent_actions = []
        
        # Добавляем последние задачи
        for task in tasks.order_by('-updated_at')[:5]:
            action = {
                'icon': 'tasks',
                'description': f'Задача "{task.title}" изменила статус на {task.get_status_display()}',
                'timestamp': task.updated_at
            }
            recent_actions.append(action)
        
        # Добавляем последние путевые листы для водителей
        if user.role == 'DRIVER':
            for waybill in Waybill.objects.filter(driver=user).order_by('-created_at')[:5]:
                action = {
                    'icon': 'file-alt',
                    'description': f'Создан путевой лист №{waybill.number}',
                    'timestamp': waybill.created_at
                }
                recent_actions.append(action)
        
        # Добавляем последние расходы для бухгалтеров и снабженцев
        if user.role in ['ACCOUNTANT', 'SUPPLIER']:
            for expense in Expense.objects.filter(created_by=user).order_by('-created_at')[:5]:
                action = {
                    'icon': 'money-bill-wave',
                    'description': f'Добавлен расход на сумму {expense.amount} тг',
                    'timestamp': expense.created_at
                }
                recent_actions.append(action)
        
        # Сортируем все действия по времени
        recent_actions.sort(key=lambda x: x['timestamp'], reverse=True)
        context['recent_actions'] = recent_actions[:10]  # Оставляем только 10 последних действий

        return context

class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/notifications.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unread_notifications'] = Notification.objects.filter(
            user=self.request.user,
            is_read=False
        ).count()
        return context

class VehiclesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/vehicles.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'vehicles'
        context['unread_notifications'] = Notification.objects.filter(
            user=self.request.user,
            is_read=False
        ).count()
        
        # Добавляем флаг, может ли пользователь управлять транспортом
        context['can_manage_vehicles'] = self.request.user.role in ['DIRECTOR', 'SUPERADMIN']
        
        return context

class TasksView(LoginRequiredMixin, TemplateView):
    template_name = 'core/tasks.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'tasks'
        return context

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
        if not request.user.role in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            return HttpResponseForbidden("У вас нет прав для просмотра этой страницы")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'employees'
        context['can_manage_employees'] = self.request.user.role in ['DIRECTOR', 'SUPERADMIN'] or self.request.user.is_superuser
        return context

class WaybillViewSet(viewsets.ModelViewSet):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle', 'driver', 'date']
    search_fields = ['number', 'departure_point', 'destination_point', 'cargo_description']
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
            response = HttpResponse(output.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="waybill-{waybill.number}.pdf"'
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
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)
        
        # Подготавливаем ответ
        output.seek(0)
        filename = f"waybills_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
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
            response = HttpResponse(output.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="waybill-{waybill.number}.pdf"'
            return response

class WaybillCreateView(LoginRequiredMixin, CreateView):
    model = Waybill
    template_name = 'core/waybill_form.html'
    fields = ['date', 'vehicle', 'driver', 'departure_point', 'destination_point', 
              'cargo_description', 'cargo_weight']
    success_url = reverse_lazy('core:waybills')
    
    def dispatch(self, request, *args, **kwargs):
        # Проверяем права доступа
        if not (request.user.is_superuser or request.user.role in ['DIRECTOR', 'SUPERADMIN', 'DRIVER']):
            return HttpResponseForbidden('У вас нет прав для создания путевых листов')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ограничиваем выбор водителей только водителями
        form.fields['driver'].queryset = User.objects.filter(role='DRIVER', is_active=True)
        # Если пользователь - водитель, устанавливаем его как водителя по умолчанию
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
        waybill = self.get_object()
        # Проверяем права доступа
        if not (request.user.is_superuser or request.user.role in ['DIRECTOR', 'SUPERADMIN'] or 
                (request.user.role == 'DRIVER' and request.user == waybill.driver)):
            return HttpResponseForbidden('У вас нет прав для редактирования этого путевого листа')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ограничиваем выбор водителей только водителями
        form.fields['driver'].queryset = User.objects.filter(role='DRIVER', is_active=True)
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
        
        if request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для удаления путевых листов')
            return redirect('core:waybills')
        
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, pk):
        waybill = get_object_or_404(Waybill, pk=pk)
        waybill_number = waybill.number
        
        try:
            waybill.delete()
            messages.success(request, f'Путевой лист №{waybill_number} успешно удален')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении путевого листа: {str(e)}')
        
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
        response['Content-Disposition'] = f'attachment; filename="{user.get_full_name()}_resume.pdf"'
        
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
        if not request.user.role in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            return JsonResponse({'error': 'У вас нет прав для выполнения этого действия'}, status=403)
            
        employee = get_object_or_404(User, pk=pk)
        
        if 'photo' in request.FILES:
            photo = request.FILES['photo']
            # Проверка типа файла
            if not photo.content_type.startswith('image/'):
                return JsonResponse({'error': 'Загружаемый файл должен быть изображением'}, status=400)
                
            # Проверка размера файла (максимум 5 МБ)
            if photo.size > 5 * 1024 * 1024:
                return JsonResponse({'error': 'Размер файла не должен превышать 5 МБ'}, status=400)
                
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
        if not request.user.role in ['DIRECTOR', 'ACCOUNTANT', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для просмотра списка сотрудников')
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
        if not request.user.is_authenticated or request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для добавления сотрудников')
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
        if not request.user.is_authenticated or request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для добавления сотрудников')
            return redirect('core:index')
        
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
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Пользователь с таким email уже существует'
        
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
        
        # Генерация случайного пароля
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            position=position,
            role=role
        )
        
        # Дополнительные поля из формы
        user.desired_salary = request.POST.get('desired_salary', '')
        user.age = request.POST.get('age', '')
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
        
        messages.success(request, f'Сотрудник {user.get_full_name()} успешно создан. Логин: {username}, пароль: {password}')
        return redirect('core:employee_edit', pk=user.pk)

class EmployeeEditView(View):
    template_name = 'core/employee_form.html'
    
    def get(self, request, pk):
        # Проверка прав доступа
        if not request.user.is_authenticated or request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для редактирования сотрудников')
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
        if not request.user.is_authenticated or request.user.role not in ['DIRECTOR', 'SUPERADMIN'] and not request.user.is_superuser:
            messages.error(request, 'У вас нет прав для редактирования сотрудников')
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
        employee.age = request.POST.get('age', '')
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
                    print(f"Ошибка при удалении старого файла рекомендации: {e}")
            
            employee.recommendation_file = request.FILES['recommendation_file']
        
        employee.save()
        
        messages.success(request, f'Данные сотрудника {employee.get_full_name()} успешно обновлены')
        return redirect('core:employee_edit', pk=employee.pk)


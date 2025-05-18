from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from ..models import Expense, Task
from ..serializers import FinancialReportSerializer
from django.http import HttpResponse
from ..utils.reports import generate_pdf_report, generate_excel_report

class FinanceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def _check_finance_access(self, user):
        return user.role in ['DIRECTOR', 'SUPERADMIN', 'ACCOUNTANT']
    
    def list(self, request):
        """Получить финансовый дашборд за последние 30 дней"""
        if not self._check_finance_access(request.user):
            return Response(
                {"detail": "У вас нет доступа к финансовой информации"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Получаем данные за последние 30 дней
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        return self.generate_report(start_date, end_date)
        
    @action(detail=False, methods=['get'])
    def report(self, request):
        """Сгенерировать финансовый отчет за указанный период"""
        if not self._check_finance_access(request.user):
            return Response(
                {"detail": "У вас нет доступа к финансовой информации"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {"detail": "Необходимо указать start_date и end_date"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return self.generate_report(start_date, end_date)
    
    def generate_report(self, start_date, end_date):
        """Генерация отчета за указанный период"""
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        tasks = Task.objects.filter(created_at__range=[start_date, end_date])
        
        # Общая статистика
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        expenses_by_category = list(expenses.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total'))
        
        # Статистика по задачам
        tasks_by_status = list(tasks.values('status').annotate(
            count=Count('id')
        ).order_by('status'))
        
        # Статистика по транспорту
        expenses_by_vehicle = list(expenses.values(
            'vehicle__number', 'vehicle__brand', 'vehicle__model'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total'))
        
        data = {
            'period': {'start': start_date, 'end': end_date},
            'total_expenses': total_expenses,
            'expenses_by_category': expenses_by_category,
            'total_tasks': tasks.count(),
            'tasks_by_status': tasks_by_status,
            'expenses_by_vehicle': expenses_by_vehicle
        }
        
        serializer = FinancialReportSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """Получить ежемесячную сводку расходов"""
        if not self._check_finance_access(request.user):
            return Response(
                {"detail": "У вас нет доступа к финансовой информации"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        months = int(request.query_params.get('months', 12))
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30 * months)
        
        monthly_data = Expense.objects.filter(
            date__range=[start_date, end_date]
        ).values('category').annotate(
            year=timezone.ExtractYear('date'),
            month=timezone.ExtractMonth('date'),
            total=Sum('amount'),
            count=Count('id')
        ).order_by('year', 'month', 'category')
        
        return Response(monthly_data)
    
    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        """Экспорт финансового отчета в PDF"""
        if not self._check_finance_access(request.user):
            return Response(
                {"detail": "У вас нет доступа к финансовой информации"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Получаем данные отчета
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        if 'start_date' in request.query_params:
            start_date = request.query_params['start_date']
        if 'end_date' in request.query_params:
            end_date = request.query_params['end_date']
            
        data = self.generate_report(start_date, end_date).data
        
        # Генерируем PDF
        pdf = generate_pdf_report(data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="financial-report.pdf"'
            return response
            
        return Response(
            {"detail": "Не удалось сгенерировать PDF"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт финансового отчета в Excel"""
        if not self._check_finance_access(request.user):
            return Response(
                {"detail": "У вас нет доступа к финансовой информации"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Получаем данные отчета
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        if 'start_date' in request.query_params:
            start_date = request.query_params['start_date']
        if 'end_date' in request.query_params:
            end_date = request.query_params['end_date']
            
        data = self.generate_report(start_date, end_date).data
        
        # Генерируем Excel
        excel = generate_excel_report(data)
        response = HttpResponse(
            excel,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="financial-report.xlsx"'
        return response

    def perform_create(self, serializer):
        expense = serializer.save(created_by=self.request.user)
        from core.models import Notification
        # Уведомление для всех бухгалтеров
        for accountant in expense.get_accountants():
            Notification.create_expense_notification(accountant, expense)
        # Уведомление для создателя, если он не бухгалтер
        if not self.request.user.role == 'ACCOUNTANT':
            Notification.create_expense_notification(self.request.user, expense) 
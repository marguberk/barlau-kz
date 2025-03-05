from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
import os
from core.models import User

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
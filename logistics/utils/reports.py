from io import BytesIO
from datetime import datetime
from decimal import Decimal

from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
import xlsxwriter

def generate_pdf_report(data):
    """Генерация PDF отчета"""
    template = get_template('logistics/reports/finance_report.html')
    html = template.render({
        'data': data,
        'generated_at': timezone.now(),
        'categories': {
            'FUEL': 'Топливо',
            'MAINTENANCE': 'Техобслуживание',
            'REPAIR': 'Ремонт',
            'OTHER': 'Прочее'
        }
    })
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return None

def generate_excel_report(data):
    """Генерация Excel отчета"""
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    
    # Форматы
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#4B5563',
        'font_color': 'white',
        'border': 1
    })
    
    money_format = workbook.add_format({
        'num_format': '# ##0 ₸',
        'align': 'right'
    })
    
    date_format = workbook.add_format({
        'num_format': 'dd.mm.yyyy'
    })
    
    # Общая информация
    summary = workbook.add_worksheet('Общая информация')
    summary.set_column('A:A', 20)
    summary.set_column('B:B', 15)
    
    summary.write('A1', 'Период', header_format)
    summary.write('B1', 'Сумма', header_format)
    
    row = 1
    summary.write(row, 0, 'Всего расходов')
    summary.write(row, 1, data['total_expenses'], money_format)
    
    # Расходы по категориям
    categories = workbook.add_worksheet('По категориям')
    categories.set_column('A:A', 20)
    categories.set_column('B:C', 15)
    
    categories.write('A1', 'Категория', header_format)
    categories.write('B1', 'Сумма', header_format)
    categories.write('C1', 'Количество', header_format)
    
    row = 1
    category_names = {
        'FUEL': 'Топливо',
        'MAINTENANCE': 'Техобслуживание',
        'REPAIR': 'Ремонт',
        'OTHER': 'Прочее'
    }
    
    for expense in data['expenses_by_category']:
        categories.write(row, 0, category_names.get(expense['category'], expense['category']))
        categories.write(row, 1, expense['total'], money_format)
        categories.write(row, 2, expense['count'])
        row += 1
    
    # Расходы по транспорту
    vehicles = workbook.add_worksheet('По транспорту')
    vehicles.set_column('A:A', 30)
    vehicles.set_column('B:E', 15)
    
    vehicles.write('A1', 'Транспорт', header_format)
    vehicles.write('B1', 'Топливо', header_format)
    vehicles.write('C1', 'Ремонт', header_format)
    vehicles.write('D1', 'Обслуживание', header_format)
    vehicles.write('E1', 'Всего', header_format)
    
    row = 1
    for vehicle in data['expenses_by_vehicle']:
        vehicle_name = f"{vehicle['vehicle__brand']} {vehicle['vehicle__model']} ({vehicle['vehicle__number']})"
        vehicles.write(row, 0, vehicle_name)
        vehicles.write(row, 1, vehicle.get('fuel_total', 0), money_format)
        vehicles.write(row, 2, vehicle.get('repair_total', 0), money_format)
        vehicles.write(row, 3, vehicle.get('maintenance_total', 0), money_format)
        vehicles.write(row, 4, vehicle['total'], money_format)
        row += 1
    
    # Помесячная динамика
    monthly = workbook.add_worksheet('Помесячно')
    monthly.set_column('A:A', 15)
    monthly.set_column('B:B', 15)
    
    monthly.write('A1', 'Месяц', header_format)
    monthly.write('B1', 'Сумма', header_format)
    
    row = 1
    for month in data['expenses_by_month']:
        monthly.write(row, 0, f"{month['month']}/{month['year']}")
        monthly.write(row, 1, month['total'], money_format)
        row += 1
    
    workbook.close()
    return output.getvalue() 
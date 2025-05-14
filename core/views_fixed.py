from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

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

class VehiclesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/vehicles.html'
    
    def get(self, request, *args, **kwargs):
        return redirect('core:trucks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'vehicles'
        return context 
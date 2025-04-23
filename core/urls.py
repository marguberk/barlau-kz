from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView,
    ProfileView,
    NotificationsView,
    VehiclesView,
    TasksView,
    ExpensesView,
    FinanceView,
    WaybillViewSet,
    WaybillListView,
    WaybillPrintView,
    EmployeesView,
    EmployeeViewSet,
    NotificationViewSet,
    EmployeeDetailView,
    EmployeePDFView,
    AboutPageView,
    EmployeeFormView,
    EmployeePhotoUploadView,
    EmployeeListView,
    EmployeeCreateView,
    EmployeeEditView,
    WaybillCreateView,
    WaybillUpdateView,
    WaybillDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskArchiveView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleArchiveView,
    logout_view,
    MapView,
    ProfileEditView,
    ChangePasswordView
)
from .api import update_profile, upload_profile_photo, get_profile_stats

app_name = 'core'

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee-api')
router.register(r'waybills', WaybillViewSet, basename='waybill-api')
router.register(r'notifications', NotificationViewSet, basename='notification-api')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('vehicles/', VehiclesView.as_view(), name='vehicles'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('map/', MapView.as_view(), name='map'),
    path('expenses/', ExpensesView.as_view(), name='expenses'),
    path('finance/', FinanceView.as_view(), name='finance'),
    
    # Профиль и аутентификация
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/password/', ChangePasswordView.as_view(), name='change-password'),
    path('accounts/logout/', logout_view, name='custom-logout'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/users/me/', update_profile, name='api-profile-update'),
    path('api/users/me/photo/', upload_profile_photo, name='api-profile-photo-upload'),
    path('api/users/me/stats/', get_profile_stats, name='api-profile-stats'),
    
    # Employees
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/mobile/', EmployeesView.as_view(template_name='core/employees_mobile.html'), name='employees_mobile'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/pdf/', EmployeePDFView.as_view(), name='employee-pdf'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/upload-photo/', EmployeePhotoUploadView.as_view(), name='employee_upload_photo'),
    
    # Waybills
    path('waybills/', WaybillListView.as_view(), name='waybills'),
    path('waybills/<int:pk>/print/', WaybillPrintView.as_view(), name='waybill-print'),
    path('waybills/add/', WaybillCreateView.as_view(), name='waybill-add'),
    path('waybills/<int:pk>/edit/', WaybillUpdateView.as_view(), name='waybill-edit'),
    path('waybills/<int:pk>/delete/', WaybillDeleteView.as_view(), name='waybill-delete'),
    
    # Задачи
    path('tasks/add/', TaskCreateView.as_view(), name='task-add'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<int:pk>/archive/', TaskArchiveView.as_view(), name='task-archive'),
    
    # Транспорт
    path('vehicles/add/', VehicleCreateView.as_view(), name='vehicle-add'),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle-edit'),
    path('vehicles/<int:pk>/archive/', VehicleArchiveView.as_view(), name='vehicle-archive'),
] 
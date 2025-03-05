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
    WaybillDeleteView
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
    path('expenses/', ExpensesView.as_view(), name='expenses'),
    path('finance/', FinanceView.as_view(), name='finance'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/v1/users/me/', update_profile, name='api-profile-update'),
    path('api/v1/users/me/photo/', upload_profile_photo, name='api-profile-photo-upload'),
    path('api/v1/users/me/stats/', get_profile_stats, name='api-profile-stats'),
    
    # Employees
    path('employees/', EmployeeListView.as_view(), name='employees'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
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
] 
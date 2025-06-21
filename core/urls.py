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
    EmployeeDeleteView,
    WaybillCreateView,
    WaybillUpdateView,
    WaybillDeleteView,
    TaskCreateView,
    TaskUpdateView,
    TaskArchiveView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleArchiveView,
    VehicleDeleteView,
    logout_view,
    MapView,
    ChecklistView,
    ProfileEditView,
    ChangePasswordView,
    TrucksView,
    TruckDetailView,
    FileUploadView,
    NotificationManualCreateView,
)
from .api import (
    update_profile, upload_profile_photo, get_profile_stats, trips_api, driver_locations_api, 
    employee_pdf_api, vehicles_api, TripViewSet, ChecklistTemplateViewSet, TripChecklistViewSet, ChecklistItemViewSet,
    create_checklist_for_trip, generate_checklist_pdf, update_checklist_item, upload_checklist_photos, delete_checklist_photo
)
from logistics.views.task import TaskViewSet
from django.views.generic import TemplateView

app_name = 'core'

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee-api')
router.register(r'waybills', WaybillViewSet, basename='waybill-api')
router.register(r'notifications', NotificationViewSet, basename='notification-api')
router.register(r'tasks', TaskViewSet, basename='task-api')
router.register(r'trips', TripViewSet, basename='trip-api')
router.register(r'checklist-templates', ChecklistTemplateViewSet, basename='checklist-template-api')
router.register(r'trip-checklists', TripChecklistViewSet, basename='trip-checklist-api')
router.register(r'checklist-items', ChecklistItemViewSet, basename='checklist-item-api')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('vehicles/', VehiclesView.as_view(), name='vehicles'),
    path('trucks/', TrucksView.as_view(), name='trucks'),
    path('trucks/add/', VehicleCreateView.as_view(), name='truck-add'),
    path('trucks/<int:pk>/', TruckDetailView.as_view(), name='truck-detail'),
    path('trucks/<int:pk>/delete/', VehicleDeleteView.as_view(), name='truck-delete'),
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('map/', MapView.as_view(), name='map'),
    path('checklist/', ChecklistView.as_view(), name='checklist'),
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
    path('api/trips/', trips_api, name='api-trips'),
    path('api/trips/<int:pk>/', trips_api, name='api-trips-detail'),
    path('dashboard/api/trips/', trips_api, name='dashboard-api-trips'),
    path('dashboard/api/trips/<int:pk>/', trips_api, name='dashboard-api-trips-detail'),
    path('api/driver_locations/', driver_locations_api, name='api-driver-locations'),
    path('api/employees/<int:pk>/pdf/', employee_pdf_api, name='api-employee-pdf'),
    path('api/vehicles/', vehicles_api, name='api-vehicles'),
    path('api/trips/<int:trip_id>/create-checklist/', create_checklist_for_trip, name='api-create-checklist'),
    path('api/checklists/<int:checklist_id>/pdf/', generate_checklist_pdf, name='api-checklist-pdf'),
    path('api/checklist-items/<int:item_id>/update/', update_checklist_item, name='api-update-checklist-item'),
    path('api/checklist-items/<int:item_id>/upload-photos/', upload_checklist_photos, name='api-upload-checklist-photos'),
    path('api/checklist-photos/<int:photo_id>/delete/', delete_checklist_photo, name='api-delete-checklist-photo'),
    
    # Employees
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/mobile/', EmployeesView.as_view(template_name='core/employees_mobile.html'), name='employees_mobile'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/pdf/', EmployeePDFView.as_view(), name='employee-pdf'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
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
    
    # Офлайн-страница для PWA
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
    
    # MaroAI Design System Demo
    path('demo/maroai/', TemplateView.as_view(template_name='core/maroai-demo.html'), name='maroai-demo'),
    
    # Ручное создание уведомления
    path('notifications/manual_create/', NotificationManualCreateView.as_view(), name='notification-manual-create'),
] 
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
    TripDetailView,
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
    NotificationBroadcastView,
    NotificationBroadcastAPIView,
    UpdateFCMTokenAPIView,
    UpdateOneSignalPlayerIdAPIView,
    EmployeePDFPublicView,
    trips_simple_view,
    drivers_simple_view,
    create_trip,
    create_trip_simple,
    create_trip_test,
    DriverDocumentsView,
    DriverDocumentDeleteView,
)
# from .views_gps import gps_update_page, update_gps_data
# from .views_gps_test import gps_test_page, gps_test_api
from .api import (
    update_profile, upload_profile_photo, get_profile_stats, trips_api, public_trips_api, open_trips_api, driver_locations_api, 
    employee_pdf_api, employee_pdf_public, vehicles_api, TripViewSet, ChecklistTemplateViewSet, TripChecklistViewSet, ChecklistItemViewSet,
    create_checklist_for_trip, get_trip_checklist, generate_checklist_pdf, update_checklist_item, upload_checklist_photos, delete_checklist_photo,
    tasks_simple_api
)
# from .views_webhook import gps_webhook
from logistics.views.task import TaskViewSet
from logistics.views.expense import ExpenseViewSet
from logistics.views.vehicle import VehicleViewSet
from django.views.generic import TemplateView

app_name = 'core'

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee-api')
router.register(r'waybills', WaybillViewSet, basename='waybill-api')
router.register(r'notifications', NotificationViewSet, basename='notification-api')
router.register(r'tasks', TaskViewSet, basename='task-api')
router.register(r'expenses', ExpenseViewSet, basename='expense-api')
router.register(r'vehicles', VehicleViewSet, basename='vehicle-api')
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
    path('trips/', MapView.as_view(), name='trips'),
    path('trips/create/', create_trip, name='create-trip'),
    path('trips/create-simple/', create_trip_simple, name='create-trip-simple'),
    path('trips/create-test/', create_trip_test, name='create-trip-test'),
    path('test-trips/', TemplateView.as_view(template_name='core/test_trips.html'), name='test-trips'),
    path('checklist/', ChecklistView.as_view(), name='checklist'),
    path('expenses/', ExpensesView.as_view(), name='expenses'),
    path('finance/', FinanceView.as_view(), name='finance'),
    
    # Профиль и аутентификация
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/password/', ChangePasswordView.as_view(), name='change-password'),
    path('accounts/logout/', logout_view, name='custom-logout'),
    
    # API endpoints
    path('api/notifications/broadcast/', NotificationBroadcastAPIView.as_view(), name='api-notification-broadcast'),
    path('api/v1/users/me/fcm-token/', UpdateFCMTokenAPIView.as_view(), name='api-update-fcm-token'),
    path('api/v1/users/me/onesignal-player-id/', UpdateOneSignalPlayerIdAPIView.as_view(), name='api-update-onesignal-player-id'),
    path('api/', include(router.urls)),
    path('api/users/me/', update_profile, name='api-profile-update'),
    path('api/users/me/photo/', upload_profile_photo, name='api-profile-photo-upload'),
    path('api/users/me/stats/', get_profile_stats, name='api-profile-stats'),
    path('api/trips-custom/', trips_api, name='api-trips-custom'),
    path('api/trips-custom/<int:pk>/', trips_api, name='api-trips-custom-detail'),
    path('trips/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('api/public/trips/', public_trips_api, name='api-public-trips'),
    path('dashboard/api/trips/', trips_simple_view, name='dashboard-api-trips'),
    path('simple-trips/', trips_simple_view, name='simple-trips'),
    path('dashboard/api/trips/<int:pk>/', trips_api, name='dashboard-api-trips-detail'),
    path('api/driver_locations/', driver_locations_api, name='api-driver-locations'),
    path('api/employees/<int:pk>/pdf/', employee_pdf_api, name='api-employee-pdf'),
    path('api/public/employees/<int:pk>/pdf/', employee_pdf_public, name='api-employee-pdf-public'),
    path('api/vehicles/', vehicles_api, name='api-vehicles'),
    path('api/tasks-simple/', tasks_simple_api, name='api-tasks-simple'),
    path('api/tasks-simple/<int:pk>/', tasks_simple_api, name='api-tasks-simple-detail'),
    path('api/trips/<int:trip_id>/create-checklist/', create_checklist_for_trip, name='api-create-checklist'),
    path('api/trips/<int:trip_id>/checklist/', get_trip_checklist, name='api-get-trip-checklist'),
    path('api/checklists/<int:checklist_id>/pdf/', generate_checklist_pdf, name='api-checklist-pdf'),
    path('api/checklist-items/<int:item_id>/update/', update_checklist_item, name='api-update-checklist-item'),
    path('api/checklist-items/<int:item_id>/upload-photos/', upload_checklist_photos, name='api-upload-checklist-photos'),
    path('api/checklist-photos/<int:photo_id>/delete/', delete_checklist_photo, name='api-delete-checklist-photo'),
    
    # GPS Webhook
    # path('api/gps-webhook/', gps_webhook, name='gps-webhook'),
    
    # Employees
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/mobile/', EmployeesView.as_view(template_name='core/employees_mobile.html'), name='employees_mobile'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/pdf/', EmployeePDFView.as_view(), name='employee-pdf'),
    path('public/employees/<int:pk>/pdf/', EmployeePDFPublicView.as_view(), name='employee-pdf-public'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/edit/', EmployeeEditView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/<int:pk>/upload-photo/', EmployeePhotoUploadView.as_view(), name='employee_upload_photo'),
    path('employees/<int:driver_id>/documents/', DriverDocumentsView.as_view(), name='driver_documents'),
    path('driver-documents/<int:document_id>/delete/', DriverDocumentDeleteView.as_view(), name='driver_document_delete'),
    
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
    path('notifications/broadcast/', NotificationBroadcastView.as_view(), name='notification-broadcast'),
    
    # API endpoints
    path('simple-trips/', trips_simple_view, name='simple-trips'),
    path('simple-drivers/', drivers_simple_view, name='simple-drivers'),
    
    # GPS обновление
    # path('gps-update/', gps_update_page, name='gps-update'),
    # path('gps-update/', update_gps_data, name='gps-update-api'),
    
    # GPS тестовая страница
    # path('gps-test/', gps_test_page, name='gps-test'),
    # path('api/gps-test/', gps_test_api, name='gps-test-api'),
] 
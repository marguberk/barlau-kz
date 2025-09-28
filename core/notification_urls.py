from django.urls import path
from .api import NotificationViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    path('mark_all_read/', NotificationViewSet.as_view({'post': 'mark_all_read'}), name='notification-mark-all-read'),
    path('unread_count/', NotificationViewSet.as_view({'get': 'unread_count'}), name='notification-unread-count'),
    path('<str:pk>/mark_read/', NotificationViewSet.as_view({'post': 'mark_read'}), name='notification-mark-read'),
    path('<str:pk>/', NotificationViewSet.as_view({'get': 'retrieve'}), name='notification-detail'),
] 
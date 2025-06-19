from django.urls import path
from .views import import_devices_view, import_clients_view, import_full_wifi_view

urlpatterns = [
    path('device_render/', import_devices_view, name='device-render'),
    path('client_render/', import_clients_view, name='clients-render'),
    path('vif_render/', import_full_wifi_view, name='vif-render'),
]

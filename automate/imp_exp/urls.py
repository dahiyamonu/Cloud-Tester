from django.urls import path
from .views import import_devices, export_devices

urlpatterns = [
    path("import/", import_devices, name="import_devices"),  # URL for importing devices
    path("export/", export_devices, name="export_devices"),  # URL for exporting devices
]

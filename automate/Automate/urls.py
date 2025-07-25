from django.contrib import admin
from django.urls import path, include
from .views import home
from dummy.views import generate_dummy_data
from imp_exp.views import import_devices, export_devices
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name='home'),
    path('imp_exp/', include('imp_exp.urls')),  # Added missing trailing slash
    path('api/', include('dummy.urls')),
    path('cloud/', include('cloud.urls')),
    path('mqbroker/', include('mqbroker.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from .views import generate_dummy_data
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dummy-data/', generate_dummy_data, name='dummy-data'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
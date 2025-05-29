from django.contrib import admin

from .models import ClientMAC
# Register your models here.

@admin.register(ClientMAC)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'is_active', 'is_use', 'created_at', 'updated_at')
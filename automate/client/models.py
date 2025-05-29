from django.db import models

# Create your models here.
class ClientMAC(models.Model):
    mac = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mac
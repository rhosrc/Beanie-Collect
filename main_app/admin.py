from django.contrib import admin
from .models import Beanie, Maintenance, Accessory, Photo

# Register your models here.

admin.site.register(Beanie)
admin.site.register(Maintenance)
admin.site.register(Accessory)
admin.site.register(Photo)
from django.contrib import admin

# Register your models here.
from .models import Online

@admin.register(Online)
class OnlineAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from ticketApp.models import *

# Register your models here.
class ScreensAdmin(admin.ModelAdmin):
    pass
admin.site.register(Screens, ScreensAdmin)
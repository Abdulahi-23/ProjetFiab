from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

# Register your models here.
class DerangementAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    

    admin.site.register(models.Derangement, admin.ModelAdmin)
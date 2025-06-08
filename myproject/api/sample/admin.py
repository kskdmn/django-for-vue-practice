from django.contrib import admin

from .models import *


class SampleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_by', 'created_at', 'updated_by', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('id',)

admin.site.register(Sample, SampleAdmin)
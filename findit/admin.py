from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
	search_fields = ('name',)

admin.site.register(Feedback)
admin.site.register(Analytics)
admin.site.register(Tips)

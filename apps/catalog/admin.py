from django.contrib import admin

from .models import Company, CompanySale, Sale

# Register your models here.
admin.site.register(Company)
admin.site.register(Sale)
admin.site.register(CompanySale)
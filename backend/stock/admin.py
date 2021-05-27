from django.contrib import admin
from .models import Stock
# Register your models here.


class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'stock_activity')
    list_display_links = ['stock_name']


admin.site.register(Stock,StockAdmin)
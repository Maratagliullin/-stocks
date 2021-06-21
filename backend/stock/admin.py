from django.contrib import admin
# Register your models here.
from django.db import models
from .models import SourceDataCompany
from .models import Stock
import json
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django_celery_results.models import TaskResult
from django_celery_results.admin import TaskResultAdmin


class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'stock_activity')
    list_display_links = ['stock_name']
    # readonly_fields = ['tradingview_dentifier', 'investing_dentifier']


class SourceDataCompanyAdmin(admin.ModelAdmin):
    list_display = ('stock_ticker', 'date', 'source')
    list_display_links = ['stock_ticker']
    readonly_fields = ['stock_ticker', 'source',
                       'source_formatted', 'date', 'json_value_formatted', ]
    exclude = ('json_value', 'source_url')

    # This will help you to disbale add functionality
    def has_add_permission(self, request, obj=None):
        return False

    def source_formatted(self, obj):
        return format_html('<a href ='+obj.source_url+' target = "_blank" rel = "noopener noreferrer" > '+obj.source_url + ' </a>')
    source_formatted.short_description = 'Ссылка на источник данных'

    def json_value_formatted(self, obj=None):
        if obj and obj.json_value:
            result = json.dumps(obj.json_value, ensure_ascii=False, indent=1)
            # # keep spaces
            result_str = f'<pre>{result}</pre>'
            result = mark_safe(result_str)
            return result
    json_value_formatted.short_description = 'Данные'


# admin.site.unregister(TaskResult)
admin.site.register(Stock, StockAdmin)
admin.site.register(SourceDataCompany, SourceDataCompanyAdmin)

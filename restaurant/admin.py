from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
import uuid
from .models import Restaurant, Section, Table
from itertools import groupby
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    show_change_link = True
    fields = ['name']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_sections_count', 'get_tables_count']
    search_fields = ['name']
    inlines = [SectionInline]

    def get_sections_count(self, obj):
        return obj.sections.count()
    get_sections_count.short_description = "Секции"

    def get_tables_count(self, obj):
        return Table.objects.filter(section__restaurant=obj).count()
    get_tables_count.short_description = "Столы"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('sections')


class TableInline(admin.TabularInline):
    model = Table
    extra = 1
    show_change_link = True
    readonly_fields = ['qr_preview']
    fields = ['number', 'qr_preview']

    def qr_preview(self, obj):
        if obj and obj.qr:
            return format_html('<img src="{}" width="70" height="70"/>', obj.qr.url)
        return "QR код будет создан после сохранения"
    qr_preview.short_description = 'Предпросмотр'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'get_tables_count']
    list_filter = ['restaurant']
    search_fields = ['name', 'restaurant__name']
    autocomplete_fields = ['restaurant']
    inlines = [TableInline]

    def get_tables_count(self, obj):
        return obj.tables.count()
    get_tables_count.short_description = "Столы"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('restaurant')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = [
        'table_number',
        'section_info',
        'qr_preview',
        'download_qr',
        'status_display',
        'call_time',
        'bill_time',
        'organization_id',
        'iiko_waiter_id',
        'iiko_department_id',
    ]
    
    list_filter = [
        'section__restaurant',
        'section',
        'call_waiter',
        'bill_waiter'
    ]
    
    search_fields = [
        'number',
        'section__name',
        'section__restaurant__name',
        'organization_id',
        'iiko_waiter_id',
        'iiko_department_id'
    ]
    
    readonly_fields = ['qr_preview', 'download_qr']
    autocomplete_fields = ['section']

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'uuid',
                'number',
                'section',
            )
        }),
        ('Интеграция с iiko', {
            'fields': (
                'organization_id',
                'iiko_waiter_id',
                'iiko_department_id'
            ),
            'classes': ('collapse',),
            'description': 'Идентификаторы с системой iiko'
        }),
        ('QR код', {
            'fields': ('qr_preview', 'download_qr'),
        }),
        ('Статус обслуживания', {
            'fields': (
                ('call_waiter', 'call_time'),
                ('bill_waiter', 'bill_time')
            ),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        ro_fields = list(self.readonly_fields)
        if obj:  
            ro_fields += ['number', 'section']
            ro_fields.append('uuid')
        return ro_fields
    
    def table_number(self, obj):
        return f"Стол №{obj.number}"
    table_number.short_description = "Номер"

    def section_info(self, obj):
        if obj.section:
            return f"{obj.section.restaurant.name} - {obj.section.name}"
        return "Не назначено"
    section_info.short_description = "Расположение"

    def qr_preview(self, obj):
        if obj.qr:
            return format_html(
                '<div style="text-align: center;">'
                '<a href="{}" target="_blank">'
                '<img src="{}" width="100" height="100" style="cursor: pointer;"/>'
                '</a><br>'
                '<a href="{}" target="_blank" '
                'style="display: inline-block; padding: 5px 15px; margin-top: 5px; '
                'background-color: #417690; color: white; text-decoration: none; '
                'border-radius: 4px; font-size: 12px;">'
                'Перейти</a>'
                '</div>',
                f"{settings.AVATARIYA_BASE_URL}/{obj.uuid}/", 
                obj.qr.url,  
                f"{settings.AVATARIYA_BASE_URL}/{obj.uuid}/"   
            )
        return "QR код отсутствует"
    qr_preview.short_description = 'QR код'

    def download_qr(self, obj):
        if obj.qr:
            return format_html('<a href="{}" download>Скачать</a>', obj.qr.url)
        return "QR код отсутствует"
    download_qr.short_description = "Скачать QR"

    def status_display(self, obj):
        status = []
        if obj.call_waiter:
            if obj.call_time:
                status.append(f"Вызов официанта ({obj.call_time.strftime('%H:%M')})")
            else:
                status.append("Вызов официанта")
        if obj.bill_waiter:
            if obj.bill_time:
                status.append(f"Запрос счёта ({obj.bill_time.strftime('%H:%M')})")
            else:
                status.append("Запрос счёта")
        if status:
            return format_html("<br>".join(status))
        return "Нет активных запросов"
    status_display.short_description = "Статус стола"

    def save_model(self, request, obj, form, change):
        try:
            if not change:
                existing_table = Table.objects.filter(
                    section=obj.section,
                    number=obj.number
                ).exists()
                
                if existing_table:
                    raise ValidationError(
                        f'Стол №{obj.number} уже существует в секции "{obj.section.name}"'
                    )
            if not obj.uuid:
                obj.uuid = uuid.uuid4()
                
            if obj.call_waiter and not obj.call_time:
                obj.call_time = timezone.now()
            if obj.bill_waiter and not obj.bill_time:
                obj.bill_time = timezone.now()
                
            super().save_model(request, obj, form, change)
            
        except IntegrityError as e:
            raise ValidationError(
                f'Ошибка при создании стола №{obj.number}: {str(e)}'
            )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('section', 'section__restaurant')
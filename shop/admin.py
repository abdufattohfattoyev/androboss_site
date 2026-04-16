from django.contrib import admin
from django.utils.html import format_html
from .models import Order, VisitorStat


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'discount_badge', 'status', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at', 'ip_address')
    list_per_page = 25
    list_editable = ('status',)

    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('name', 'phone', 'discount')
        }),
        ('Holat', {
            'fields': ('status', 'note')
        }),
        ('Texnik', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def discount_badge(self, obj):
        if obj.discount:
            return format_html(
                '<span style="background:#e74c3c;color:#fff;padding:2px 8px;border-radius:12px;font-size:12px;">'
                '{}%</span>', obj.discount
            )
        return '—'
    discount_badge.short_description = 'Chegirma'

    def status_badge(self, obj):
        colors = {
            'new': '#3498db',
            'called': '#f39c12',
            'confirmed': '#27ae60',
            'cancelled': '#e74c3c',
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:12px;">'
            '{}</span>', color, obj.get_status_display()
        )
    status_badge.short_description = 'Holat'


@admin.register(VisitorStat)
class VisitorStatAdmin(admin.ModelAdmin):
    list_display = ('date', 'count')
    ordering = ('-date',)
    readonly_fields = ('date', 'count')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

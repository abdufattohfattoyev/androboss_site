from django.contrib import admin
from django.utils.html import format_html
from .models import Order, VisitorStat, TelegramAdmin, Review, ReviewMedia


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


class ReviewMediaInline(admin.TabularInline):
    model = ReviewMedia
    extra = 1
    fields = ('media_type', 'file', 'order', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if not obj.pk or not obj.file:
            return '—'
        url = obj.file.url
        if obj.media_type == 'image':
            return format_html('<img src="{}" style="height:60px;border-radius:6px;"/>', url)
        if obj.media_type == 'video':
            return format_html('<video src="{}" style="height:60px;" controls></video>', url)
        if obj.media_type == 'audio':
            return format_html('<audio src="{}" controls style="width:160px;"></audio>', url)
        return '—'
    preview.short_description = 'Ko\'rinish'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('avatar_preview', 'full_name_display', 'rating_stars', 'date', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'rating')
    search_fields = ('first_name', 'last_name', 'text')
    inlines = [ReviewMediaInline]
    list_per_page = 20

    fieldsets = (
        ('Profil', {
            'fields': ('first_name', 'last_name', 'avatar')
        }),
        ('Sharh', {
            'fields': ('rating', 'text', 'date')
        }),
        ('Sozlamalar', {
            'fields': ('is_active', 'order')
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;"/>', obj.avatar.url)
        return format_html(
            '<div style="width:40px;height:40px;border-radius:50%;background:#e74c3c;'
            'color:#fff;display:flex;align-items:center;justify-content:center;'
            'font-weight:700;font-size:14px;">{}</div>', obj.initials
        )
    avatar_preview.short_description = 'Avatar'

    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'Ism Familiya'

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#f1c40f;font-size:16px;">{}</span>', stars)
    rating_stars.short_description = 'Reyting'


@admin.register(TelegramAdmin)
class TelegramAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id', 'status_badge')
    list_editable = ('chat_id',)

    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#27ae60;color:#fff;padding:2px 10px;'
                'border-radius:12px;font-size:12px;">Faol</span>'
            )
        return format_html(
            '<span style="background:#e74c3c;color:#fff;padding:2px 10px;'
            'border-radius:12px;font-size:12px;">Nofaol</span>'
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

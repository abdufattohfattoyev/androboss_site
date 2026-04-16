import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta

from .models import Order, VisitorStat
from .telegram_utils import notify_new_order


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def landing(request):
    """Asosiy landing page."""
    return render(request, 'shop/index.html')


@csrf_exempt
@require_POST
def order_submit(request):
    """Buyurtmani qabul qiladi, DB ga saqlaydi va Telegram ga yuboradi."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, Exception):
        data = request.POST

    name = str(data.get('name', '')).strip()
    phone = str(data.get('phone', '')).strip()
    discount = int(data.get('discount', 0))

    if not name:
        return JsonResponse({'ok': False, 'error': 'Ism kiritilmagan'}, status=400)
    if not phone or len(phone) < 7:
        return JsonResponse({'ok': False, 'error': 'Telefon raqam noto\'g\'ri'}, status=400)

    order = Order.objects.create(
        name=name,
        phone=phone,
        discount=discount,
        ip_address=get_client_ip(request),
    )

    notify_new_order(order)

    return JsonResponse({'ok': True, 'order_id': order.id})


@staff_member_required
def statistics(request):
    """Admin uchun statistika sahifasi."""
    today = timezone.localdate()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Tashrif statistikasi
    visitor_stats = VisitorStat.objects.filter(date__gte=month_ago).order_by('-date')
    total_visitors_today = VisitorStat.objects.filter(date=today).first()
    total_visitors_week = sum(
        s.count for s in VisitorStat.objects.filter(date__gte=week_ago)
    )
    total_visitors_month = sum(s.count for s in visitor_stats)

    # Buyurtma statistikasi
    orders_today = Order.objects.filter(created_at__date=today).count()
    orders_week = Order.objects.filter(created_at__date__gte=week_ago).count()
    orders_month = Order.objects.filter(created_at__date__gte=month_ago).count()
    orders_total = Order.objects.count()

    recent_orders = Order.objects.all()[:20]

    ctx = {
        'visitor_stats': visitor_stats,
        'total_visitors_today': total_visitors_today.count if total_visitors_today else 0,
        'total_visitors_week': total_visitors_week,
        'total_visitors_month': total_visitors_month,
        'orders_today': orders_today,
        'orders_week': orders_week,
        'orders_month': orders_month,
        'orders_total': orders_total,
        'recent_orders': recent_orders,
    }
    return render(request, 'shop/statistics.html', ctx)

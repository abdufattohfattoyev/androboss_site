import requests
from django.conf import settings


def send_telegram_message(chat_id: str, text: str) -> bool:
    token = settings.TELEGRAM_BOT_TOKEN
    if not token or not chat_id:
        return False
    try:
        resp = requests.post(
            f'https://api.telegram.org/bot{token}/sendMessage',
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
            timeout=10,
        )
        return resp.status_code == 200
    except Exception:
        return False


def notify_new_order(order) -> None:
    """Barcha faol Telegram adminlarga yangi buyurtma haqida xabar yuboradi."""
    text = (
        f'🛒 <b>YANGI BUYURTMA!</b>\n'
        f'━━━━━━━━━━━━━━━\n'
        f'👤 Ism: <b>{order.name}</b>\n'
        f'📞 Telefon: <b>{order.phone}</b>\n'
        f'🎁 Chegirma: <b>{order.discount}%</b>\n'
        f'📅 Sana: <b>{order.created_at.strftime("%d.%m.%Y %H:%M")}</b>\n'
        f'🌐 IP: <code>{order.ip_address or "—"}</code>\n'
        f'━━━━━━━━━━━━━━━\n'
        f'#buyurtma #androboss'
    )

    sent = False
    try:
        from shop.models import TelegramAdmin
        admins = TelegramAdmin.objects.filter(is_active=True)
        for admin in admins:
            send_telegram_message(admin.chat_id, text)
            sent = True
    except Exception:
        pass

    if not sent:
        fallback = settings.TELEGRAM_CHAT_ID
        if fallback:
            send_telegram_message(fallback, text)

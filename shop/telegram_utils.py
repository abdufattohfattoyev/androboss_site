import requests
from django.conf import settings


def send_telegram_message(text: str) -> bool:
    """Telegram botga xabar yuboradi. Muvaffaqiyatli bo'lsa True qaytaradi."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        return False

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        resp = requests.post(url, json={
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML',
        }, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False


def notify_new_order(order) -> bool:
    """Yangi buyurtma haqida Telegram xabar yuboradi."""
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
    return send_telegram_message(text)

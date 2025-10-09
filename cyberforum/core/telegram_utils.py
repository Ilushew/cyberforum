import requests
from django.conf import settings

def send_telegram_message(text: str, chat_id: str = None):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не задан")
        return

    target_chat_id = chat_id or getattr(settings, 'TELEGRAM_CHANNEL_ID', None)
    if not target_chat_id:
        print("❌ Не указан chat_id")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': target_chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка отправки: {e}")
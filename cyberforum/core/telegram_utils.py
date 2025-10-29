import core.models
import requests

from django.conf import settings


def send_telegram_message(text: str):
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не задан")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "parse_mode": "HTML",
        "text": text
    }

    for subscriber in core.models.TelegramSubscriber.objects.all():
        payload["chat_id"] = subscriber.telegram_id
        try:
            requests.post(url, data=payload, timeout=5)
        except Exception as e:
            print(f"Ошибка отправки пользователю {subscriber.telegram_id}: {e}")

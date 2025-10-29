import os
import sys
import asgiref.sync
import telegram
import telegram.ext
import django


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberforum.settings')
django.setup()

from core.models import TelegramSubscriber

TELEGRAM_BOT_TOKEN = django.conf.settings.TELEGRAM_BOT_TOKEN

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не задан в settings.py")


@asgiref.sync.sync_to_async
def subscribe_user(chat_id: int, username: str):
    TelegramSubscriber.objects.get_or_create(
        telegram_id=chat_id,
        defaults={"username": username}
    )

@asgiref.sync.sync_to_async
def unsubscribe_user(chat_id: int):
    TelegramSubscriber.objects.filter(telegram_id=chat_id).delete()


async def start(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [telegram.KeyboardButton("🔔 Подписаться на рассылку"), telegram.KeyboardButton("🔕 Отписаться от рассылки")],
        [telegram.KeyboardButton("ℹ️ Информация о боте"), telegram.KeyboardButton("🌐 Перейти на сайт")],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите действие..."
    )

    await update.message.reply_text(
        "🚀 Привет! Я бот РЦФГ Удмуртии.\n"
        "Используйте кнопки ниже чтобы получать уведомления о новых событиях и новостях.",
        reply_markup=reply_markup
    )


async def handle_message(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    username = update.message.chat.username or ""

    if text == "🔔 Подписаться на рассылку":
        await subscribe_user(chat_id, username)
        await update.message.reply_text("✅ Вы успешно подписались на рассылку!")
    elif text == "🔕 Отписаться от рассылки":
        await unsubscribe_user(chat_id)
        await update.message.reply_text("❌ Вы отписались от рассылки.")
    elif text == "ℹ️ Информация о боте":
        info_text = (
            "🤖 *Информация о боте*\n\n"
            "Этот бот создан для уведомлений о новых событиях и новостях РЦФГ Удмуртии.\n"
            "Вы можете подписаться на рассылку, чтобы получать анонсы мероприятий и важные новости напрямую в Telegram.\n\n"
            "💡 Разработан командой \"404\"."
        )
        await update.message.reply_text(info_text, parse_mode="Markdown")
    elif text == "🌐 Перейти на сайт":
        await update.message.reply_text("🌐 Официальный сайт: https://")


def main():
    application = telegram.ext.Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(telegram.ext.CommandHandler("start", start))
    application.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, handle_message))

    print("Telegram-бот запущен")
    application.run_polling()


if __name__ == "__main__":
    main()

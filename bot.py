import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json

# دریافت متغیرهای محیطی
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID'))

def start(update, context):
    # بررسی اینکه آیا کاربر مجاز است یا نه
    if update.message.from_user.id == AUTHORIZED_USER_ID:
        update.message.reply_text("لطفاً اطلاعات برنامه را به صورت JSON ارسال کنید.")
    else:
        update.message.reply_text("شما مجاز به استفاده از این ربات نیستید.")

def handle_message(update, context):
    # بررسی اینکه آیا کاربر مجاز است یا نه
    if update.message.from_user.id == AUTHORIZED_USER_ID:
        try:
            # اطلاعات JSON ارسال شده از کاربر را پارس (parse) می‌کنیم
            app_data = json.loads(update.message.text)

            app_name = app_data['name']
            app_version = app_data['version']
            download_url = app_data['downloadURL']
            icon_url = app_data['iconURL']

            # پیام برای ارسال به کانال
            message = f"📱 نام برنامه: {app_name}\n🔢 نسخه: {app_version}\n🔗 لینک دانلود: {download_url}"

            # ارسال پیام و تصویر به کانال
            context.bot.send_photo(chat_id=CHANNEL_ID, photo=icon_url, caption=message)

            update.message.reply_text("اطلاعات به کانال ارسال شد.")
        except Exception as e:
            update.message.reply_text(f"خطا در پردازش اطلاعات: {e}")
    else:
        update.message.reply_text("شما مجاز به استفاده از این ربات نیستید.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

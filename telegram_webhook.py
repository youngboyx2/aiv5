from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import logging

# ใส่ TOKEN ของบอทคุณตรงนี้
TELEGRAM_TOKEN = '8022830347:AAEspymZf6jGWvXVnhhqoYlXHM-hNMrgnHE'

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

# Dispatcher สำหรับรับอีเวนต์
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# เปิด logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# คำสั่ง /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="สวัสดี! บอทพร้อมทำงานแล้วครับ")

# เพิ่ม handler
dispatcher.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# หน้า test
@app.route('/')
def index():
    return 'Hello from Telegram bot'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


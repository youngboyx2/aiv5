from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
import os
import filetype

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("7847051947:AAGkCnIoaGiWoiA3-Tq_ih_iq-aAzj8zr04")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is not set. Please add it in environment variables on Render.")
bot = Bot(token=TELEGRAM_TOKEN)

# Dispatcher สำหรับจัดการข้อความ
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

# ฟังก์ชันเมื่อมีข้อความเข้า
def handle_message(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text
    context.bot.send_message(chat_id=chat_id, text=f"📨 คุณส่ง: {text}")

# เพิ่ม handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# หน้า root
@app.route('/', methods=['GET'])
def index():
    return "✅ Telegram Webhook is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

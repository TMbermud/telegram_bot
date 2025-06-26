import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from PIL import Image
from flask import Flask
from threading import Thread

TOKEN = "8077937110:AAGFI2Ht8wd-Pg2BT1u_rJuVj0LZuwETQyE"  # Bu yerga o'z tokeningizni yozing

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

def start(update, context):
    update.message.reply_text("Salom! Menga PNG yoki JPEG rasm yubor — uni stikerga aylantirib beraman!")

def handle_image(update, context):
    user_id = update.message.from_user.id
    file = update.message.photo[-1].get_file()
    file_path = f"{user_id}_input.jpg"
    output_path = f"{user_id}_sticker.webp"

    file.download(file_path)

    try:
        img = Image.open(file_path).convert("RGBA")
        img.thumbnail((512, 512))
        new_img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        x = (512 - img.width) // 2
        y = (512 - img.height) // 2
        new_img.paste(img, (x, y), img)
        new_img.save(output_path, format="WEBP")

        with open(output_path, 'rb') as f:
            update.message.reply_sticker(f)

    except Exception as e:
        update.message.reply_text(f"Xatolik: {e}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)

def main():
    keep_alive()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

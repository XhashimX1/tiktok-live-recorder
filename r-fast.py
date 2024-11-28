import sys
import subprocess
from telegram import Bot
import os
import asyncio

# التوكين الخاص بالبوت
TOKEN = '7834159832:AAF9FgfLOJ6HLVjy1_2VRcF63qegLdaIupo'
bot = Bot(token=TOKEN)

# قراءة مسارات الملفات من سطر الأوامر
files_to_upload = sys.argv[1:]

# معرف الدردشة
chat_id = '421777948'

# دالة غير متزامنة لإرسال الفيديو إلى تليجرام
async def send_video_to_telegram(file_path):
    try:
        with open(file_path, 'rb') as video:
            await bot.send_video(chat_id=chat_id, video=video, caption=os.path.basename(file_path))
        print(f"Video {file_path} sent successfully!")
        # حذف الفيديو بعد إرساله بنجاح
        os.remove(file_path)
        print(f"Video {file_path} deleted successfully!")
    except Exception as e:
        print(f"Error sending video {file_path}: {e}")

# الدالة الرئيسية لتشغيل الكود غير المتزامن
async def main():
    for file in files_to_upload:
        await send_video_to_telegram(file)

# تشغيل الحدث غير المتزامن
asyncio.run(main())

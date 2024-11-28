import sys
import subprocess
from telegram import Bot
import os
import asyncio

# التوكين الخاص بالبوت
TOKEN = '7749324996:AAFSpsRIyPCQ9dxzOuShUATSm3V9MP1goD4'
bot = Bot(token=TOKEN)

# قراءة مسارات الملفات من سطر الأوامر
files_to_upload = sys.argv[1:]

# معرف الدردشة
chat_id = '421777948'

# دالة لتقسيم الفيديو
def split_video(video_path):
    output_pattern = video_path.rsplit('.', 1)[0] + "_part%03d.mp4"
    command = [
        'ffmpeg', '-i', video_path, '-c', 'copy', '-map', '0',
        '-segment_time', '00:01:20', '-force_key_frames', 'expr:gte(t,n_forced*80)',
        '-f', 'segment', '-reset_timestamps', '1', output_pattern
    ]
    subprocess.run(command)
    parts = [output_pattern % i for i in range(100)]  # توقع عدد الأجزاء (يمكنك تعديل هذا إذا لزم الأمر)
    parts = [part for part in parts if os.path.exists(part)]
    return parts

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
        parts = split_video(file)
        for part in parts:
            await send_video_to_telegram(part)
        # حذف الملف الأساسي بعد إرسال جميع الأجزاء
        os.remove(file)
        print(f"Original video {file} deleted successfully!")

# تشغيل الحدث غير المتزامن
asyncio.run(main())

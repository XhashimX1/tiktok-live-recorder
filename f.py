import sys
from telegram import Bot
import os
import subprocess
import asyncio

# التوكين الخاص بالبوت
TOKEN = '7749324996:AAFSpsRIyPCQ9dxzOuShUATSm3V9MP1goD4'
bot = Bot(token=TOKEN)

# قراءة مسارات الملفات من سطر الأوامر
files_to_upload = sys.argv[1:]

# معرف الدردشة
chat_id = '421777948'

# دالة لإنشاء لقطات شاشة من الفيديو
def create_screenshots(video_path):
    timestamps = ['00:00:15', '00:01:00', '00:01:40']  # النقاط الزمنية المختلفة
    screenshot_paths = []
    for i, timestamp in enumerate(timestamps):
        screenshot_path = video_path.rsplit('.', 1)[0] + f"_screenshot_{i+1}.jpg"
        command = [
            'ffmpeg', '-i', video_path, '-ss', timestamp, '-vframes', '1', screenshot_path
        ]
        subprocess.run(command, check=True)
        screenshot_paths.append(screenshot_path)
    return screenshot_paths

# دالة غير متزامنة لإرسال الفيديو مع لقطات الشاشة
async def send_video_to_telegram(file_path):
    try:
        screenshot_paths = create_screenshots(file_path)
        with open(file_path, 'rb') as video:
            await bot.send_video(chat_id=chat_id, video=video, caption=os.path.basename(file_path))
        for screenshot_path in screenshot_paths:
            with open(screenshot_path, 'rb') as screenshot:
                await bot.send_photo(chat_id=chat_id, photo=screenshot, caption=f'Screenshot of {os.path.basename(file_path)}')
        print(f"Video {file_path} and screenshots sent successfully!")
        # حذف الفيديو ولقطات الشاشة بعد إرسالهما بنجاح
        os.remove(file_path)
        for screenshot_path in screenshot_paths:
            os.remove(screenshot_path)
        print(f"Video {file_path} and screenshots deleted successfully!")
    except Exception as e:
        print(f"Error sending video {file_path}: {e}")

# الدالة الرئيسية لتشغيل الكود غير المتزامن
async def main():
    for file in files_to_upload:
        await send_video_to_telegram(file)

# تشغيل الحدث غير المتزامن
asyncio.run(main())

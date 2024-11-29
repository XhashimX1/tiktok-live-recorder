import os
from telegram import Bot
import asyncio
import sys

# التوكين الخاص بالبوت
TOKEN = '7834159832:AAF9FgfLOJ6HLVjy1_2VRcF63qegLdaIupo'
bot = Bot(token=TOKEN)

# قراءة مسار الدليل من سطر الأوامر
directory_path = sys.argv[1]

# معرف الدردشة
chat_id = '421777948'

# دالة لتقسيم الفيديو
def split_video(video_path):
    output_pattern = video_path.rsplit('.', 1)[0] + "_part%03d.mp4"
    command = [
        'ffmpeg', '-i', video_path, '-c', 'copy', '-map', '0',
        '-segment_time', '00:01:00', '-force_key_frames', 'expr:gte(t,n_forced*60)',
        '-f', 'segment', '-reset_timestamps', '1', output_pattern
    ]
    subprocess.run(command)
    parts = [output_pattern % i for i in range(100)]  # توقع عدد الأجزاء (يمكنك تعديل هذا إذا لزم الأمر)
    parts = [part for part in parts if os.path.exists(part)]
    return parts

# دالة لإنشاء لقطات شاشة من الفيديو
def create_screenshots(video_path):
    timestamps = ['00:00:10', '00:00:30', '00:00:50']  # النقاط الزمنية المختلفة
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
        
        # تأخير بسيط قبل محاولة الحذف
        await asyncio.sleep(2)
        
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
        parts = split_video(file)
        for part in parts:
            await send_video_to_telegram(part)
        # تأخير بسيط قبل محاولة الحذف
        await asyncio.sleep(2)
        os.remove(file)
        print(f"Original video {file} deleted successfully!")

# تشغيل الحدث غير المتزامن
asyncio.run(main())

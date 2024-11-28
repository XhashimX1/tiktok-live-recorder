import os
import time
import subprocess

# مسار المجلد الذي سيتم مراقبته
folder_to_monitor = '/home/runner/tiktok-live-recorder/rec'

# الدالة لمراقبة المجلد وتطبيق السكربت r.py عند تجاوز عدد الملفات 3
def monitor_folder():
    while True:
        # احصل على قائمة بالملفات ذات الامتداد .mp4 بغض النظر عن الحجم
        files = sorted(
            [os.path.join(folder_to_monitor, f) for f in os.listdir(folder_to_monitor) if f.endswith('.mp4')],
            key=os.path.getctime
        )
        # إذا تجاوز عدد الملفات 3، قم بتنفيذ السكربت r.py على أقدم ملف
        if len(files) > 3:
            oldest_file = files[0]  # أقدم ملف
            command = f'python3 r.py {oldest_file}'
            subprocess.run(command, shell=True)
        time.sleep(180)  # انتظر 180 ثانية (3 دقائق) قبل التحقق مرة أخرى

# بدء مراقبة المجلد
if __name__ == "__main__":
    monitor_folder()

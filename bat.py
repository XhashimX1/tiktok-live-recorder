import os
import time
import subprocess

# مسار المجلد الذي سيتم مراقبته
folder_to_monitor = '/home/runner/tiktok-live-recorder'

# الدالة لمراقبة المجلد وتطبيق السكربت fliv عند تجاوز عدد الملفات 5
def monitor_folder():
    while True:
        # احصل على قائمة بالملفات ذات الامتداد .mp4
        files = sorted(
            [os.path.join(folder_to_monitor, f) for f in os.listdir(folder_to_monitor) if f.endswith('.mp4')],
            key=os.path.getctime
        )
        # إذا تجاوز عدد الملفات 5، قم بتنفيذ السكربت fliv.py على أقدم 3 ملفات
        if len(files) > 5:
            for i in range(3):  # تنفيذ السكربت على أقدم 3 ملفات
                oldest_file = files[i]
                command = f'python3 fliv.py {oldest_file}'
                subprocess.run(command, shell=True)
        time.sleep(120)  # انتظر 120 ثانية (2 دقائق) قبل التحقق مرة أخرى

# بدء مراقبة المجلد
if __name__ == "__main__":
    monitor_folder()

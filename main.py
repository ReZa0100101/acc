"""
نرم‌افزار حسابداری حرفه‌ای
فایل اصلی برنامه - نسخه تصحیح شده
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# اضافه کردن مسیر پوشه‌های پروژه
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """تابع اصلی برنامه"""
    try:
        # وارد کردن کلاس‌ها
        from src.ui.main_window import MainWindow
        from src.utils.config import Config
        from src.database.database_manager import DatabaseManager
        
        # تنظیمات اولیه
        config = Config()
        
        # ایجاد دیتابیس
        db_manager = DatabaseManager(config)
        
        # ایجاد پنجره اصلی
        root = tk.Tk()
        app = MainWindow(root, config)
        
        # اجرای برنامه
        root.mainloop()
        
    except Exception as e:
        print(f"خطا در اجرای برنامه: {e}")
        import traceback
        traceback.print_exc()
        input("برای خروج Enter را فشار دهید...")

if __name__ == "__main__":
    main()

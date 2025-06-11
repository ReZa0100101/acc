"""
فایل تنظیمات برنامه - نسخه بهبود یافته
"""

import os
import json
from pathlib import Path

class Config:
    """کلاس مدیریت تنظیمات برنامه"""
    
    def __init__(self):
        self.app_name = "نرم افزار جامع حسابداری"
        self.version = "1.0.0"
        self.author = "توسعه‌دهنده"
        
        # مسیرهای پروژه
        self.base_dir = Path(__file__).parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.config_dir = self.base_dir / "config"
        self.assets_dir = self.base_dir / "assets"
        self.icons_dir = self.assets_dir / "icons"
        
        # ایجاد پوشه‌ها در صورت عدم وجود
        self._create_directories()
        
        # تنظیمات فونت
        self.fonts = {
            'persian_text': ('Iranian Sans', 9, 'bold'),  # فونت متن فارسی
            'numbers': ('Calibri', 9, 'normal'),  # فونت اعداد
            'title': ('Iranian Sans', 12, 'bold'),  # فونت عناوین
            'button': ('Iranian Sans', 9, 'bold')  # فونت دکمه‌ها
        }
        
        # تنظیمات رابط کاربری
        self.ui_settings = {
            'window_width': 1280,
            'window_height': 720,
            'min_width': 1024,
            'min_height': 600,
            'rtl_support': True
        }
        
        # رنگ‌های برنامه
        self.colors = {
            'primary': '#F18F01',  # نارنجی
            'secondary': '#333333',  # مشکی
            'menu_bg': '#FFFFFF',  # سفید
            'menu_hover': '#E0E0E0',  # خاکستری روشن
            'menu_active': '#F18F01',  # نارنجی
            'text_primary': '#333333',  # مشکی
            'text_secondary': '#666666',  # خاکستری
            'text_light': '#FFFFFF',  # سفید
            'border': '#CCCCCC',  # خاکستری روشن
            'form_bg': '#F8F9FA',  # پس‌زمینه فرم
            'input_bg': '#FFFFFF',  # پس‌زمینه ورودی
            'success': '#28A745',  # سبز
            'error': '#DC3545',  # قرمز
            'warning': '#FFC107'  # زرد
        }
        
        # اطلاعات تماس
        self.contact_info = {
            'support': '۰۹۱۲۶۵۷۷۴۴۲\n۰۹۳۳۹۴۷۸۰۵۰',
            'sales': '۰۲۱-۵۷۹۵۳\n۰۲۱-۴۱۶۷۵۰۰۰',
            'company': 'فناوری اطلاعات صبور'
        }
        
        # تنظیمات دیتابیس
        self.database = {
            'name': 'accounting.db',
            'path': self.data_dir / 'accounting.db'
        }
        
    def _create_directories(self):
        """ایجاد پوشه‌های مورد نیاز"""
        directories = [self.data_dir, self.config_dir, self.assets_dir, self.icons_dir]
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    def save_config(self, config_data, filename):
        """ذخیره تنظیمات در فایل"""
        config_path = self.config_dir / f"{filename}.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    def load_config(self, filename):
        """بارگذاری تنظیمات از فایل"""
        config_path = self.config_dir / f"{filename}.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

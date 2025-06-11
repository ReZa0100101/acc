"""
نوار وضعیت برنامه - نسخه تصحیح شده
"""

import tkinter as tk
from tkinter import ttk

class StatusBar:
    """کلاس نوار وضعیت"""
    
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.create_status_bar()
    
    def create_status_bar(self):
        """ایجاد نوار وضعیت"""
        # فریم نوار وضعیت
        self.status_frame = tk.Frame(self.root, bg="#F0F0F0", height=25)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # برچسب کاربر
        self.user_label = tk.Label(
            self.status_frame,
            text="کاربر جاری: مدیر سیستم",
            font=self.config.fonts['persian_text'],
            bg="#F0F0F0"
        )
        self.user_label.pack(side=tk.RIGHT, padx=10)
        
        # جداکننده
        separator1 = tk.Label(
            self.status_frame,
            text="|",
            font=self.config.fonts['persian_text'],
            bg="#F0F0F0"
        )
        separator1.pack(side=tk.RIGHT)
        
        # برچسب تاریخ و ساعت
        self.datetime_label = tk.Label(
            self.status_frame,
            text="",
            font=self.config.fonts['numbers'],
            bg="#F0F0F0"
        )
        self.datetime_label.pack(side=tk.RIGHT, padx=10)
        
        # آیکن تقویم
        self.calendar_label = tk.Label(
            self.status_frame,
            text="📅",
            font=self.config.fonts['persian_text'],
            bg="#F0F0F0"
        )
        self.calendar_label.pack(side=tk.RIGHT)
    
    def update_status(self, message):
        """به‌روزرسانی پیام وضعیت"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def update_datetime(self, datetime_str):
        """به‌روزرسانی تاریخ و ساعت"""
        self.datetime_label.config(text=datetime_str)

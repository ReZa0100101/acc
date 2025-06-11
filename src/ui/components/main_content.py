"""
محتوای اصلی برنامه - نسخه بهبود یافته با پشتیبانی از تب‌ها
"""

import tkinter as tk
from tkinter import ttk
import math

class MainContent:
    """کلاس محتوای اصلی برنامه"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.create_content()
        self.active_tabs = {}  # نگهداری تب‌های فعال
    
    def create_content(self):
        """ایجاد محتوای اصلی"""
        # فریم اصلی محتوا
        self.content_frame = tk.Frame(self.parent, bg=self.config.colors['secondary'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # ایجاد طرح دو رنگ (نارنجی و مشکی)
        self.create_diagonal_background()
        
        # اطلاعات تماس
        self.create_contact_info()
        
        # پیام خوش‌آمدگویی
        self.create_welcome_message()
        
        # ایجاد نوار تب‌ها
        self.create_tab_bar()
    
    def create_diagonal_background(self):
        """ایجاد پس‌زمینه دو رنگ با خط مورب"""
        # کانواس برای رسم پس‌زمینه
        self.canvas = tk.Canvas(
            self.content_frame, 
            bg=self.config.colors['secondary'],
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # رسم مثلث نارنجی
        def draw_background(event=None):
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            # پاک کردن کانواس
            self.canvas.delete("all")
            
            # رسم مثلث نارنجی
            self.canvas.create_polygon(
                0, 0,  # بالا سمت چپ
                0, height,  # پایین سمت چپ
                width * 0.6, height,  # پایین وسط
                0, 0,  # بالا سمت چپ
                fill=self.config.colors['primary'],
                outline=""
            )
        
        # تنظیم رویداد تغییر اندازه
        self.canvas.bind("<Configure>", draw_background)
    
    def create_contact_info(self):
        """ایجاد اطلاعات تماس"""
        # فریم اطلاعات تماس
        contact_frame = tk.Frame(self.canvas, bg=self.config.colors['secondary'])
        self.canvas.create_window(
            self.canvas.winfo_reqwidth() - 20, 
            self.canvas.winfo_reqheight() - 100,
            window=contact_frame,
            anchor=tk.NE
        )
        
        # لوگوی شرکت
        logo_label = tk.Label(
            contact_frame, 
            text=self.config.contact_info['company'],
            font=self.config.fonts['title'],
            fg=self.config.colors['text_light'],
            bg=self.config.colors['secondary']
        )
        logo_label.pack(anchor=tk.E, pady=(0, 10))
        
        # خط جداکننده
        separator = tk.Frame(contact_frame, height=2, width=200, bg=self.config.colors['text_light'])
        separator.pack(anchor=tk.E, pady=5)
        
        # اطلاعات تماس
        support_label = tk.Label(
            contact_frame,
            text=f"مشاوره و پشتیبانی: {self.config.contact_info['support']}",
            font=self.config.fonts['numbers'],
            fg=self.config.colors['text_light'],
            bg=self.config.colors['secondary'],
            justify=tk.RIGHT
        )
        support_label.pack(anchor=tk.E)
        
        sales_label = tk.Label(
            contact_frame,
            text=f"فروش: {self.config.contact_info['sales']}",
            font=self.config.fonts['numbers'],
            fg=self.config.colors['text_light'],
            bg=self.config.colors['secondary'],
            justify=tk.RIGHT
        )
        sales_label.pack(anchor=tk.E)
    
    def create_welcome_message(self):
        """ایجاد پیام خوش‌آمدگویی"""
        # متن خوش‌آمدگویی
        welcome_label = tk.Label(
            self.canvas,
            text="جهت دریافت شناسه کالا و خدمت کلیک کنید",
            font=self.config.fonts['title'],
            fg=self.config.colors['text_light'],
            bg=self.config.colors['secondary']
        )
        
        # قرار دادن متن در کانواس
        self.canvas.create_window(
            self.canvas.winfo_reqwidth() - 20,
            100,
            window=welcome_label,
            anchor=tk.NE
        )
    
    def create_tab_bar(self):
        """ایجاد نوار تب‌ها"""
        # فریم نوار تب‌ها
        self.tab_frame = tk.Frame(self.content_frame, bg='#F0F0F0', height=30)
        self.tab_frame.pack(side=tk.TOP, fill=tk.X)
        
        # نوتبوک برای مدیریت تب‌ها
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # تنظیم استایل تب‌ها
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Iranian Sans', 10, 'normal'))
        style.configure('TNotebook', background='#F0F0F0')
    
    def add_tab(self, title, content_class, *args, **kwargs):
        """اضافه کردن تب جدید"""
        # بررسی وجود تب با همین عنوان
        if title in self.active_tabs:
            # انتخاب تب موجود
            tab_index = self.notebook.index(self.active_tabs[title])
            self.notebook.select(tab_index)
            return self.active_tabs[title]
        
        # ایجاد فریم جدید برای تب
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=title)
        
        # ایجاد محتوای تب
        tab_content = content_class(tab_frame, self.config, *args, **kwargs)
        
        # ذخیره تب در لیست تب‌های فعال
        self.active_tabs[title] = tab_frame
        
        # انتخاب تب جدید
        self.notebook.select(self.notebook.index(tab_frame))
        
        return tab_content
    
    def close_tab(self, title):
        """بستن تب"""
        if title in self.active_tabs:
            tab_index = self.notebook.index(self.active_tabs[title])
            self.notebook.forget(tab_index)
            del self.active_tabs[title]
    
    def close_all_tabs(self):
        """بستن همه تب‌ها"""
        for title in list(self.active_tabs.keys()):
            self.close_tab(title)

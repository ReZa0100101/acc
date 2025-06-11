"""
منوی بالای برنامه - نسخه بهبود یافته با import های صحیح
"""

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

class TopMenu:
    """کلاس منوی بالای برنامه"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.active_menu = None
        self.submenu_frame = None
        self.menu_frames = {}
        self.menu_buttons = {}
        self.create_menu()
    
    def create_menu(self):
        """ایجاد منوی اصلی"""
        # فریم منوی اصلی
        self.menu_frame = tk.Frame(self.parent, bg=self.config.colors['menu_bg'], height=100)
        self.menu_frame.pack(fill=tk.X)
        
        # تعریف منوها (از راست به چپ)
        menus = [
            {"name": "تعاریف اولیه", "icon": "definitions.png", "command": lambda: self.toggle_submenu("تعاریف اولیه")},
            {"name": "طرف حساب ها", "icon": "accounts.png", "command": lambda: self.toggle_submenu("طرف حساب ها")},
            {"name": "صدور فاکتور", "icon": "invoice.png", "command": lambda: self.toggle_submenu("صدور فاکتور")},
            {"name": "دریافت و پرداخت", "icon": "payment.png", "command": lambda: self.toggle_submenu("دریافت و پرداخت")},
            {"name": "گزارشات", "icon": "reports.png", "command": lambda: self.toggle_submenu("گزارشات")},
            {"name": "مدیریت سیستم", "icon": "system.png", "command": lambda: self.toggle_submenu("مدیریت سیستم")},
            {"name": "سامانه مودیان", "icon": "taxpayers.png", "command": lambda: self.toggle_submenu("سامانه مودیان")},
            {"name": "فعال سازی", "icon": "activate.png", "command": lambda: self.toggle_submenu("فعال سازی")},
            {"name": "آموزش", "icon": "education.png", "command": lambda: self.toggle_submenu("آموزش")},
        ]
        
        # ایجاد دکمه‌های منو از راست به چپ
        for i, menu in enumerate(menus):
            frame = tk.Frame(self.menu_frame, bg=self.config.colors['menu_bg'], padx=5, pady=5)
            frame.pack(side=tk.RIGHT, padx=2)
            self.menu_frames[menu["name"]] = frame
            
            # ایجاد دکمه با فونت فارسی
            button = tk.Button(
                frame, 
                text=menu["name"],
                compound=tk.TOP,
                bg=self.config.colors['menu_bg'],
                fg=self.config.colors['text_primary'],
                font=self.config.fonts['button'],
                relief=tk.FLAT,
                bd=0,
                padx=10,
                pady=5,
                command=menu["command"]
            )
            button.pack(fill=tk.BOTH, expand=True)
            self.menu_buttons[menu["name"]] = button
        
        # دکمه صفحه اصلی
        home_frame = tk.Frame(self.menu_frame, bg=self.config.colors['menu_bg'], padx=5, pady=5)
        home_frame.pack(side=tk.LEFT, padx=2)
        
        home_button = tk.Button(
            home_frame, 
            text="صفحه اصلی",
            compound=tk.TOP,
            bg=self.config.colors['menu_bg'],
            fg=self.config.colors['text_primary'],
            font=self.config.fonts['button'],
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=5,
            command=self.show_home
        )
        home_button.pack(fill=tk.BOTH, expand=True)
    
    def toggle_submenu(self, menu_name):
        """نمایش یا مخفی کردن زیرمنو"""
        # اگر زیرمنویی باز است، آن را ببندیم
        if self.submenu_frame:
            self.submenu_frame.destroy()
            self.submenu_frame = None
            
            # اگر روی همان منوی قبلی کلیک شده، فقط بستن کافی است
            if self.active_menu == menu_name:
                self.active_menu = None
                return
        
        # ذخیره منوی فعال
        self.active_menu = menu_name
        
        # ایجاد زیرمنو برای منوی انتخاب شده
        if menu_name == "تعاریف اولیه":
            self.show_definitions_submenu()
        elif menu_name == "طرف حساب ها":
            self.show_accounts_submenu()
        elif menu_name == "صدور فاکتور":
            self.show_invoice_submenu()
        elif menu_name == "دریافت و پرداخت":
            self.show_payment_submenu()
        elif menu_name == "گزارشات":
            self.show_reports_submenu()
        elif menu_name == "مدیریت سیستم":
            self.show_system_submenu()
        elif menu_name == "سامانه مودیان":
            self.show_taxpayers_submenu()
        elif menu_name == "فعال سازی":
            self.show_activation_submenu()
        elif menu_name == "آموزش":
            self.show_education_submenu()
    
    def calculate_submenu_width(self, items):
        """محاسبه عرض مناسب برای زیرمنو بر اساس طولانی‌ترین آیتم"""
        # ایجاد یک لیبل موقت برای محاسبه عرض
        temp_label = tk.Label(self.parent, font=self.config.fonts['persian_text'])
        
        max_width = 0
        for item in items:
            temp_label.config(text=item["name"])
            temp_label.update_idletasks()
            text_width = temp_label.winfo_reqwidth()
            if text_width > max_width:
                max_width = text_width
        
        temp_label.destroy()
        
        # اضافه کردن padding و حداقل عرض
        return max(max_width + 40, 200)  # حداقل 200 پیکسل
    
    def create_submenu(self, menu_name, items):
        """ایجاد زیرمنو با عرض خودکار و موقعیت صحیح"""
        # مخفی کردن زیرمنوهای قبلی
        if self.submenu_frame:
            self.submenu_frame.destroy()
        
        # دریافت موقعیت و اندازه دکمه منو
        button = self.menu_buttons[menu_name]
        frame = self.menu_frames[menu_name]
        
        # محاسبه عرض مناسب برای زیرمنو
        submenu_width = self.calculate_submenu_width(items)
        
        # ایجاد فریم زیرمنو
        self.submenu_frame = tk.Frame(
            self.parent, 
            bg=self.config.colors['menu_bg'],
            relief=tk.RAISED,
            bd=1
        )
        
        # محاسبه موقعیت زیرمنو
        # به‌روزرسانی اطلاعات موقعیت
        frame.update_idletasks()
        button.update_idletasks()
        
        # موقعیت سمت راست دکمه منو
        frame_x = frame.winfo_x()
        frame_width = frame.winfo_width()
        menu_right_x = frame_x + frame_width
        
        # موقعیت y زیر منو
        menu_y = self.menu_frame.winfo_height()
        
        # تنظیم موقعیت زیرمنو تا سمت راست آن با سمت راست منو هم‌راستا باشد
        submenu_x = menu_right_x - submenu_width
        
        # اطمینان از اینکه زیرمنو از سمت چپ صفحه خارج نشود
        if submenu_x < 0:
            submenu_x = 0
        
        # قرار دادن زیرمنو در موقعیت مناسب
        self.submenu_frame.place(x=submenu_x, y=menu_y, width=submenu_width)
        
        # ایجاد دکمه‌های زیرمنو
        for item in items:
            button_frame = tk.Frame(self.submenu_frame, bg=self.config.colors['menu_bg'])
            button_frame.pack(fill=tk.X, padx=2, pady=1)
            
            button = tk.Button(
                button_frame,
                text=item["name"],
                anchor=tk.E,  # راست چین
                bg=self.config.colors['menu_bg'],
                fg=self.config.colors['text_primary'],
                font=self.config.fonts['persian_text'],
                relief=tk.FLAT,
                bd=0,
                padx=15,
                pady=5,
                command=item.get("command", lambda: None)
            )
            button.pack(fill=tk.X)
            
            # اضافه کردن افکت hover
            def on_enter(e, btn=button):
                btn.config(bg=self.config.colors['menu_hover'])
            
            def on_leave(e, btn=button):
                btn.config(bg=self.config.colors['menu_bg'])
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
    
    # توابع نمایش زیرمنوها
    def show_definitions_submenu(self):
        items = [
            {"name": "تعریف انبار", "command": lambda: self.open_warehouse_form()},
            {"name": "تعریف گروه کالا و خدمات", "command": lambda: self.open_product_group_form()},
            {"name": "واحدهای اندازه گیری", "command": lambda: self.open_units_form()},
            {"name": "تعریف کالا و خدمات", "command": lambda: self.open_products_form()},
            {"name": "لیست کالا و خدمات", "command": lambda: self.open_products_list()},
            {"name": "بانک ها", "command": lambda: self.open_banks_form()},
            {"name": "حساب های بانکی", "command": lambda: self.open_bank_accounts_form()},
            {"name": "صندوق ها", "command": lambda: self.open_cash_boxes_form()},
            {"name": "تعریف درآمد و هزینه", "command": lambda: self.open_income_expense_form()},
            {"name": "تعریف فرمول تولید", "command": lambda: self.open_production_formula_form()}
        ]
        self.create_submenu("تعاریف اولیه", items)
    
    def show_accounts_submenu(self):
        items = [
            {"name": "لیست اشخاص و طرف حساب ها", "command": lambda: self.open_customers_list()},
            {"name": "ایجاد طرف حساب جدید", "command": lambda: self.open_customer_form()},
            {"name": "لیست پیگیری ها و درج پیگیری جدید", "command": lambda: print("لیست پیگیری ها")},
            {"name": "نحوه آشنایی ها", "command": lambda: print("نحوه آشنایی ها")},
            {"name": "گروه بندی طرف حساب ها", "command": lambda: print("گروه بندی طرف حساب ها")},
            {"name": "ورود مشتری از طریق اکسل", "command": lambda: print("ورود مشتری از طریق اکسل")}
        ]
        self.create_submenu("طرف حساب ها", items)
    
    def show_invoice_submenu(self):
        items = [
            {"name": "صدور فاکتور خرید", "command": lambda: print("صدور فاکتور خرید")},
            {"name": "صدور فاکتور فروش", "command": lambda: print("صدور فاکتور فروش")},
            {"name": "صدور فاکتور فروش (طلا و جواهر)", "command": lambda: print("صدور فاکتور فروش طلا")},
            {"name": "صدور فاکتور فروش فوری", "command": lambda: print("صدور فاکتور فروش فوری")},
            {"name": "صدور فاکتور برگشت از خرید", "command": lambda: print("صدور فاکتور برگشت از خرید")}
        ]
        self.create_submenu("صدور فاکتور", items)
    
    def show_payment_submenu(self):
        items = [
            {"name": "ثبت دریافتی ها", "command": lambda: print("ثبت دریافتی ها")},
            {"name": "ثبت پرداختی ها", "command": lambda: print("ثبت پرداختی ها")},
            {"name": "جابجایی بین صندوق ها و حساب ها", "command": lambda: print("جابجایی بین صندوق ها")},
            {"name": "ثبت درآمدها", "command": lambda: print("ثبت درآمدها")},
            {"name": "ثبت هزینه ها", "command": lambda: print("ثبت هزینه ها")}
        ]
        self.create_submenu("دریافت و پرداخت", items)
    
    def show_reports_submenu(self):
        items = [
            {"name": "گزارش فاکتورها", "command": lambda: print("گزارش فاکتورها")},
            {"name": "گزارش دریافت و پرداخت طرف حساب", "command": lambda: print("گزارش دریافت و پرداخت")},
            {"name": "گزارش عملکرد حساب", "command": lambda: print("گزارش عملکرد حساب")},
            {"name": "گزارش عملکرد صندوق", "command": lambda: print("گزارش عملکرد صندوق")}
        ]
        self.create_submenu("گزارشات", items)
    
    def show_system_submenu(self):
        items = [
            {"name": "تنظیمات سیستم", "command": lambda: print("تنظیمات سیستم")},
            {"name": "سطح دسترسی ها", "command": lambda: print("سطح دسترسی ها")},
            {"name": "کاربران", "command": lambda: print("کاربران")},
            {"name": "تهیه نسخه پشتیبان از اطلاعات", "command": lambda: print("تهیه نسخه پشتیبان")},
            {"name": "بازیابی فایل پشتیبان", "command": lambda: print("بازیابی فایل پشتیبان")}
        ]
        self.create_submenu("مدیریت سیستم", items)
    
    def show_taxpayers_submenu(self):
        items = [
            {"name": "اتصال به سامانه مودیان", "command": lambda: print("اتصال به سامانه مودیان")},
            {"name": "تنظیمات سامانه", "command": lambda: print("تنظیمات سامانه")},
            {"name": "گزارش ارسال‌ها", "command": lambda: print("گزارش ارسال‌ها")}
        ]
        self.create_submenu("سامانه مودیان", items)
    
    def show_activation_submenu(self):
        items = [
            {"name": "فعال‌سازی نرم‌افزار", "command": lambda: print("فعال‌سازی نرم‌افزار")},
            {"name": "وضعیت لایسنس", "command": lambda: print("وضعیت لایسنس")},
            {"name": "تمدید لایسنس", "command": lambda: print("تمدید لایسنس")}
        ]
        self.create_submenu("فعال سازی", items)
    
    def show_education_submenu(self):
        items = [
            {"name": "آموزش کار با نرم‌افزار", "command": lambda: print("آموزش کار با نرم‌افزار")},
            {"name": "راهنمای سریع", "command": lambda: print("راهنمای سریع")},
            {"name": "ویدیوهای آموزشی", "command": lambda: print("ویدیوهای آموزشی")}
        ]
        self.create_submenu("آموزش", items)
    
    def show_home(self):
        """نمایش صفحه اصلی"""
        if self.submenu_frame:
            self.submenu_frame.destroy()
            self.submenu_frame = None
            self.active_menu = None
        print("نمایش صفحه اصلی")
    
    # توابع باز کردن فرم‌ها
    def open_warehouse_form(self):
        """باز کردن فرم انبار"""
        try:
            from ...ui.forms.warehouse_form import WarehouseForm
            form = WarehouseForm(self.parent, self.config)
        except Exception as e:
            print(f"خطا در باز کردن فرم انبار: {e}")
    
    def open_product_group_form(self):
        """باز کردن فرم گروه کالا"""
        try:
            from ...ui.forms.product_group_form import ProductGroupForm
            form = ProductGroupForm(self.parent, self.config)
        except Exception as e:
            print(f"خطا در باز کردن فرم گروه کالا: {e}")
    
    def open_units_form(self):
        """باز کردن فرم واحدها"""
        try:
            from ...ui.forms.units_form import UnitsForm
            form = UnitsForm(self.parent, self.config)
        except Exception as e:
            print(f"خطا در باز کردن فرم واحدها: {e}")

    
    def open_products_form(self):
        """باز کردن فرم کالا"""
        try:
            from ...ui.forms.products_form import ProductsForm
            form = ProductsForm(self.parent, self.config)
        except Exception as e:
            print(f"خطا در باز کردن فرم کالا: {e}")
    
    def open_products_list(self):
        """باز کردن لیست کالا"""
        try:
            from ...ui.forms.products_list import ProductsListForm
            
            # اگر main_window در دسترس است، فرم را در آن نمایش دهیم
            if hasattr(self.parent, 'master') and hasattr(self.parent.master, 'show_form_in_main_content'):
                self.parent.master.show_form_in_main_content(ProductsListForm)
            else:
                # در غیر این صورت به روش قبلی باز کنیم
                form = ProductsListForm(self.parent, self.config)
        except Exception as e:
            print(f"خطا در باز کردن لیست کالا: {e}")
    
    def open_banks_form(self):
        print("باز کردن فرم بانک‌ها")
        # TODO: پیاده‌سازی فرم بانک‌ها
    
    def open_bank_accounts_form(self):
        print("باز کردن فرم حساب‌های بانکی")
        # TODO: پیاده‌سازی فرم حساب‌های بانکی
    
    def open_cash_boxes_form(self):
        print("باز کردن فرم صندوق‌ها")
        # TODO: پیاده‌سازی فرم صندوق‌ها
    
    def open_income_expense_form(self):
        print("باز کردن فرم درآمد و هزینه")
        # TODO: پیاده‌سازی فرم درآمد و هزینه
    
    def open_production_formula_form(self):
        print("باز کردن فرم فرمول تولید")
        # TODO: پیاده‌سازی فرم فرمول تولید
    
    def open_customers_list(self):
        print("باز کردن لیست مشتریان")
        # TODO: پیاده‌سازی لیست مشتریان
    
    def open_customer_form(self):
        print("باز کردن فرم مشتری")
        # TODO: پیاده‌سازی فرم مشتری

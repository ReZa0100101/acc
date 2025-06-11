"""
داشبورد اصلی برنامه
"""

import tkinter as tk
from tkinter import ttk

class Dashboard:
    """کلاس داشبورد اصلی"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.create_dashboard()
    
    def create_dashboard(self):
        """ایجاد داشبورد"""
        # فریم اصلی داشبورد
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # عنوان داشبورد
        title_label = ttk.Label(
            self.main_frame,
            text="داشبورد حسابداری",
            font=(self.config.ui_settings['font_family'], 16, 'bold')
        )
        title_label.pack(pady=20)
        
        # فریم کارت‌های اطلاعاتی
        self.cards_frame = ttk.Frame(self.main_frame)
        self.cards_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # کارت‌های اطلاعاتی
        self.create_info_cards()
        
        # فریم دکمه‌های سریع
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # دکمه‌های دسترسی سریع
        self.create_quick_buttons()
    
    def create_info_cards(self):
        """ایجاد کارت‌های اطلاعاتی"""
        # کارت تعداد اسناد
        documents_frame = ttk.LabelFrame(self.cards_frame, text="اسناد", padding=10)
        documents_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(documents_frame, text="تعداد اسناد امروز:", font=('Tahoma', 10)).pack()
        ttk.Label(documents_frame, text="0", font=('Tahoma', 14, 'bold'), foreground='blue').pack()
        
        # کارت مانده حساب‌ها
        accounts_frame = ttk.LabelFrame(self.cards_frame, text="حساب‌ها", padding=10)
        accounts_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(accounts_frame, text="تعداد حساب‌ها:", font=('Tahoma', 10)).pack()
        ttk.Label(accounts_frame, text="0", font=('Tahoma', 14, 'bold'), foreground='green').pack()
        
        # کارت گردش مالی
        financial_frame = ttk.LabelFrame(self.cards_frame, text="گردش مالی", padding=10)
        financial_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(financial_frame, text="گردش امروز:", font=('Tahoma', 10)).pack()
        ttk.Label(financial_frame, text="0 ریال", font=('Tahoma', 14, 'bold'), foreground='red').pack()
    
    def create_quick_buttons(self):
        """ایجاد دکمه‌های دسترسی سریع"""
        # عنوان
        ttk.Label(
            self.buttons_frame,
            text="دسترسی سریع",
            font=(self.config.ui_settings['font_family'], 12, 'bold')
        ).pack(pady=(0, 10))
        
        # فریم دکمه‌ها
        buttons_container = ttk.Frame(self.buttons_frame)
        buttons_container.pack()
        
        # ردیف اول دکمه‌ها
        row1_frame = ttk.Frame(buttons_container)
        row1_frame.pack(pady=5)
        
        ttk.Button(row1_frame, text="سند جدید", width=15, command=self.new_document).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1_frame, text="تعریف حساب", width=15, command=self.new_account).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1_frame, text="گزارش تراز", width=15, command=self.trial_balance).pack(side=tk.LEFT, padx=5)
        
        # ردیف دوم دکمه‌ها
        row2_frame = ttk.Frame(buttons_container)
        row2_frame.pack(pady=5)
        
        ttk.Button(row2_frame, text="لیست اسناد", width=15, command=self.list_documents).pack(side=tk.LEFT, padx=5)
        ttk.Button(row2_frame, text="لیست حساب‌ها", width=15, command=self.list_accounts).pack(side=tk.LEFT, padx=5)
        ttk.Button(row2_frame, text="پشتیبان‌گیری", width=15, command=self.backup).pack(side=tk.LEFT, padx=5)
    
    # توابع دکمه‌ها
    def new_document(self):
        print("سند جدید ایجاد شد")
    
    def new_account(self):
        print("حساب جدید تعریف شد")
    
    def trial_balance(self):
        print("گزارش تراز آزمایشی")
    
    def list_documents(self):
        print("لیست اسناد")
    
    def list_accounts(self):
        print("لیست حساب‌ها")
    
    def backup(self):
        print("پشتیبان‌گیری انجام شد")

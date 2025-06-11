"""
نوار منوی اصلی برنامه - نسخه راست چین
"""

import tkinter as tk
from tkinter import messagebox

class MenuBar:
    """کلاس نوار منوی اصلی"""
    
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.create_menu()
    
    def create_menu(self):
        """ایجاد منوی اصلی راست چین"""
        # ایجاد نوار منو
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # منوی راهنما (سمت راست)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="راهنما", menu=self.help_menu)
        self.help_menu.add_command(label="راهنمای استفاده", command=self.show_help)
        self.help_menu.add_command(label="درباره برنامه", command=self.about)
        
        # منوی تنظیمات
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="تنظیمات", menu=self.settings_menu)
        self.settings_menu.add_command(label="تنظیمات عمومی", command=self.general_settings)
        self.settings_menu.add_command(label="پشتیبان‌گیری", command=self.backup)
        self.settings_menu.add_command(label="بازیابی", command=self.restore)
        
        # منوی گزارشات
        self.reports_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="گزارشات", menu=self.reports_menu)
        self.reports_menu.add_command(label="تراز آزمایشی", command=self.trial_balance)
        self.reports_menu.add_command(label="ترازنامه", command=self.balance_sheet)
        self.reports_menu.add_command(label="سود و زیان", command=self.profit_loss)
        self.reports_menu.add_separator()
        self.reports_menu.add_command(label="گردش حساب", command=self.account_statement)
        self.reports_menu.add_command(label="دفتر کل", command=self.general_ledger)
        
        # منوی حسابداری
        self.accounting_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="حسابداری", menu=self.accounting_menu)
        
        # زیرمنوی اسناد
        self.documents_menu = tk.Menu(self.accounting_menu, tearoff=0)
        self.accounting_menu.add_cascade(label="اسناد", menu=self.documents_menu)
        self.documents_menu.add_command(label="سند جدید", command=self.new_document)
        self.documents_menu.add_command(label="ویرایش سند", command=self.edit_document)
        self.documents_menu.add_command(label="حذف سند", command=self.delete_document)
        self.documents_menu.add_separator()
        self.documents_menu.add_command(label="لیست اسناد", command=self.list_documents)
        self.documents_menu.add_command(label="جستجوی سند", command=self.search_document)
        
        # زیرمنوی حساب‌ها
        self.accounts_menu = tk.Menu(self.accounting_menu, tearoff=0)
        self.accounting_menu.add_cascade(label="حساب‌ها", menu=self.accounts_menu)
        self.accounts_menu.add_command(label="تعریف حساب", command=self.define_account)
        self.accounts_menu.add_command(label="ویرایش حساب", command=self.edit_account)
        self.accounts_menu.add_command(label="حذف حساب", command=self.delete_account)
        self.accounts_menu.add_separator()
        self.accounts_menu.add_command(label="لیست حساب‌ها", command=self.list_accounts)
        self.accounts_menu.add_command(label="جستجوی حساب", command=self.search_account)
        
        # زیرمنوی اشخاص
        self.persons_menu = tk.Menu(self.accounting_menu, tearoff=0)
        self.accounting_menu.add_cascade(label="اشخاص", menu=self.persons_menu)
        self.persons_menu.add_command(label="تعریف شخص", command=self.define_person)
        self.persons_menu.add_command(label="لیست اشخاص", command=self.list_persons)
        
        # منوی فایل (سمت چپ)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="فایل", menu=self.file_menu)
        self.file_menu.add_command(label="جدید", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="باز کردن", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="ذخیره", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="ذخیره با نام", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="چاپ", command=self.print_file, accelerator="Ctrl+P")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="خروج", command=self.root.quit, accelerator="Alt+F4")
        
        # تنظیم کلیدهای میانبر
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """تنظیم کلیدهای میانبر"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-p>', lambda e: self.print_file())
        self.root.bind('<F1>', lambda e: self.show_help())
    
    # توابع منوی فایل
    def new_file(self):
        messagebox.showinfo("جدید", "فایل جدید ایجاد شد")
    
    def open_file(self):
        messagebox.showinfo("باز کردن", "فایل باز شد")
    
    def save_file(self):
        messagebox.showinfo("ذخیره", "فایل ذخیره شد")
    
    def save_as_file(self):
        messagebox.showinfo("ذخیره با نام", "فایل با نام جدید ذخیره شد")
    
    def print_file(self):
        messagebox.showinfo("چاپ", "فایل چاپ شد")
    
    # توابع منوی حسابداری - اسناد
    def new_document(self):
        messagebox.showinfo("سند جدید", "سند جدید ایجاد شد")
    
    def edit_document(self):
        messagebox.showinfo("ویرایش سند", "سند ویرایش شد")
    
    def delete_document(self):
        if messagebox.askyesno("حذف سند", "آیا مطمئن هستید؟"):
            messagebox.showinfo("حذف سند", "سند حذف شد")
    
    def list_documents(self):
        messagebox.showinfo("لیست اسناد", "لیست اسناد نمایش داده شد")
    
    def search_document(self):
        messagebox.showinfo("جستجوی سند", "جستجوی سند انجام شد")
    
    # توابع منوی حسابداری - حساب‌ها
    def define_account(self):
        messagebox.showinfo("تعریف حساب", "حساب جدید تعریف شد")
    
    def edit_account(self):
        messagebox.showinfo("ویرایش حساب", "حساب ویرایش شد")
    
    def delete_account(self):
        if messagebox.askyesno("حذف حساب", "آیا مطمئن هستید؟"):
            messagebox.showinfo("حذف حساب", "حساب حذف شد")
    
    def list_accounts(self):
        messagebox.showinfo("لیست حساب‌ها", "لیست حساب‌ها نمایش داده شد")
    
    def search_account(self):
        messagebox.showinfo("جستجوی حساب", "جستجوی حساب انجام شد")
    
    # توابع منوی اشخاص
    def define_person(self):
        messagebox.showinfo("تعریف شخص", "شخص جدید تعریف شد")
    
    def list_persons(self):
        messagebox.showinfo("لیست اشخاص", "لیست اشخاص نمایش داده شد")
    
    # توابع منوی گزارشات
    def trial_balance(self):
        messagebox.showinfo("تراز آزمایشی", "گزارش تراز آزمایشی")
    
    def balance_sheet(self):
        messagebox.showinfo("ترازنامه", "گزارش ترازنامه")
    
    def profit_loss(self):
        messagebox.showinfo("سود و زیان", "گزارش سود و زیان")
    
    def account_statement(self):
        messagebox.showinfo("گردش حساب", "گزارش گردش حساب")
    
    def general_ledger(self):
        messagebox.showinfo("دفتر کل", "گزارش دفتر کل")
    
    # توابع منوی تنظیمات
    def general_settings(self):
        messagebox.showinfo("تنظیمات", "تنظیمات عمومی")
    
    def backup(self):
        messagebox.showinfo("پشتیبان‌گیری", "پشتیبان‌گیری انجام شد")
    
    def restore(self):
        messagebox.showinfo("بازیابی", "بازیابی انجام شد")
    
    # توابع منوی راهنما
    def show_help(self):
        help_text = """
راهنمای استفاده از نرم‌افزار حسابداری

منوی فایل:
- جدید: ایجاد فایل جدید
- باز کردن: باز کردن فایل موجود
- ذخیره: ذخیره فایل فعلی

منوی حسابداری:
- اسناد: مدیریت اسناد حسابداری
- حساب‌ها: مدیریت حساب‌های مالی
- اشخاص: مدیریت اطلاعات اشخاص

منوی گزارشات:
- تراز آزمایشی: نمایش تراز آزمایشی
- ترازنامه: نمایش ترازنامه
- سود و زیان: نمایش گزارش سود و زیان

کلیدهای میانبر:
Ctrl+N: فایل جدید
Ctrl+O: باز کردن فایل
Ctrl+S: ذخیره فایل
F1: راهنما
        """
        messagebox.showinfo("راهنما", help_text)
    
    def about(self):
        about_text = f"""
{self.config.app_name}
نسخه {self.config.version}

نرم‌افزار حسابداری حرفه‌ای
با پشتیبانی کامل از زبان فارسی

توسعه‌دهنده: {self.config.author}
سال تولید: 2024
        """
        messagebox.showinfo("درباره برنامه", about_text)

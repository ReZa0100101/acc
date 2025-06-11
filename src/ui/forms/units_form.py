"""
فرم واحدهای اندازه گیری
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_form import BaseForm
from ...database.database_manager import DatabaseManager

class UnitsForm(BaseForm):
    """فرم واحدهای اندازه گیری"""
    
    def __init__(self, parent, config):
        self.db_manager = DatabaseManager(config)
        super().__init__(parent, config, "واحدهای اندازه گیری", 600, 500)
        self.create_form()
        self.load_units()
        self.selected_unit_id = None
    
    def create_form(self):
        """ایجاد فرم"""
        # فریم اصلی
        main_frame = tk.Frame(self.window, bg='#F5F5F5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # نوار ابزار بالایی
        self.create_toolbar(main_frame)
        
        # فریم فیلدهای ورودی
        input_frame = tk.Frame(main_frame, bg='#F5F5F5')
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # فیلد نام واحد
        name_frame = tk.Frame(input_frame, bg='#F5F5F5')
        name_frame.pack(fill=tk.X, pady=5)
        
        name_label = tk.Label(
            name_frame,
            text="نام واحد *",
            font=self.config.fonts['persian_text'],
            bg='#F5F5F5',
            anchor='e'
        )
        name_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=self.config.fonts['persian_text'],
            justify='right',
            width=40,
            relief=tk.SOLID,
            bd=1
        )
        self.name_entry.pack(side=tk.RIGHT, padx=(0, 15))
        
        # فیلد شناسه واحد
        symbol_frame = tk.Frame(input_frame, bg='#F5F5F5')
        symbol_frame.pack(fill=tk.X, pady=5)
        
        symbol_label = tk.Label(
            symbol_frame,
            text="شناسه واحد :",
            font=self.config.fonts['persian_text'],
            bg='#F5F5F5',
            anchor='e'
        )
        symbol_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = tk.Entry(
            symbol_frame,
            textvariable=self.symbol_var,
            font=self.config.fonts['persian_text'],
            justify='right',
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        self.symbol_entry.pack(side=tk.RIGHT, padx=(0, 15))
        
        # دکمه انتخاب از لیست
        select_btn = tk.Button(
            symbol_frame,
            text="انتخاب از لیست",
            font=self.config.fonts['button'],
            bg='#E0E0E0',
            command=self.select_from_list,
            relief=tk.RAISED,
            bd=2
        )
        select_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # فریم دکمه‌های ذخیره و لغو
        button_frame = tk.Frame(main_frame, bg='#F5F5F5')
        button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # دکمه لغو
        cancel_btn = tk.Button(
            button_frame,
            text="لغو (F12)",
            font=self.config.fonts['button'],
            bg='#E8E8E8',
            fg='black',
            command=self.close_window,
            width=12,
            relief=tk.RAISED,
            bd=2
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # دکمه ذخیره
        save_btn = tk.Button(
            button_frame,
            text="ذخیره (F9)",
            font=self.config.fonts['button'],
            bg='#4CAF50',
            fg='white',
            command=self.save_unit,
            width=12,
            relief=tk.RAISED,
            bd=2
        )
        save_btn.pack(side=tk.LEFT)
        
        # فریم جدول
        table_frame = tk.Frame(main_frame, bg='#F5F5F5')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ایجاد جدول
        self.create_units_table(table_frame)
        
        # فوکس روی فیلد نام
        self.name_entry.focus_set()
        
        # تنظیم کلیدهای میانبر
        self.setup_shortcuts()
    
    def create_toolbar(self, parent):
        """ایجاد نوار ابزار"""
        toolbar = tk.Frame(parent, bg='#E0E0E0', height=50)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        toolbar.pack_propagate(False)
        
        # دکمه حذف (سمت راست)
        delete_btn = tk.Button(
            toolbar,
            text="🗑 حذف (Del)",
            font=self.config.fonts['button'],
            bg='#F44336',
            fg='white',
            command=self.delete_unit,
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5
        )
        delete_btn.pack(side=tk.RIGHT, padx=5, pady=8)
        
        # دکمه ویرایش
        edit_btn = tk.Button(
            toolbar,
            text="✏ ویرایش (F2)",
            font=self.config.fonts['button'],
            bg='#FF9800',
            fg='white',
            command=self.edit_unit,
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5
        )
        edit_btn.pack(side=tk.RIGHT, padx=5, pady=8)
        
        # دکمه جدید
        new_btn = tk.Button(
            toolbar,
            text="➕ جدید (F1)",
            font=self.config.fonts['button'],
            bg='#4CAF50',
            fg='white',
            command=self.new_unit,
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5
        )
        new_btn.pack(side=tk.RIGHT, padx=5, pady=8)
        
        # دکمه چاپ لیست (سمت چپ)
        print_btn = tk.Button(
            toolbar,
            text="🖨 چاپ لیست",
            font=self.config.fonts['button'],
            bg='#2196F3',
            fg='white',
            command=self.print_list,
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5
        )
        print_btn.pack(side=tk.LEFT, padx=5, pady=8)
    
    def create_units_table(self, parent):
        """ایجاد جدول واحدها"""
        # فریم برای جدول
        table_container = tk.Frame(parent, bg='white', relief=tk.SOLID, bd=1)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # ایجاد Treeview
        columns = ('symbol', 'code')
        self.units_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='tree headings',
            height=15
        )
        
        # تنظیم ستون‌ها از راست به چپ
        self.units_tree.heading('#0', text='واحد', anchor='center')
        self.units_tree.heading('symbol', text='شناسه', anchor='center')
        self.units_tree.heading('code', text='کد / خدمات', anchor='center')
        
        self.units_tree.column('#0', width=200, anchor='e')
        self.units_tree.column('symbol', width=100, anchor='center')
        self.units_tree.column('code', width=150, anchor='center')
        
        # تنظیم استایل
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=self.config.fonts['persian_text'],
                       background='#E3F2FD')
        style.configure("Treeview", 
                       font=self.config.fonts['persian_text'],
                       rowheight=25)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.units_tree.yview)
        self.units_tree.configure(yscrollcommand=scrollbar.set)
        
        # قرارگیری
        self.units_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # رویداد انتخاب
        self.units_tree.bind('<<TreeviewSelect>>', self.on_unit_select)
        self.units_tree.bind('<Double-1>', self.edit_unit)
    
    def load_units(self):
        """بارگذاری واحدها"""
        try:
            # پاک کردن جدول
            for item in self.units_tree.get_children():
                self.units_tree.delete(item)
            
            # دریافت واحدها
            units = self.db_manager.get_records('units')
            
            # اضافه کردن به جدول
            for i, unit in enumerate(units, 1):
                self.units_tree.insert(
                    '', 'end',
                    text=unit['name'],
                    values=(unit['symbol'] or '', '0'),
                    tags=(unit['id'],)
                )
                
        except Exception as e:
            print(f"خطا در بارگذاری واحدها: {e}")
    
    def select_from_list(self):
        """انتخاب از لیست"""
        messagebox.showinfo("انتخاب از لیست", "این قابلیت در نسخه‌های بعدی اضافه خواهد شد", parent=self.window)
    
    def print_list(self):
        """چاپ لیست واحدها"""
        messagebox.showinfo("چاپ", "عملیات چاپ لیست واحدها", parent=self.window)
    
    def on_unit_select(self, event):
        """رویداد انتخاب واحد"""
        selection = self.units_tree.selection()
        if selection:
            item = selection[0]
            tags = self.units_tree.item(item)['tags']
            if tags:
                self.selected_unit_id = int(tags[0])
    
    def new_unit(self):
        """واحد جدید"""
        self.clear_form()
    
    def edit_unit(self, event=None):
        """ویرایش واحد"""
        if not self.selected_unit_id:
            self.show_warning_message("لطفاً یک واحد را انتخاب کنید")
            return
        
        try:
            units = self.db_manager.get_records('units', 'id = ?', [self.selected_unit_id])
            if units:
                unit = units[0]
                self.name_var.set(unit['name'])
                self.symbol_var.set(unit['symbol'] or '')
        except Exception as e:
            self.show_error_message(f"خطا در بارگذاری واحد: {str(e)}")
    
    def delete_unit(self):
        """حذف واحد"""
        if not self.selected_unit_id:
            self.show_warning_message("لطفاً یک واحد را انتخاب کنید")
            return
        
        if messagebox.askyesno("تأیید حذف", "آیا مطمئن هستید؟", parent=self.window):
            try:
                self.db_manager.delete_record('units', 'id = ?', [self.selected_unit_id])
                self.show_success_message("واحد حذف شد")
                self.load_units()
                self.clear_form()
            except Exception as e:
                self.show_error_message(f"خطا در حذف واحد: {str(e)}")
    
    def save_unit(self):
        """ذخیره واحد"""
        if not self.name_var.get().strip():
            self.show_error_message("نام واحد الزامی است")
            return
        
        try:
            unit_data = {
                'name': self.name_var.get().strip(),
                'symbol': self.symbol_var.get().strip(),
                'description': ''
            }
            
            if self.selected_unit_id:
                # ویرایش
                self.db_manager.update_record('units', unit_data, f"id = {self.selected_unit_id}")
                self.show_success_message("واحد ویرایش شد")
            else:
                # جدید
                self.db_manager.insert_record('units', unit_data)
                self.show_success_message("واحد ثبت شد")
            
            self.load_units()
            self.clear_form()
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                self.show_error_message("واحد با این نام وجود دارد")
            else:
                self.show_error_message(f"خطا: {str(e)}")
    
    def clear_form(self):
        """پاک کردن فرم"""
        self.name_var.set("")
        self.symbol_var.set("")
        self.selected_unit_id = None
        self.name_entry.focus_set()
    
    def setup_shortcuts(self):
        """تنظیم کلیدهای میانبر"""
        self.window.bind('<F1>', lambda e: self.new_unit())
        self.window.bind('<F2>', lambda e: self.edit_unit())
        self.window.bind('<Delete>', lambda e: self.delete_unit())
        self.window.bind('<F9>', lambda e: self.save_unit())
        self.window.bind('<F12>', lambda e: self.close_window())

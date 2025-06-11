"""
فرم تعریف انبار - طراحی مطابق تصویر
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_form import BaseForm
from ...database.database_manager import DatabaseManager

class WarehouseForm(BaseForm):
    """فرم تعریف انبار"""
    
    def __init__(self, parent, config):
        self.db_manager = DatabaseManager(config)
        super().__init__(parent, config, "انبارها", 600, 500)
        self.create_form()
        self.load_warehouses()
        self.selected_warehouse_id = None
    
    def create_form(self):
        """ایجاد فرم"""
        # حذف عنوان پیش‌فرض
        # self.create_title_frame("انبارها")
        
        # فریم اصلی
        main_frame = tk.Frame(self.window, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # نوار ابزار بالایی
        self.create_toolbar(main_frame)
        
        # فریم فیلدهای ورودی
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # فیلد نام انبار
        name_frame = tk.Frame(input_frame, bg='white')
        name_frame.pack(fill=tk.X, pady=5)
        
        name_label = tk.Label(
            name_frame,
            text="نام انبار *",
            font=self.config.fonts['persian_text'],
            bg='white',
            anchor='e'
        )
        name_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=self.config.fonts['persian_text'],
            justify='right',
            width=50
        )
        self.name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 10))
        
        # فریم دکمه‌های ذخیره و لغو
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # دکمه لغو
        cancel_btn = tk.Button(
            button_frame,
            text="لغو (F12)",
            font=self.config.fonts['button'],
            bg='#E0E0E0',
            command=self.close_window,
            width=12
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # دکمه ذخیره
        save_btn = tk.Button(
            button_frame,
            text="ذخیره (F9)",
            font=self.config.fonts['button'],
            bg='#90EE90',
            command=self.save_warehouse,
            width=12
        )
        save_btn.pack(side=tk.LEFT)
        
        # فریم جدول
        table_frame = tk.Frame(main_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ایجاد جدول
        self.create_warehouse_table(table_frame)
        
        # فوکس روی فیلد نام
        self.name_entry.focus_set()
        
        # تنظیم کلیدهای میانبر
        self.setup_shortcuts()
    
    def create_toolbar(self, parent):
        """ایجاد نوار ابزار"""
        toolbar = tk.Frame(parent, bg='#F0F0F0', height=40)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        # دکمه حذف
        delete_btn = tk.Button(
            toolbar,
            text="✖ حذف (Del)",
            font=self.config.fonts['button'],
            bg='#FF6B6B',
            fg='white',
            command=self.delete_warehouse,
            relief=tk.RAISED,
            bd=2
        )
        delete_btn.pack(side=tk.RIGHT, padx=2, pady=5)
        
        # دکمه ویرایش
        edit_btn = tk.Button(
            toolbar,
            text="✏ ویرایش (F2)",
            font=self.config.fonts['button'],
            bg='#FFB347',
            command=self.edit_warehouse,
            relief=tk.RAISED,
            bd=2
        )
        edit_btn.pack(side=tk.RIGHT, padx=2, pady=5)
        
        # دکمه جدید
        new_btn = tk.Button(
            toolbar,
            text="➕ جدید (F1)",
            font=self.config.fonts['button'],
            bg='#90EE90',
            command=self.new_warehouse,
            relief=tk.RAISED,
            bd=2
        )
        new_btn.pack(side=tk.RIGHT, padx=2, pady=5)
    
    def create_warehouse_table(self, parent):
        """ایجاد جدول انبارها"""
        # فریم برای جدول
        table_container = tk.Frame(parent, bg='white')
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # ایجاد Treeview
        columns = ('count',)
        self.warehouse_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='tree headings',
            height=15
        )
        
        # تنظیم ستون‌ها
        self.warehouse_tree.heading('#0', text='انبار', anchor='center')
        self.warehouse_tree.heading('count', text='تعداد کالا', anchor='center')
        
        self.warehouse_tree.column('#0', width=300, anchor='e')
        self.warehouse_tree.column('count', width=100, anchor='center')
        
        # اضافه کردن ستون ردیف
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.config.fonts['persian_text'])
        style.configure("Treeview", font=self.config.fonts['persian_text'])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.warehouse_tree.yview)
        self.warehouse_tree.configure(yscrollcommand=scrollbar.set)
        
        # قرارگیری
        self.warehouse_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # رویداد انتخاب
        self.warehouse_tree.bind('<<TreeviewSelect>>', self.on_warehouse_select)
        self.warehouse_tree.bind('<Double-1>', self.edit_warehouse)
    
    def load_warehouses(self):
        """بارگذاری انبارها"""
        try:
            # پاک کردن جدول
            for item in self.warehouse_tree.get_children():
                self.warehouse_tree.delete(item)
            
            # دریافت انبارها
            warehouses = self.db_manager.get_records('warehouses')
            
            # اضافه کردن به جدول
            for i, warehouse in enumerate(warehouses, 1):
                # محاسبه تعداد کالا (فعلاً 0)
                item_count = 0
                
                self.warehouse_tree.insert(
                    '', 'end',
                    text=warehouse['name'],
                    values=(item_count,),
                    tags=(warehouse['id'],)
                )
                
        except Exception as e:
            print(f"خطا در بارگذاری انبارها: {e}")
    
    def on_warehouse_select(self, event):
        """رویداد انتخاب انبار"""
        selection = self.warehouse_tree.selection()
        if selection:
            item = selection[0]
            tags = self.warehouse_tree.item(item)['tags']
            if tags:
                self.selected_warehouse_id = int(tags[0])
    
    def new_warehouse(self):
        """انبار جدید"""
        self.clear_form()
    
    def edit_warehouse(self, event=None):
        """ویرایش انبار"""
        if not self.selected_warehouse_id:
            self.show_warning_message("لطفاً یک انبار را انتخاب کنید")
            return
        
        try:
            warehouses = self.db_manager.get_records('warehouses', 'id = ?', [self.selected_warehouse_id])
            if warehouses:
                warehouse = warehouses[0]
                self.name_var.set(warehouse['name'])
        except Exception as e:
            self.show_error_message(f"خطا در بارگذاری انبار: {str(e)}")
    
    def delete_warehouse(self):
        """حذف انبار"""
        if not self.selected_warehouse_id:
            self.show_warning_message("لطفاً یک انبار را انتخاب کنید")
            return
        
        if messagebox.askyesno("تأیید حذف", "آیا مطمئن هستید؟", parent=self.window):
            try:
                self.db_manager.delete_record('warehouses', 'id = ?', [self.selected_warehouse_id])
                self.show_success_message("انبار حذف شد")
                self.load_warehouses()
                self.clear_form()
            except Exception as e:
                self.show_error_message(f"خطا در حذف انبار: {str(e)}")
    
    def save_warehouse(self):
        """ذخیره انبار"""
        if not self.name_var.get().strip():
            self.show_error_message("نام انبار الزامی است")
            return
        
        try:
            warehouse_data = {'name': self.name_var.get().strip()}
            
            if self.selected_warehouse_id:
                # ویرایش
                self.db_manager.update_record('warehouses', warehouse_data, f"id = {self.selected_warehouse_id}")
                self.show_success_message("انبار ویرایش شد")
            else:
                # جدید
                self.db_manager.insert_record('warehouses', warehouse_data)
                self.show_success_message("انبار ثبت شد")
            
            self.load_warehouses()
            self.clear_form()
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                self.show_error_message("انبار با این نام وجود دارد")
            else:
                self.show_error_message(f"خطا: {str(e)}")
    
    def clear_form(self):
        """پاک کردن فرم"""
        self.name_var.set("")
        self.selected_warehouse_id = None
        self.name_entry.focus_set()
    
    def setup_shortcuts(self):
        """تنظیم کلیدهای میانبر"""
        self.window.bind('<F1>', lambda e: self.new_warehouse())
        self.window.bind('<F2>', lambda e: self.edit_warehouse())
        self.window.bind('<Delete>', lambda e: self.delete_warehouse())
        self.window.bind('<F9>', lambda e: self.save_warehouse())
        self.window.bind('<F12>', lambda e: self.close_window())

"""
فرم تعریف گروه کالا و خدمات - طراحی بهبود یافته
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_form import BaseForm
from ...database.database_manager import DatabaseManager

class ProductGroupForm(BaseForm):
    """فرم تعریف گروه کالا و خدمات"""
    
    def __init__(self, parent, config):
        self.db_manager = DatabaseManager(config)
        super().__init__(parent, config, "گروه کالا", 700, 600)
        self.create_form()
        self.load_groups()
        self.selected_group_id = None
    
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
        
        # فیلد نام گروه
        name_frame = tk.Frame(input_frame, bg='#F5F5F5')
        name_frame.pack(fill=tk.X, pady=5)
        
        name_label = tk.Label(
            name_frame,
            text="نام گروه *",
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
            width=60,
            relief=tk.SOLID,
            bd=1
        )
        self.name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 15))
        
        # فیلد توضیحات
        desc_frame = tk.Frame(input_frame, bg='#F5F5F5')
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = tk.Label(
            desc_frame,
            text="توضیحات :",
            font=self.config.fonts['persian_text'],
            bg='#F5F5F5',
            anchor='ne'
        )
        desc_label.pack(side=tk.RIGHT, padx=(0, 10), anchor='n')
        
        self.desc_text = tk.Text(
            desc_frame,
            font=self.config.fonts['persian_text'],
            height=3,
            width=60,
            relief=tk.SOLID,
            bd=1
        )
        self.desc_text.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 15))
        
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
            command=self.save_group,
            width=12,
            relief=tk.RAISED,
            bd=2
        )
        save_btn.pack(side=tk.LEFT)
        
        # فریم جدول
        table_frame = tk.Frame(main_frame, bg='#F5F5F5')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ایجاد جدول
        self.create_group_table(table_frame)
        
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
            command=self.delete_group,
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
            command=self.edit_group,
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
            command=self.new_group,
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
    
    def create_group_table(self, parent):
        """ایجاد جدول گروه‌ها"""
        # فریم برای جدول
        table_container = tk.Frame(parent, bg='white', relief=tk.SOLID, bd=1)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # ایجاد Treeview با ستون‌های از راست به چپ
        columns = ('description', 'subgroup_count')
        self.group_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='tree headings',
            height=15
        )
        
        # تنظیم ستون‌ها از راست به چپ
        self.group_tree.heading('#0', text='گروه کالا یا خدمات', anchor='center')
        self.group_tree.heading('subgroup_count', text='تعداد زیرگروه', anchor='center')
        self.group_tree.heading('description', text='توضیحات', anchor='center')
        
        self.group_tree.column('#0', width=300, anchor='e')
        self.group_tree.column('subgroup_count', width=120, anchor='center')
        self.group_tree.column('description', width=250, anchor='e')
        
        # تنظیم استایل
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=self.config.fonts['persian_text'],
                       background='#E3F2FD')
        style.configure("Treeview", 
                       font=self.config.fonts['persian_text'],
                       rowheight=25)
        style.configure("Treeview", fieldbackground='white')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.group_tree.yview)
        self.group_tree.configure(yscrollcommand=scrollbar.set)
        
        # قرارگیری
        self.group_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # رویداد انتخاب
        self.group_tree.bind('<<TreeviewSelect>>', self.on_group_select)
        self.group_tree.bind('<Double-1>', self.edit_group)
    
    def load_groups(self):
        """بارگذاری گروه‌ها"""
        try:
            # پاک کردن جدول
            for item in self.group_tree.get_children():
                self.group_tree.delete(item)
            
            # دریافت گروه‌ها
            groups = self.db_manager.get_records('product_groups')
            
            # اضافه کردن به جدول
            for i, group in enumerate(groups, 1):
                # محاسبه تعداد زیرگروه
                subgroups = self.db_manager.get_records('product_groups', 'parent_id = ?', [group['id']])
                subgroup_count = len(subgroups)
                
                self.group_tree.insert(
                    '', 'end',
                    text=group['name'],
                    values=(group['description'] or '', subgroup_count),
                    tags=(group['id'],)
                )
                
        except Exception as e:
            print(f"خطا در بارگذاری گروه‌ها: {e}")
    
    def print_list(self):
        """چاپ لیست گروه‌ها"""
        messagebox.showinfo("چاپ", "عملیات چاپ لیست گروه‌ها", parent=self.window)
    
    def on_group_select(self, event):
        """رویداد انتخاب گروه"""
        selection = self.group_tree.selection()
        if selection:
            item = selection[0]
            tags = self.group_tree.item(item)['tags']
            if tags:
                self.selected_group_id = int(tags[0])
    
    def new_group(self):
        """گروه جدید"""
        self.clear_form()
    
    def edit_group(self, event=None):
        """ویرایش گروه"""
        if not self.selected_group_id:
            self.show_warning_message("لطفاً یک گروه را انتخاب کنید")
            return
        
        try:
            groups = self.db_manager.get_records('product_groups', 'id = ?', [self.selected_group_id])
            if groups:
                group = groups[0]
                self.name_var.set(group['name'])
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.insert("1.0", group['description'] or '')
        except Exception as e:
            self.show_error_message(f"خطا در بارگذاری گروه: {str(e)}")
    
    def delete_group(self):
        """حذف گروه"""
        if not self.selected_group_id:
            self.show_warning_message("لطفاً یک گروه را انتخاب کنید")
            return
        
        if messagebox.askyesno("تأیید حذف", "آیا مطمئن هستید؟", parent=self.window):
            try:
                # بررسی وجود زیرگروه
                subgroups = self.db_manager.get_records('product_groups', 'parent_id = ?', [self.selected_group_id])
                if subgroups:
                    self.show_error_message("این گروه دارای زیرگروه است")
                    return
                
                self.db_manager.delete_record('product_groups', 'id = ?', [self.selected_group_id])
                self.show_success_message("گروه حذف شد")
                self.load_groups()
                self.clear_form()
            except Exception as e:
                self.show_error_message(f"خطا در حذف گروه: {str(e)}")
    
    def save_group(self):
        """ذخیره گروه"""
        if not self.name_var.get().strip():
            self.show_error_message("نام گروه الزامی است")
            return
        
        try:
            group_data = {
                'name': self.name_var.get().strip(),
                'description': self.desc_text.get("1.0", tk.END).strip(),
                'parent_id': None
            }
            
            if self.selected_group_id:
                # ویرایش
                self.db_manager.update_record('product_groups', group_data, f"id = {self.selected_group_id}")
                self.show_success_message("گروه ویرایش شد")
            else:
                # جدید
                self.db_manager.insert_record('product_groups', group_data)
                self.show_success_message("گروه ثبت شد")
            
            self.load_groups()
            self.clear_form()
            
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                self.show_error_message("گروه با این نام وجود دارد")
            else:
                self.show_error_message(f"خطا: {str(e)}")
    
    def clear_form(self):
        """پاک کردن فرم"""
        self.name_var.set("")
        self.desc_text.delete("1.0", tk.END)
        self.selected_group_id = None
        self.name_entry.focus_set()
    
    def setup_shortcuts(self):
        """تنظیم کلیدهای میانبر"""
        self.window.bind('<F1>', lambda e: self.new_group())
        self.window.bind('<F2>', lambda e: self.edit_group())
        self.window.bind('<Delete>', lambda e: self.delete_group())
        self.window.bind('<F9>', lambda e: self.save_group())
        self.window.bind('<F12>', lambda e: self.close_window())

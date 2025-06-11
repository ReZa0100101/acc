"""
فرم لیست کالا و خدمات - مطابق تصویر
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_form import BaseForm
from ...database.database_manager import DatabaseManager
from ...utils.persian_utils import english_to_persian_digits, format_currency

class ProductsListForm(BaseForm):
    """فرم لیست کالا و خدمات"""
    
    def __init__(self, parent, config):
        self.db_manager = DatabaseManager(config)
        super().__init__(parent, config, "لیست کالا و خدمات", 1200, 700)
        self.create_form()
        self.load_data()
        self.selected_product_id = None
    
    def create_form(self):
        """ایجاد فرم"""
        # تنظیم فونت
        default_font = ('Iranian Sans', 10, 'normal')
        self.window.option_add('*Font', default_font)
        
        # فریم اصلی
        main_frame = tk.Frame(self.window, bg='#F0F0F0')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # فریم فیلترها در بالا
        filter_frame = tk.Frame(main_frame, bg='#F0F0F0', height=50)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        filter_frame.pack_propagate(False)
        
        # فیلد جستجو (وسط)
        search_frame = tk.Frame(filter_frame, bg='#F0F0F0')
        search_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20, pady=10)
        
        search_label = tk.Label(
            search_frame,
            text=": نام کالا یا خدمات",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F0F0F0'
        )
        search_label.pack(side=tk.RIGHT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            relief=tk.SOLID,
            bd=1
        )
        self.search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # کمبوباکس گروه (سمت راست)
        group_frame = tk.Frame(filter_frame, bg='#F0F0F0')
        group_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        group_label = tk.Label(
            group_frame,
            text=": گروه",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F0F0F0'
        )
        group_label.pack(side=tk.RIGHT, padx=5)
        
        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(
            group_frame,
            textvariable=self.group_var,
            font=('Iranian Sans', 10, 'normal'),
            width=15,
            justify='right',
            state="readonly"
        )
        self.group_combo.pack(side=tk.RIGHT, padx=5)
        self.group_combo.bind('<<ComboboxSelected>>', self.on_group_filter)
        
        # فریم جدول
        table_frame = tk.Frame(main_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ایجاد جدول
        self.create_products_table(table_frame)
        
        # فریم دکمه‌ها در پایین
        buttons_frame = tk.Frame(main_frame, bg='#F0F0F0', height=60)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        buttons_frame.pack_propagate(False)
        
        # دکمه چاپ (سمت چپ)
        print_btn = tk.Button(
            buttons_frame,
            text="📄 چاپ (F5)",
            font=('Iranian Sans', 10, 'normal'),
            bg='#9E9E9E',
            fg='white',
            command=self.print_list,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8
        )
        print_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # دکمه‌های اصلی (سمت راست)
        # حذف (قرمز)
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑 حذف (Del)",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F44336',
            fg='white',
            command=self.delete_product,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8
        )
        delete_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # ویرایش (نارنجی)
        edit_btn = tk.Button(
            buttons_frame,
            text="✏ ویرایش (F2)",
            font=('Iranian Sans', 10, 'normal'),
            bg='#FF9800',
            fg='white',
            command=self.edit_product,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8
        )
        edit_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # گردش کالا (آبی)
        circulation_btn = tk.Button(
            buttons_frame,
            text="📊 گردش کالا",
            font=('Iranian Sans', 10, 'normal'),
            bg='#2196F3',
            fg='white',
            command=self.show_circulation,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8
        )
        circulation_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # جدید (سبز)
        new_btn = tk.Button(
            buttons_frame,
            text="➕ جدید (F1)",
            font=('Iranian Sans', 10, 'normal'),
            bg='#4CAF50',
            fg='white',
            command=self.new_product,
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=8
        )
        new_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # بارگذاری گروه‌ها
        self.load_groups()
        
        # تنظیم کلیدهای میانبر
        self.setup_shortcuts()
    
    def create_products_table(self, parent):
        """ایجاد جدول محصولات"""
        # فریم برای جدول و اسکرول‌بار
        table_container = tk.Frame(parent, bg='white')
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # تعریف ستون‌ها (از راست به چپ مطابق تصویر)
        columns = (
            'product_service_id',  # شناسه کالا و خدمت
            'vat_rate',           # نرخ ارزش افزوده  
            'current_stock',      # موجودی فعلی
            'description',        # توضیحات
            'use_in_invoice',     # استفاده در فاکتور
            'unit',              # واحد
            'sell_price',        # قیمت فروش
            'title',             # عنوان کالا / خدمات
            'group',             # گروه
            'id'                 # شناسه
        )
        
        self.products_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='headings',  # تغییر از 'tree headings' به 'headings'
            height=20
        )
        
        # اضافه کردن ستون ردیف به صورت جداگانه
        self.products_tree.insert_column(0, 'row_num', text='ردیف', width=50, anchor='center')
        
        # تنظیم هدرهای ستون‌ها (از راست به چپ)
        self.products_tree.heading('#0', text='ردیف', anchor='center')
        self.products_tree.heading('id', text='شناسه', anchor='center')
        self.products_tree.heading('group', text='گروه', anchor='center')
        self.products_tree.heading('title', text='عنوان کالا / خدمات', anchor='center')
        self.products_tree.heading('sell_price', text='قیمت فروش', anchor='center')
        self.products_tree.heading('unit', text='واحد', anchor='center')
        self.products_tree.heading('use_in_invoice', text='استفاده در فاکتور', anchor='center')
        self.products_tree.heading('description', text='توضیحات', anchor='center')
        self.products_tree.heading('current_stock', text='موجودی فعلی', anchor='center')
        self.products_tree.heading('vat_rate', text='نرخ ارزش افزوده', anchor='center')
        self.products_tree.heading('product_service_id', text='شناسه کالا و خدمت', anchor='center')
        
        # تنظیم عرض ستون‌ها
        self.products_tree.column('#0', width=50, anchor='center')
        self.products_tree.column('id', width=80, anchor='center')
        self.products_tree.column('group', width=100, anchor='e')
        self.products_tree.column('title', width=150, anchor='e')
        self.products_tree.column('sell_price', width=100, anchor='e')
        self.products_tree.column('unit', width=80, anchor='center')
        self.products_tree.column('use_in_invoice', width=120, anchor='center')
        self.products_tree.column('description', width=120, anchor='e')
        self.products_tree.column('current_stock', width=100, anchor='center')
        self.products_tree.column('vat_rate', width=120, anchor='center')
        self.products_tree.column('product_service_id', width=150, anchor='center')
        
        # تنظیم استایل
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=('Iranian Sans', 10, 'bold'),
                       background='#E3F2FD')
        style.configure("Treeview", 
                       font=('Iranian Sans', 10, 'normal'),
                       rowheight=25)
        
        # اسکرول‌بارها
        v_scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient=tk.HORIZONTAL, command=self.products_tree.xview)
        
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # قرارگیری
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # رویدادها
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        self.products_tree.bind('<Double-1>', self.edit_product)
    
    def load_groups(self):
        """بارگذاری گروه‌ها برای فیلتر"""
        try:
            groups = self.db_manager.get_records('product_groups')
            group_names = ['همه گروه‌ها'] + [group['name'] for group in groups]
            self.group_combo['values'] = group_names
            self.group_combo.set('همه گروه‌ها')
        except Exception as e:
            print(f"خطا در بارگذاری گروه‌ها: {e}")
    
    def load_data(self):
        """بارگذاری داده‌های محصولات"""
        try:
            # پاک کردن جدول
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            
            # کوئری پیچیده برای دریافت اطلاعات کامل
            query = """
                SELECT 
                    p.id,
                    p.name,
                    p.code,
                    p.sell_price,
                    p.buy_price,
                    p.stock_quantity,
                    p.description,
                    p.is_service,
                    pg.name as group_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN product_groups pg ON p.group_id = pg.id
                LEFT JOIN units u ON p.unit_id = u.id
                ORDER BY p.id
            """
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            products = cursor.fetchall()
            conn.close()
            
            # اضافه کردن به جدول
            for i, product in enumerate(products, 1):
                # تبدیل قیمت به فرمت فارسی
                sell_price_formatted = format_currency(product['sell_price']) if product['sell_price'] else "0"
                
                # تعیین واحد
                unit_display = product['unit_name'] or 'عدد'
                
                # تعیین گروه
                group_display = product['group_name'] or 'بدون گروه'
                
                # تعیین موجودی (فقط برای کالا)
                stock_display = english_to_persian_digits(str(int(product['stock_quantity']))) if not product['is_service'] else '-'
                
                # شناسه کالا/خدمت (کد محصول)
                product_code = english_to_persian_digits(product['code']) if product['code'] else '-'
                
                self.products_tree.insert(
                    '', 'end',
                    text=english_to_persian_digits(str(i)),  # ردیف
                    values=(
                        product_code,                    # شناسه کالا و خدمت
                        english_to_persian_digits('10'), # نرخ ارزش افزوده (پیش‌فرض)
                        stock_display,                   # موجودی فعلی
                        product['description'] or '',    # توضیحات
                        'بله',                          # استفاده در فاکتور (پیش‌فرض)
                        unit_display,                    # واحد
                        sell_price_formatted,            # قیمت فروش
                        product['name'],                 # عنوان کالا / خدمات
                        group_display,                   # گروه
                        english_to_persian_digits(str(product['id']))  # شناسه
                    ),
                    tags=(product['id'],)
                )
                
        except Exception as e:
            print(f"خطا در بارگذاری محصولات: {e}")
            messagebox.showerror("خطا", f"خطا در بارگذاری اطلاعات: {str(e)}", parent=self.window)
    
    def on_search(self, event=None):
        """جستجو در محصولات"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self.load_data()
            return
        
        try:
            # پاک کردن جدول
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            
            # جستجو در نام محصولات
            query = """
                SELECT 
                    p.id,
                    p.name,
                    p.code,
                    p.sell_price,
                    p.buy_price,
                    p.stock_quantity,
                    p.description,
                    p.is_service,
                    pg.name as group_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN product_groups pg ON p.group_id = pg.id
                LEFT JOIN units u ON p.unit_id = u.id
                WHERE p.name LIKE ? OR p.code LIKE ?
                ORDER BY p.id
            """
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
            products = cursor.fetchall()
            conn.close()
            
            # اضافه کردن نتایج به جدول
            for i, product in enumerate(products, 1):
                sell_price_formatted = format_currency(product['sell_price']) if product['sell_price'] else "0"
                unit_display = product['unit_name'] or 'عدد'
                group_display = product['group_name'] or 'بدون گروه'
                stock_display = english_to_persian_digits(str(int(product['stock_quantity']))) if not product['is_service'] else '-'
                product_code = english_to_persian_digits(product['code']) if product['code'] else '-'
                
                self.products_tree.insert(
                    '', 'end',
                    text=english_to_persian_digits(str(i)),
                    values=(
                        product_code,
                        english_to_persian_digits('10'),
                        stock_display,
                        product['description'] or '',
                        'بله',
                        unit_display,
                        sell_price_formatted,
                        product['name'],
                        group_display,
                        english_to_persian_digits(str(product['id']))
                    ),
                    tags=(product['id'],)
                )
                
        except Exception as e:
            print(f"خطا در جستجو: {e}")
    
    def on_group_filter(self, event=None):
        """فیلتر بر اساس گروه"""
        selected_group = self.group_var.get()
        if selected_group == 'همه گروه‌ها':
            self.load_data()
            return
        
        try:
            # پاک کردن جدول
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            
            # فیلتر بر اساس گروه
            query = """
                SELECT 
                    p.id,
                    p.name,
                    p.code,
                    p.sell_price,
                    p.buy_price,
                    p.stock_quantity,
                    p.description,
                    p.is_service,
                    pg.name as group_name,
                    u.name as unit_name,
                    u.symbol as unit_symbol
                FROM products p
                LEFT JOIN product_groups pg ON p.group_id = pg.id
                LEFT JOIN units u ON p.unit_id = u.id
                WHERE pg.name = ?
                ORDER BY p.id
            """
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (selected_group,))
            products = cursor.fetchall()
            conn.close()
            
            # اضافه کردن نتایج به جدول
            for i, product in enumerate(products, 1):
                sell_price_formatted = format_currency(product['sell_price']) if product['sell_price'] else "0"
                unit_display = product['unit_name'] or 'عدد'
                group_display = product['group_name'] or 'بدون گروه'
                stock_display = english_to_persian_digits(str(int(product['stock_quantity']))) if not product['is_service'] else '-'
                product_code = english_to_persian_digits(product['code']) if product['code'] else '-'
                
                self.products_tree.insert(
                    '', 'end',
                    text=english_to_persian_digits(str(i)),
                    values=(
                        product_code,
                        english_to_persian_digits('10'),
                        stock_display,
                        product['description'] or '',
                        'بله',
                        unit_display,
                        sell_price_formatted,
                        product['name'],
                        group_display,
                        english_to_persian_digits(str(product['id']))
                    ),
                    tags=(product['id'],)
                )
                
        except Exception as e:
            print(f"خطا در فیلتر گروه: {e}")
    
    def on_product_select(self, event):
        """انتخاب محصول"""
        selection = self.products_tree.selection()
        if selection:
            item = selection[0]
            tags = self.products_tree.item(item)['tags']
            if tags:
                self.selected_product_id = int(tags[0])
    
    def new_product(self):
        """محصول جدید"""
        try:
            from .products_form import ProductsForm
            form = ProductsForm(self.window, self.config)
            self.window.wait_window(form.window)
            self.load_data()  # بارگذاری مجدد داده‌ها
        except Exception as e:
            print(f"خطا در باز کردن فرم محصول جدید: {e}")
    
    def edit_product(self, event=None):
        """ویرایش محصول"""
        if not self.selected_product_id:
            messagebox.showwarning("هشدار", "لطفاً یک محصول را انتخاب کنید", parent=self.window)
            return
        
        try:
            # دریافت اطلاعات محصول
            query = """
                SELECT 
                    p.*,
                    pg.name as group_name,
                    u.name as unit_name
                FROM products p
                LEFT JOIN product_groups pg ON p.group_id = pg.id
                LEFT JOIN units u ON p.unit_id = u.id
                WHERE p.id = ?
            """
            
            conn = self.db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (self.selected_product_id,))
            product = cursor.fetchone()
            conn.close()
            
            if not product:
                messagebox.showerror("خطا", "محصول مورد نظر یافت نشد", parent=self.window)
                return
            
            # باز کردن فرم ویرایش با اطلاعات محصول
            from .products_form import ProductsForm
            form = ProductsForm(self.parent, self.config)
            
            # تنظیم اطلاعات محصول در فرم
            form.product_type.set("خدمات" if product['is_service'] else "کالا")
            form.on_type_change()  # اعمال تغییرات مربوط به نوع محصول
            
            form.code_var.set(product['code'])
            form.name_var.set(product['name'])
            form.name_entry.config(fg='black')  # تغییر رنگ متن به مشکی
            
            form.product_id_var.set(product.get('product_id', ''))
            form.sell_price_var.set(format_currency(product['sell_price']))
            form.buy_price_var.set(format_currency(product['buy_price']))
            form.weight_var.set(product.get('weight', ''))
            form.barcode_var.set(product.get('barcode', ''))
            
            # تنظیم گروه و واحد
            if product['group_name']:
                form.group_var.set(product['group_name'])
            if product['unit_name']:
                form.unit_var.set(product['unit_name'])
            
            # تنظیم توضیحات
            form.desc_text.delete("1.0", tk.END)
            if product['description']:
                form.desc_text.insert("1.0", product['description'])
                form.desc_text.config(fg='black')
            
            # تنظیم موجودی
            form.current_stock_var.set(str(int(product['stock_quantity'])))
            form.min_stock_var.set(str(int(product.get('min_stock', 0))))
            form.max_stock_var.set(str(int(product.get('max_stock', 0))))
            
            # ذخیره شناسه محصول برای ویرایش
            form.selected_product_id = self.selected_product_id
            
            # منتظر بستن فرم
            self.window.wait_window(form.window)
            self.load_data()  # بارگذاری مجدد داده‌ها
            
        except Exception as e:
            print(f"خطا در ویرایش محصول: {e}")
            messagebox.showerror("خطا", f"خطا در ویرایش محصول: {str(e)}", parent=self.window)
    
    def delete_product(self):
        """حذف محصول"""
        if not self.selected_product_id:
            messagebox.showwarning("هشدار", "لطفاً یک محصول را انتخاب کنید", parent=self.window)
            return
        
        if messagebox.askyesno("تأیید حذف", "آیا مطمئن هستید که می‌خواهید این محصول را حذف کنید؟", parent=self.window):
            try:
                self.db_manager.delete_record('products', 'id = ?', [self.selected_product_id])
                messagebox.showinfo("موفقیت", "محصول با موفقیت حذف شد", parent=self.window)
                self.load_data()
                self.selected_product_id = None
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در حذف محصول: {str(e)}", parent=self.window)
    
    def show_circulation(self):
        """نمایش گردش کالا"""
        if not self.selected_product_id:
            messagebox.showwarning("هشدار", "لطفاً یک محصول را انتخاب کنید", parent=self.window)
            return
        
        messagebox.showinfo("گردش کالا", f"نمایش گردش کالا برای محصول شناسه {self.selected_product_id}", parent=self.window)
    
    def print_list(self):
        """چاپ لیست"""
        messagebox.showinfo("چاپ", "عملیات چاپ لیست محصولات", parent=self.window)
    
    def setup_shortcuts(self):
        """تنظیم کلیدهای میانبر"""
        self.window.bind('<F1>', lambda e: self.new_product())
        self.window.bind('<F2>', lambda e: self.edit_product())
        self.window.bind('<Delete>', lambda e: self.delete_product())
        self.window.bind('<F5>', lambda e: self.print_list())
        self.window.bind('<Escape>', lambda e: self.close_window())

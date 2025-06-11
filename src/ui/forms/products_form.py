"""
فرم ثبت مشخصات کالا و خدمات - دقیقاً مطابق تصویر
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from .base_form import BaseForm
from ...database.database_manager import DatabaseManager

class ProductsForm(BaseForm):
    """فرم ثبت مشخصات کالا و خدمات"""
    
    def __init__(self, parent, config):
        self.db_manager = DatabaseManager(config)
        # تنظیم اندازه دقیق پنجره مطابق تصویر
        super().__init__(parent, config, "ثبت مشخصات کالا و خدمات", 820, 600)
        self.product_image = None
        self.selected_product_id = None  # برای ویرایش محصول
        self.create_form()
        
        # بارگذاری داده‌های پایه
        self.load_product_groups()
        self.load_units()
        self.load_warehouses()
    
    def create_form(self):
        """ایجاد فرم"""
        # تنظیم فونت کل فرم به Iranian Sans سایز 10
        default_font = ('Iranian Sans', 10, 'normal')
        self.window.option_add('*Font', default_font)
        
        # فریم اصلی
        main_frame = tk.Frame(self.window, bg='#F5F5F5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # فریم مشخصات اصلی
        specs_frame = tk.LabelFrame(
            main_frame,
            text="مشخصات اصلی",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='black',
            labelanchor='ne'
        )
        specs_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # فریم دو ستون مساوی با Grid
        columns_frame = tk.Frame(specs_frame, bg='#F5F5F5')
        columns_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # تنظیم Grid برای دو ستون مساوی
        columns_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        columns_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        
        # ستون چپ (50% عرض)  
        left_column = tk.Frame(columns_frame, bg='#F5F5F5')
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # ستون راست (50% عرض)
        right_column = tk.Frame(columns_frame, bg='#F5F5F5')
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # === ستون راست ===
        
        # ردیف 1: کالا - خدمات - کد کالا
        row1_right = tk.Frame(right_column, bg='#F5F5F5')
        row1_right.pack(fill=tk.X, pady=3)
        
        # رادیو باتن‌ها
        self.product_type = tk.StringVar(value="کالا")
        
        # کالا (سبز)
        product_radio = tk.Radiobutton(
            row1_right,
            text="کالا",
            variable=self.product_type,
            value="کالا",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='green',
            selectcolor='#F5F5F5',
            command=self.on_type_change
        )
        product_radio.pack(side=tk.RIGHT, padx=2)
        
        # خدمات
        service_radio = tk.Radiobutton(
            row1_right,
            text="خدمات",
            variable=self.product_type,
            value="خدمات",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            selectcolor='#F5F5F5',
            command=self.on_type_change
        )
        service_radio.pack(side=tk.RIGHT, padx=2)
        
        # کد کالا/خدمات
        self.code_label = tk.Label(
            row1_right,
            text=": کد کالا *",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red'
        )
        self.code_label.pack(side=tk.RIGHT, padx=(20, 2))
        
        self.code_var = tk.StringVar()
        code_entry = tk.Entry(
            row1_right,
            textvariable=self.code_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=15,
            relief=tk.SOLID,
            bd=1
        )
        code_entry.pack(side=tk.RIGHT, ipady=3)

        # validation برای فقط عدد
        def validate_code(char):
            return char.isdigit()

        code_vcmd = (self.window.register(validate_code), '%S')
        code_entry.config(validate='key', validatecommand=code_vcmd)
        
        # ردیف 2: نام کالا/خدمات
        row2_right = tk.Frame(right_column, bg='#F5F5F5')
        row2_right.pack(fill=tk.X, pady=3)
        
        self.name_label = tk.Label(
            row2_right,
            text=": نام کالا *",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red'
        )
        self.name_label.pack(side=tk.RIGHT, padx=2)
        
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(
            row2_right,
            textvariable=self.name_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            relief=tk.SOLID,
            bd=1,
            fg='gray'
        )
        self.name_entry.insert(0, "یک نام برای کالا یا خدمات وارد کنید")
        self.name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2, ipady=3)

        # رویدادهای focus برای placeholder
        def on_name_focus_in(event):
            if self.name_entry.get() == "یک نام برای کالا یا خدمات وارد کنید":
                self.name_entry.delete(0, tk.END)
                self.name_entry.config(fg='black')

        def on_name_focus_out(event):
            if self.name_entry.get() == "":
                self.name_entry.insert(0, "یک نام برای کالا یا خدمات وارد کنید")
                self.name_entry.config(fg='gray')

        self.name_entry.bind('<FocusIn>', on_name_focus_in)
        self.name_entry.bind('<FocusOut>', on_name_focus_out)
        
        # ردیف 3: شناسه کالا/خدمات
        row3_right = tk.Frame(right_column, bg='#F5F5F5')
        row3_right.pack(fill=tk.X, pady=3)

        id_label = tk.Label(
            row3_right,
            text=": شناسه کالا / خدمت",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        id_label.pack(side=tk.RIGHT, padx=2)

        # ورودی شناسه
        self.product_id_var = tk.StringVar()
        id_entry = tk.Entry(
            row3_right,
            textvariable=self.product_id_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=25,
            relief=tk.SOLID,
            bd=1
        )
        id_entry.pack(side=tk.RIGHT, padx=2, ipady=3)

        # دکمه طوسی (بعد از کادر)
        color_btn = tk.Button(
            row3_right,
            text="■",
            font=('Iranian Sans', 10, 'normal'),
            bg='#CCCCCC',
            width=2,
            height=1,
            relief=tk.SOLID,
            bd=1
        )
        color_btn.pack(side=tk.RIGHT, padx=2)
        
        # ردیف 4: قیمت فروش
        row4_right = tk.Frame(right_column, bg='#F5F5F5')
        row4_right.pack(fill=tk.X, pady=3)

        sell_price_label = tk.Label(
            row4_right,
            text=": قیمت فروش *",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red'
        )
        sell_price_label.pack(side=tk.RIGHT, padx=2)

        self.sell_price_var = tk.StringVar()
        sell_price_entry = tk.Entry(
            row4_right,
            textvariable=self.sell_price_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=15,
            relief=tk.SOLID,
            bd=1
        )
        sell_price_entry.pack(side=tk.RIGHT, padx=2, ipady=3)

        # ریال
        rial_label = tk.Label(
            row4_right,
            text="ریال",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        rial_label.pack(side=tk.RIGHT, padx=2)

        # validation و فرمت کردن قیمت فروش
        def format_price_sell(event):
            value = sell_price_entry.get().replace(',', '')
            if value.isdigit() and value:
                formatted = f"{int(value):,}"
                self.sell_price_var.set(formatted)

        def validate_price_sell(char):
            return char.isdigit()

        sell_price_vcmd = (self.window.register(validate_price_sell), '%S')
        sell_price_entry.config(validate='key', validatecommand=sell_price_vcmd)
        sell_price_entry.bind('<KeyRelease>', format_price_sell)
        
        # ردیف 5: واحد اندازه گیری
        row5_right = tk.Frame(right_column, bg='#F5F5F5')
        row5_right.pack(fill=tk.X, pady=3)

        unit_label = tk.Label(
            row5_right,
            text=": واحد اندازه گیری *",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red'
        )
        unit_label.pack(side=tk.RIGHT, padx=2)

        # کمبوباکس واحد
        self.unit_var = tk.StringVar(value="بسته")
        self.unit_combo = ttk.Combobox(
            row5_right,
            textvariable=self.unit_var,
            font=('Iranian Sans', 10, 'normal'),
            width=15,
            justify='right'
        )
        self.unit_combo.pack(side=tk.RIGHT, padx=2, ipady=3)

        # دکمه اضافه کردن
        add_unit_btn = tk.Button(
            row5_right,
            text="+",
            font=('Iranian Sans', 10, 'normal'),
            bg='#4CAF50',
            fg='white',
            width=2,
            height=1,
            relief=tk.RAISED,
            bd=1,
            command=self.open_units_form
        )
        add_unit_btn.pack(side=tk.RIGHT, padx=1)
        
        # ردیف 6: توضیحات
        row6_right = tk.Frame(right_column, bg='#F5F5F5')
        row6_right.pack(fill=tk.X, pady=3)
        
        desc_label = tk.Label(
            row6_right,
            text=": توضیحات",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        desc_label.pack(side=tk.RIGHT, anchor=tk.N, padx=2)
        
        # متن توضیحات
        self.desc_text = tk.Text(
            row6_right,
            font=('Iranian Sans', 10, 'normal'),
            height=4,
            width=40,
            relief=tk.SOLID,
            bd=1,
            bg='#FFEBCD',
            fg='gray'
        )
        self.desc_text.insert("1.0", "شرح معرفی کالا (اختیاری)")
        self.desc_text.tag_configure("right", justify='right')
        self.desc_text.tag_add("right", "1.0", "end")
        self.desc_text.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)

        # رویدادهای focus برای placeholder
        def on_desc_focus_in(event):
            current_text = self.desc_text.get("1.0", tk.END).strip()
            if current_text == "شرح معرفی کالا (اختیاری)" or current_text == "شرح معرفی خدمات (اختیاری)":
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.config(fg='black')

        def on_desc_focus_out(event):
            if self.desc_text.get("1.0", tk.END).strip() == "":
                placeholder = "شرح معرفی کالا (اختیاری)" if self.product_type.get() == "کالا" else "شرح معرفی خدمات (اختیاری)"
                self.desc_text.insert("1.0", placeholder)
                self.desc_text.config(fg='gray')
                self.desc_text.tag_configure("right", justify='right')
                self.desc_text.tag_add("right", "1.0", "end")

        self.desc_text.bind('<FocusIn>', on_desc_focus_in)
        self.desc_text.bind('<FocusOut>', on_desc_focus_out)
        
        # === ستون چپ ===
        
        # ردیف 1: گروه دسته بندی
        row1_left = tk.Frame(left_column, bg='#F5F5F5')
        row1_left.pack(fill=tk.X, pady=3)

        group_label = tk.Label(
            row1_left,
            text=": گروه دسته بندی *",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red'
        )
        group_label.pack(side=tk.RIGHT, padx=2)

        # کمبوباکس گروه
        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(
            row1_left,
            textvariable=self.group_var,
            font=('Iranian Sans', 10, 'normal'),
            width=20,
            justify='right'
        )
        self.group_combo.pack(side=tk.RIGHT, padx=2, ipady=3)

        # دکمه اضافه کردن
        add_group_btn = tk.Button(
            row1_left,
            text="+",
            font=('Iranian Sans', 10, 'normal'),
            bg='#4CAF50',
            fg='white',
            width=2,
            height=1,
            relief=tk.RAISED,
            bd=1,
            command=self.open_product_group_form
        )
        add_group_btn.pack(side=tk.RIGHT, padx=1)
        
        # ردیف 2: نرخ ارزش افزوده
        row2_left = tk.Frame(left_column, bg='#F5F5F5')
        row2_left.pack(fill=tk.X, pady=3)

        vat_label = tk.Label(
            row2_left,
            text=": نرخ ارزش افزوده",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        vat_label.pack(side=tk.RIGHT, padx=2)

        self.vat_var = tk.StringVar(value="10")
        vat_entry = tk.Entry(
            row2_left,
            textvariable=self.vat_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=10,
            relief=tk.SOLID,
            bd=1
        )
        vat_entry.pack(side=tk.RIGHT, padx=2, ipady=3)

        # درصد
        vat_percent = tk.Label(
            row2_left,
            text="درصد",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        vat_percent.pack(side=tk.RIGHT, padx=2)
        
        # ردیف 3: بارکد/ایران کد
        row3_left = tk.Frame(left_column, bg='#F5F5F5')
        row3_left.pack(fill=tk.X, pady=3)

        barcode_label = tk.Label(
            row3_left,
            text=": بارکد/ایران کد",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        barcode_label.pack(side=tk.RIGHT, padx=2)

        # آیکون بارکد (سمت چپ)
        barcode_icon = tk.Label(
            row3_left,
            text="|||",
            font=('Courier', 12, 'bold'),
            bg='#F5F5F5'
        )
        barcode_icon.pack(side=tk.LEFT, padx=2)

        # ورودی بارکد
        self.barcode_var = tk.StringVar()
        barcode_entry = tk.Entry(
            row3_left,
            textvariable=self.barcode_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        barcode_entry.pack(side=tk.RIGHT, padx=2, ipady=3)

        # validation برای فقط عدد
        def validate_barcode(char):
            return char.isdigit()

        barcode_vcmd = (self.window.register(validate_barcode), '%S')
        barcode_entry.config(validate='key', validatecommand=barcode_vcmd)
        
        # ردیف 4: وزن یک واحد
        self.row4_left = tk.Frame(left_column, bg='#F5F5F5')
        self.row4_left.pack(fill=tk.X, pady=3)

        self.weight_label = tk.Label(
            self.row4_left,
            text=": وزن یک واحد",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        self.weight_label.pack(side=tk.RIGHT, padx=2)

        self.weight_var = tk.StringVar()
        self.weight_entry = tk.Entry(
            self.row4_left,
            textvariable=self.weight_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        self.weight_entry.pack(side=tk.RIGHT, padx=2, ipady=3)

        # validation برای فقط عدد و نقطه
        def validate_weight(char):
            return char.isdigit() or char == '.'

        weight_vcmd = (self.window.register(validate_weight), '%S')
        self.weight_entry.config(validate='key', validatecommand=weight_vcmd)

        # ردیف 5: قیمت خرید
        self.row5_left = tk.Frame(left_column, bg='#F5F5F5')
        self.row5_left.pack(fill=tk.X, pady=3)

        self.buy_price_label = tk.Label(
            self.row5_left,
            text=": قیمت خرید",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        self.buy_price_label.pack(side=tk.RIGHT, padx=2)

        self.buy_price_var = tk.StringVar()
        self.buy_price_entry = tk.Entry(
            self.row5_left,
            textvariable=self.buy_price_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=15,
            relief=tk.SOLID,
            bd=1
        )
        self.buy_price_entry.pack(side=tk.RIGHT, padx=2, ipady=3)

        # ریال
        self.buy_rial_label = tk.Label(
            self.row5_left,
            text="ریال",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        self.buy_rial_label.pack(side=tk.RIGHT, padx=2)

        # validation و فرمت کردن قیمت خرید
        def format_price_buy(event):
            value = self.buy_price_entry.get().replace(',', '')
            if value.isdigit() and value:
                formatted = f"{int(value):,}"
                self.buy_price_var.set(formatted)

        def validate_price_buy(char):
            return char.isdigit()

        buy_price_vcmd = (self.window.register(validate_price_buy), '%S')
        self.buy_price_entry.config(validate='key', validatecommand=buy_price_vcmd)
        self.buy_price_entry.bind('<KeyRelease>', format_price_buy)

        # ردیف 6: چک باکس‌ها و عکس کالا
        row6_left = tk.Frame(left_column, bg='#F5F5F5')
        row6_left.pack(fill=tk.X, pady=3)

        # فریم برای چک باکس‌ها (سمت راست)
        checkboxes_frame = tk.Frame(row6_left, bg='#F5F5F5')
        checkboxes_frame.pack(side=tk.RIGHT, padx=2)

        # چک باکس‌ها زیر هم در سمت راست با چک باکس قبل از متن
        self.buyable_var = tk.BooleanVar(value=True)
        self.buyable_check = tk.Checkbutton(
            checkboxes_frame,
            text="کالای قابل خرید",
            variable=self.buyable_var,
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red',
            anchor='e',
            justify='right'
        )
        self.buyable_check.pack(side=tk.TOP, anchor='e', pady=0)

        self.sellable_var = tk.BooleanVar(value=True)
        self.sellable_check = tk.Checkbutton(
            checkboxes_frame,
            text="کالای قابل فروش",
            variable=self.sellable_var,
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red',
            anchor='e',
            justify='right'
        )
        self.sellable_check.pack(side=tk.TOP, anchor='e', pady=0)

        self.producible_var = tk.BooleanVar(value=True)
        self.producible_check = tk.Checkbutton(
            checkboxes_frame,
            text="کالای قابل تولید",
            variable=self.producible_var,
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red',
            anchor='e',
            justify='right'
        )
        self.producible_check.pack(side=tk.TOP, anchor='e', pady=0)

        # فریم برای عکس و دکمه (سمت چپ)
        image_frame = tk.Frame(row6_left, bg='#F5F5F5')
        image_frame.pack(side=tk.LEFT, padx=2)

        # کادر نمایش عکس (کوچکتر)
        self.image_label = tk.Label(
            image_frame,
            text="",
            font=('Iranian Sans', 10, 'normal'),
            bg='white',
            relief=tk.SOLID,
            bd=1,
            width=8,
            height=4
        )
        self.image_label.pack(side=tk.TOP, pady=1)

        # دکمه کلیک کنید (کوچکتر)
        click_btn = tk.Button(
            image_frame,
            text="کلیک کنید",
            font=('Iranian Sans', 10, 'normal'),
            bg='#008000',
            fg='white',
            width=8,
            height=1,
            command=self.select_image,
            relief=tk.RAISED,
            bd=1
        )
        click_btn.pack(side=tk.TOP, pady=1)
        
        # فریم انبار و موجودی
        self.inventory_frame = tk.LabelFrame(
            main_frame,
            text="انبار و موجودی",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='black',
            labelanchor='ne'
        )
        self.inventory_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # فریم دو ستونه برای انبار
        inv_columns_frame = tk.Frame(self.inventory_frame, bg='#F5F5F5')
        inv_columns_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # ستون راست انبار
        inv_right_column = tk.Frame(inv_columns_frame, bg='#F5F5F5')
        inv_right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # ستون چپ انبار
        inv_left_column = tk.Frame(inv_columns_frame, bg='#F5F5F5')
        inv_left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # === ستون راست انبار ===
        
        # موجودی فعلی
        current_stock_frame = tk.Frame(inv_right_column, bg='#F5F5F5')
        current_stock_frame.pack(fill=tk.X, pady=2)
        
        current_stock_label = tk.Label(
            current_stock_frame,
            text=": موجودی فعلی *",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5',
            fg='red'
        )
        current_stock_label.pack(side=tk.RIGHT, padx=2)
        
        self.current_stock_var = tk.StringVar()
        current_stock_entry = tk.Entry(
            current_stock_frame,
            textvariable=self.current_stock_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        current_stock_entry.pack(side=tk.RIGHT, padx=2)
        
        # حداکثر موجودی
        max_stock_frame = tk.Frame(inv_right_column, bg='#F5F5F5')
        max_stock_frame.pack(fill=tk.X, pady=2)
        
        max_stock_label = tk.Label(
            max_stock_frame,
            text=": حداکثر موجودی",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        max_stock_label.pack(side=tk.RIGHT, padx=2)
        
        self.max_stock_var = tk.StringVar()
        max_stock_entry = tk.Entry(
            max_stock_frame,
            textvariable=self.max_stock_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        max_stock_entry.pack(side=tk.RIGHT, padx=2)
        
        # حداقل موجودی
        min_stock_frame = tk.Frame(inv_right_column, bg='#F5F5F5')
        min_stock_frame.pack(fill=tk.X, pady=2)
        
        min_stock_label = tk.Label(
            min_stock_frame,
            text=": حداقل موجودی",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        min_stock_label.pack(side=tk.RIGHT, padx=2)
        
        self.min_stock_var = tk.StringVar()
        min_stock_entry = tk.Entry(
            min_stock_frame,
            textvariable=self.min_stock_var,
            font=('Iranian Sans', 10, 'normal'),
            justify='right',
            width=20,
            relief=tk.SOLID,
            bd=1
        )
        min_stock_entry.pack(side=tk.RIGHT, padx=2)
        
        # === ستون چپ انبار ===
        
        # انبارهای نگهداری
        warehouse_frame = tk.Frame(inv_left_column, bg='#F5F5F5')
        warehouse_frame.pack(fill=tk.X, pady=2)
        
        warehouse_label = tk.Label(
            warehouse_frame,
            text=": انبارهای نگهداری",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        warehouse_label.pack(side=tk.RIGHT, padx=2)
        
        # دکمه اضافه کردن
        add_warehouse_btn = tk.Button(
            warehouse_frame,
            text="+",
            font=('Iranian Sans', 10, 'normal'),
            bg='#4CAF50',
            fg='white',
            width=2,
            height=1,
            relief=tk.RAISED,
            bd=1,
            command=self.open_warehouse_form
        )
        add_warehouse_btn.pack(side=tk.RIGHT, padx=1)
        
        # لیست انبارها
        self.warehouse_listbox = tk.Listbox(
            warehouse_frame,
            font=('Iranian Sans', 10, 'normal'),
            width=30,
            height=3,
            selectmode=tk.MULTIPLE,
            relief=tk.SOLID,
            bd=1
        )
        self.warehouse_listbox.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=1)
        
        # فریم پایین
        bottom_frame = tk.Frame(main_frame, bg='#F5F5F5')
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # متن راهنما
        guide_text = tk.Label(
            bottom_frame,
            text="یک شناسه اختصاصی وارد کنید اگر این مقدار را خالی بگذارید سیستم به صورت خودکار یک کد اختصاص خواهد داد",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F5F5F5'
        )
        guide_text.pack(side=tk.TOP, pady=2)
        
        # دکمه‌های ذخیره و لغو در پایین سمت چپ
        buttons_frame = tk.Frame(bottom_frame, bg='#F5F5F5')
        buttons_frame.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)

        # دکمه لغو (قرمز)
        cancel_btn = tk.Button(
            buttons_frame,
            text="لغو",
            font=('Iranian Sans', 10, 'normal'),
            bg='#F44336',
            fg='white',
            command=self.close_window,
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))

        # دکمه ذخیره (سبز)
        save_btn = tk.Button(
            buttons_frame,
            text="ذخیره",
            font=('Iranian Sans', 10, 'normal'),
            bg='#4CAF50',
            fg='white',
            command=self.save_product,
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        save_btn.pack(side=tk.LEFT)
        
        # تنظیم کلیدهای میانبر
        self.setup_shortcuts()
    
    def on_type_change(self):
        """تغییر نوع کالا/خدمات"""
        is_service = self.product_type.get() == "خدمات"
        
        # تغییر برچسب‌ها
        if is_service:
            self.code_label.config(text=": کد خدمات *")
            self.name_label.config(text=": نام خدمات *")
            self.buyable_check.config(text="خدمات قابل خرید")
            self.sellable_check.config(text="خدمات قابل فروش")
            self.producible_check.config(text="خدمات قابل تولید")
        
        # مخفی کردن بخش انبار و موجودی بدون تغییر ترتیب
            for widget in self.inventory_frame.winfo_children():
                widget.configure(state='disabled')
            self.inventory_frame.configure(fg='gray')
        
        # مخفی کردن فیلدهای مربوط به کالا بدون تغییر ترتیب
            for widget in self.row4_left.winfo_children():
                widget.configure(state='disabled')
            for widget in self.row5_left.winfo_children():
                widget.configure(state='disabled')
        
        # تغییر placeholder توضیحات
            current_text = self.desc_text.get("1.0", tk.END).strip()
            if current_text == "شرح معرفی کالا (اختیاری)":
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.insert("1.0", "شرح معرفی خدمات (اختیاری)")
                self.desc_text.config(fg='gray')
                self.desc_text.tag_configure("right", justify='right')
                self.desc_text.tag_add("right", "1.0", "end")
        else:
            self.code_label.config(text=": کد کالا *")
            self.name_label.config(text=": نام کالا *")
            self.buyable_check.config(text="کالای قابل خرید")
            self.sellable_check.config(text="کالای قابل فروش")
            self.producible_check.config(text="کالای قابل تولید")
        
        # نمایش بخش انبار و موجودی
            for widget in self.inventory_frame.winfo_children():
                try:
                    widget.configure(state='normal')
                except:
                    pass
            self.inventory_frame.configure(fg='black')
        
        # نمایش فیلدهای مربوط به کالا
            for widget in self.row4_left.winfo_children():
                try:
                    widget.configure(state='normal')
                except:
                    pass
            for widget in self.row5_left.winfo_children():
                try:
                    widget.configure(state='normal')
                except:
                    pass
        
        # تغییر placeholder توضیحات
            current_text = self.desc_text.get("1.0", tk.END).strip()
            if current_text == "شرح معرفی خدمات (اختیاری)":
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.insert("1.0", "شرح معرفی کالا (اختیاری)")
                self.desc_text.config(fg='gray')
                self.desc_text.tag_configure("right", justify='right')
                self.desc_text.tag_add("right", "1.0", "end")
    
    def select_image(self):
        """انتخاب عکس کالا"""
        file_path = filedialog.askopenfilename(
            title="انتخاب عکس کالا",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # بارگذاری و تغییر اندازه عکس
                image = Image.open(file_path)
                image = image.resize((80, 60), Image.Resampling.LANCZOS)
                self.product_image = ImageTk.PhotoImage(image)
                
                # نمایش عکس در لیبل
                self.image_label.config(image=self.product_image, text="")
                
            except Exception as e:
                self.show_error_message(f"خطا در بارگذاری عکس: {str(e)}")
    
    def load_product_groups(self):
        """بارگذاری گروه‌های کالا"""
        try:
            groups = self.db_manager.get_records('product_groups')
            group_names = [group['name'] for group in groups]
            self.group_combo['values'] = group_names
        except Exception as e:
            print(f"خطا در بارگذاری گروه‌های کالا: {e}")
    
    def load_units(self):
        """بارگذاری واحدهای اندازه‌گیری"""
        try:
            units = self.db_manager.get_records('units')
            unit_names = [unit['name'] for unit in units]
            self.unit_combo['values'] = unit_names
        except Exception as e:
            print(f"خطا در بارگذاری واحدهای اندازه‌گیری: {e}")
    
    def load_warehouses(self):
        """بارگذاری انبارها"""
        try:
            warehouses = self.db_manager.get_records('warehouses')
            self.warehouse_listbox.delete(0, tk.END)
            for warehouse in warehouses:
                self.warehouse_listbox.insert(tk.END, warehouse['name'])
            
            # انتخاب انبار مرکزی به صورت پیش‌فرض
            for i, warehouse in enumerate(warehouses):
                if warehouse['name'] == "انبار مرکزی":
                    self.warehouse_listbox.selection_set(i)
                    break
        except Exception as e:
            print(f"خطا در بارگذاری انبارها: {e}")
    
    def open_product_group_form(self):
        """باز کردن فرم گروه کالا"""
        try:
            from ...ui.forms.product_group_form import ProductGroupForm
            form = ProductGroupForm(self.parent, self.config)
            self.window.wait_window(form.window)
            self.load_product_groups()
        except Exception as e:
            print(f"خطا در باز کردن فرم گروه کالا: {e}")
    
    def open_units_form(self):
        """باز کردن فرم واحدها"""
        try:
            from ...ui.forms.units_form import UnitsForm
            form = UnitsForm(self.parent, self.config)
            self.window.wait_window(form.window)
            self.load_units()
        except Exception as e:
            print(f"خطا در باز کردن فرم واحدها: {e}")
    
    def open_warehouse_form(self):
        """باز کردن فرم انبار"""
        try:
            from ...ui.forms.warehouse_form import WarehouseForm
            form = WarehouseForm(self.parent, self.config)
            self.window.wait_window(form.window)
            self.load_warehouses()
        except Exception as e:
            print(f"خطا در باز کردن فرم انبار: {e}")
    
    def save_product(self):
        """ذخیره کالا"""
        if not self.name_var.get().strip() or self.name_var.get() == "یک نام برای کالا یا خدمات وارد کنید":
            self.show_error_message("نام کالا الزامی است")
            return
        
        if not self.code_var.get().strip():
            self.show_error_message("کد کالا الزامی است")
            return
        
        if not self.sell_price_var.get().strip():
            self.show_error_message("قیمت فروش الزامی است")
            return
        
        try:
            # دریافت گروه کالا
            group_id = None
            if self.group_var.get():
                groups = self.db_manager.get_records('product_groups', 'name = ?', [self.group_var.get()])
                if groups:
                    group_id = groups[0]['id']
            
            # دریافت واحد اندازه‌گیری
            unit_id = None
            if self.unit_var.get():
                units = self.db_manager.get_records('units', 'name = ?', [self.unit_var.get()])
                if units:
                    unit_id = units[0]['id']
            
            # تبدیل قیمت‌ها از فرمت کاما به عدد
            sell_price_clean = self.sell_price_var.get().replace(',', '') if self.sell_price_var.get() else "0"
            buy_price_clean = self.buy_price_var.get().replace(',', '') if self.buy_price_var.get() else "0"

            name_value = self.name_var.get().strip()
            desc_value = self.desc_text.get("1.0", tk.END).strip()
            
            # اگر توضیحات همان متن پیش‌فرض باشد، خالی ذخیره شود
            if desc_value == "شرح معرفی کالا (اختیاری)" or desc_value == "شرح معرفی خدمات (اختیاری)":
                desc_value = ""

            product_data = {
                'name': name_value,
                'code': self.code_var.get().strip(),
                'group_id': group_id,
                'unit_id': unit_id,
                'sell_price': float(sell_price_clean or 0),
                'buy_price': float(buy_price_clean or 0),
                'description': desc_value,
                'is_service': 1 if self.product_type.get() == "خدمات" else 0,
                'stock_quantity': float(self.current_stock_var.get() or 0) if self.product_type.get() == "کالا" else 0,
                'min_stock': float(self.min_stock_var.get() or 0) if self.product_type.get() == "کالا" else 0
            }
            
            if hasattr(self, 'selected_product_id') and self.selected_product_id:
                # ویرایش محصول موجود
                self.db_manager.update_record('products', product_data, f"id = {self.selected_product_id}")
                self.show_success_message(f"{'کالا' if self.product_type.get() == 'کالا' else 'خدمات'} با موفقیت ویرایش شد")
            else:
                # ایجاد محصول جدید
                product_id = self.db_manager.insert_record('products', product_data)
                self.show_success_message(f"{'کالا' if self.product_type.get() == 'کالا' else 'خدمات'} با موفقیت ثبت شد\nشناسه: {product_id}")
            
            self.clear_form()
            
        except Exception as e:
            self.show_error_message(f"خطا در ثبت {'کالا' if self.product_type.get() == 'کالا' else 'خدمات'}: {str(e)}")
    
    def clear_form(self):
        """پاک کردن فرم"""
        self.name_var.set("یک نام برای کالا یا خدمات وارد کنید")

        self.code_var.set("")
        self.group_var.set("")
        self.barcode_var.set("")
        self.product_id_var.set("")
        self.vat_var.set("10")
        self.sell_price_var.set("")
        self.weight_var.set("")
        self.unit_var.set("بسته")
        self.buy_price_var.set("")

        self.desc_text.delete("1.0", tk.END)
        placeholder = "شرح معرفی کالا (اختیاری)" if self.product_type.get() == "کالا" else "شرح معرفی خدمات (اختیاری)"
        self.desc_text.insert("1.0", placeholder)
        self.desc_text.config(fg='gray')
        self.desc_text.tag_configure("right", justify='right')
        self.desc_text.tag_add("right", "1.0", "end")

        self.min_stock_var.set("")
        self.max_stock_var.set("")
        self.current_stock_var.set("")
        self.product_type.set("کالا")
        self.buyable_var.set(True)
        self.sellable_var.set(True)
        self.producible_var.set(True)

        # پاک کردن عکس
        self.product_image = None
        self.image_label.config(image="", text="")

        # پاک کردن انتخاب انبارها
        self.warehouse_listbox.selection_clear(0, tk.END)
        # انتخاب انبار مرکزی
        for i in range(self.warehouse_listbox.size()):
            if self.warehouse_listbox.get(i) == "انبار مرکزی":
                self.warehouse_listbox.selection_set(i)
                break
        
        # بازگشت به حالت کالا
        self.on_type_change()
    
    def setup_shortcuts(self):
        """تنظیم کلیدهای میانبر"""
        self.window.bind('<F6>', lambda e: self.save_product())
        self.window.bind('<Escape>', lambda e: self.close_window())

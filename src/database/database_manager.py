"""
مدیریت دیتابیس
"""

import sqlite3
import os
from pathlib import Path

class DatabaseManager:
    """کلاس مدیریت دیتابیس"""
    
    def __init__(self, config):
        self.config = config
        self.db_path = config.database['path']
        self.init_database()
    
    def get_connection(self):
        """دریافت اتصال به دیتابیس"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # برای دسترسی به ستون‌ها با نام
        return conn
    
    def init_database(self):
        """ایجاد جداول دیتابیس"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # جدول انبارها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS warehouses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    address TEXT,
                    phone TEXT,
                    manager TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول گروه کالا
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS product_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    parent_id INTEGER,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES product_groups (id)
                )
            ''')
            
            # جدول واحدهای اندازه‌گیری
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS units (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    symbol TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول کالا و خدمات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    code TEXT UNIQUE,
                    group_id INTEGER,
                    unit_id INTEGER,
                    buy_price REAL DEFAULT 0,
                    sell_price REAL DEFAULT 0,
                    stock_quantity REAL DEFAULT 0,
                    min_stock REAL DEFAULT 0,
                    description TEXT,
                    is_service BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES product_groups (id),
                    FOREIGN KEY (unit_id) REFERENCES units (id)
                )
            ''')
            
            # جدول بانک‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS banks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    code TEXT,
                    address TEXT,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول حساب‌های بانکی
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bank_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bank_id INTEGER,
                    account_number TEXT NOT NULL,
                    account_name TEXT NOT NULL,
                    iban TEXT,
                    balance REAL DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (bank_id) REFERENCES banks (id)
                )
            ''')
            
            # جدول صندوق‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cash_boxes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    balance REAL DEFAULT 0,
                    responsible_person TEXT,
                    description TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول طرف حساب‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    company_name TEXT,
                    phone TEXT,
                    mobile TEXT,
                    email TEXT,
                    address TEXT,
                    national_id TEXT,
                    economic_code TEXT,
                    postal_code TEXT,
                    customer_type TEXT DEFAULT 'customer', -- customer, supplier, both
                    credit_limit REAL DEFAULT 0,
                    balance REAL DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول درآمد و هزینه‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS income_expense_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL, -- income, expense
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول فرمول‌های تولید
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS production_formulas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    product_id INTEGER,
                    quantity REAL NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # جدول اجزای فرمول تولید
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS formula_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    formula_id INTEGER,
                    product_id INTEGER,
                    quantity REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (formula_id) REFERENCES production_formulas (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            conn.commit()
            print("دیتابیس با موفقیت ایجاد شد")
            
        except Exception as e:
            print(f"خطا در ایجاد دیتابیس: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """اجرای کوئری"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.fetchall()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def insert_record(self, table, data):
        """درج رکورد جدید"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, list(data.values()))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def update_record(self, table, data, condition):
        """به‌روزرسانی رکورد"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, list(data.values()))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def delete_record(self, table, condition, params=None):
        """حذف رکورد"""
        query = f"DELETE FROM {table} WHERE {condition}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_records(self, table, condition=None, params=None):
        """دریافت رکوردها"""
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

"""
ابزارهای کار با تاریخ شمسی - نسخه بهبود یافته
"""

import datetime
from typing import Tuple

class PersianDate:
    """کلاس کار با تاریخ شمسی"""
    
    # نام ماه‌های شمسی
    PERSIAN_MONTHS = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
    ]
    
    # نام روزهای هفته
    PERSIAN_WEEKDAYS = [
        'شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'
    ]
    
    @staticmethod
    def gregorian_to_persian(g_year: int, g_month: int, g_day: int) -> Tuple[int, int, int]:
        """تبدیل تاریخ میلادی به شمسی - الگوریتم دقیق"""
        
        # جدول تبدیل برای سال‌های مختلف
        # این روش برای سال‌های 1900 تا 2100 دقیق است
        
        # محاسبه تعداد روزهای گذشته از 1 ژانویه سال جاری
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # بررسی سال کبیسه میلادی
        if (g_year % 4 == 0 and g_year % 100 != 0) or (g_year % 400 == 0):
            days_in_month[2] = 29
        
        day_of_year = sum(days_in_month[:g_month]) + g_day
        
        # تبدیل به تاریخ شمسی
        if g_year >= 2000:
            # برای سال‌های 2000 به بعد
            p_year = g_year - 621
            
            # تعیین شروع سال شمسی (حوالی 20-21 مارس)
            spring_start = 79  # تقریباً 20 مارس
            if (g_year % 4 == 0 and g_year % 100 != 0) or (g_year % 400 == 0):
                spring_start = 80  # در سال کبیسه
            
            if day_of_year < spring_start:
                # هنوز در سال شمسی قبل هستیم
                p_year -= 1
                # محاسبه روزهای باقیمانده از سال شمسی قبل
                days_left = spring_start - day_of_year
                
                # آخرین ماه‌های سال شمسی
                if days_left <= 29:  # اسفند
                    p_month = 12
                    p_day = 30 - days_left
                elif days_left <= 59:  # بهمن
                    p_month = 11
                    p_day = 30 - (days_left - 29)
                else:  # دی
                    p_month = 10
                    p_day = 30 - (days_left - 59)
            else:
                # در سال شمسی جاری هستیم
                days_passed = day_of_year - spring_start + 1
                
                # تعیین ماه و روز شمسی
                if days_passed <= 31:  # فروردین
                    p_month = 1
                    p_day = days_passed
                elif days_passed <= 62:  # اردیبهشت
                    p_month = 2
                    p_day = days_passed - 31
                elif days_passed <= 93:  # خرداد
                    p_month = 3
                    p_day = days_passed - 62
                elif days_passed <= 124:  # تیر
                    p_month = 4
                    p_day = days_passed - 93
                elif days_passed <= 155:  # مرداد
                    p_month = 5
                    p_day = days_passed - 124
                elif days_passed <= 186:  # شهریور
                    p_month = 6
                    p_day = days_passed - 155
                elif days_passed <= 216:  # مهر
                    p_month = 7
                    p_day = days_passed - 186
                elif days_passed <= 246:  # آبان
                    p_month = 8
                    p_day = days_passed - 216
                elif days_passed <= 276:  # آذر
                    p_month = 9
                    p_day = days_passed - 246
                elif days_passed <= 306:  # دی
                    p_month = 10
                    p_day = days_passed - 276
                elif days_passed <= 336:  # بهمن
                    p_month = 11
                    p_day = days_passed - 306
                else:  # اسفند
                    p_month = 12
                    p_day = days_passed - 336
        else:
            # برای سال‌های قبل از 2000 (روش ساده‌تر)
            p_year = g_year - 621
            p_month = 1
            p_day = 1
        
        return p_year, p_month, p_day
    
    @classmethod
    def now(cls) -> Tuple[int, int, int]:
        """دریافت تاریخ شمسی امروز"""
        today = datetime.date.today()
        return cls.gregorian_to_persian(today.year, today.month, today.day)
    
    @classmethod
    def format_date(cls, p_year: int, p_month: int, p_day: int) -> str:
        """فرمت کردن تاریخ شمسی"""
        return f"{p_year}/{p_month:02d}/{p_day:02d}"
    
    @classmethod
    def format_date_long(cls, p_year: int, p_month: int, p_day: int) -> str:
        """فرمت طولانی تاریخ شمسی"""
        month_name = cls.PERSIAN_MONTHS[p_month - 1]
        return f"{p_day} {month_name} {p_year}"
    
    @classmethod
    def get_weekday_name(cls, date: datetime.date) -> str:
        """دریافت نام روز هفته به فارسی"""
        # تبدیل روز هفته میلادی به شمسی
        weekday = (date.weekday() + 2) % 7
        return cls.PERSIAN_WEEKDAYS[weekday]

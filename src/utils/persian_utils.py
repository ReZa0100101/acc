"""
ابزارهای کمکی برای زبان فارسی
"""

def persian_to_english_digits(text):
    """تبدیل اعداد فارسی به انگلیسی"""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    for persian, english in zip(persian_digits, english_digits):
        text = text.replace(persian, english)
    
    return text

def english_to_persian_digits(text):
    """تبدیل اعداد انگلیسی به فارسی"""
    english_digits = '0123456789'
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    
    text = str(text)
    for english, persian in zip(english_digits, persian_digits):
        text = text.replace(english, persian)
    
    return text

def format_currency(amount):
    """فرمت کردن مبلغ با جداکننده سه رقمی"""
    if amount is None:
        return "۰"
    
    # تبدیل به عدد
    if isinstance(amount, str):
        amount = float(persian_to_english_digits(amount.replace(',', '')))
    
    # فرمت کردن با کاما
    formatted = f"{amount:,.0f}"
    
    # تبدیل به فارسی
    return english_to_persian_digits(formatted)

def format_number(number):
    """فرمت کردن عدد به فارسی"""
    if number is None:
        return "۰"
    
    return english_to_persian_digits(str(number))

def validate_persian_text(text):
    """اعتبارسنجی متن فارسی"""
    if not text or text.strip() == "":
        return False
    return True

def validate_number(text):
    """اعتبارسنجی عدد"""
    try:
        # تبدیل اعداد فارسی به انگلیسی
        english_text = persian_to_english_digits(text.replace(',', ''))
        float(english_text)
        return True
    except ValueError:
        return False

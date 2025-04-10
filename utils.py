import re
from datetime import datetime

def is_valid_url(url):
    """Проверяет, является ли строка корректным URL."""
    if url is None:
        return True
    
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// или https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # домен
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...или IP
        r'(?::\d+)?'  # опциональный порт
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))

def format_price(price):
    """Форматирует цену с разделителями тысяч."""
    return f"{price:,.2f}".replace(',', ' ').replace('.', ',')

def get_current_date_formatted():
    """Возвращает текущую дату в формате ДД.ММ.ГГГГ."""
    return datetime.now().strftime("%d.%m.%Y")

def truncate_text(text, max_length=100):
    """Обрезает текст до указанной длины, добавляя многоточие."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

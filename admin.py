import telebot
from telebot import types
import config
from database import Database

def is_admin(user_id):
    """Проверяет, является ли пользователь администратором."""
    return user_id in config.ADMIN_IDS

def get_admin_stats():
    """Получает статистику для админ-панели."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reviews")
    reviews_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(rating) FROM reviews")
    avg_rating = cursor.fetchone()[0]
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    return {
        'users_count': users_count,
        'products_count': products_count,
        'reviews_count': reviews_count,
        'avg_rating': avg_rating
    }

def get_user_list(limit=100, offset=0):
    """Получает список пользователей."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, username, first_name, last_name, registration_date FROM users ORDER BY registration_date DESC LIMIT ? OFFSET ?",
        (limit, offset)
    )
    return cursor.fetchall()

def get_product_list(category=None, limit=100, offset=0):
    """Получает список товаров."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if category:
        cursor.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY id DESC LIMIT ? OFFSET ?",
            (category, limit, offset)
        )
    else:
        cursor.execute(
            "SELECT * FROM products ORDER BY id DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
    
    return cursor.fetchall()

def update_product(product_id, name=None, category=None, description=None, price=None, image_url=None, available=None):
    """Обновляет информацию о товаре."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    update_fields = []
    params = []
    
    if name is not None:
        update_fields.append("name = ?")
        params.append(name)
    
    if category is not None:
        update_fields.append("category = ?")
        params.append(category)
    
    if description is not None:
        update_fields.append("description = ?")
        params.append(description)
    
    if price is not None:
        update_fields.append("price = ?")
        params.append(price)
    
    if image_url is not None:
        update_fields.append("image_url = ?")
        params.append(image_url)
    
    if available is not None:
        update_fields.append("available = ?")
        params.append(1 if available else 0)
    
    if not update_fields:
        return False
    
    query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
    params.append(product_id)
    
    cursor.execute(query, params)
    conn.commit()
    
    return cursor.rowcount > 0

def delete_product(product_id):
    """Удаляет товар из базы данных."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    return cursor.rowcount > 0

def send_broadcast(bot, text, parse_mode=None):
    """Отправляет сообщение всем пользователям."""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    success_count = 0
    fail_count = 0
    
    for user in users:
        try:
            bot.send_message(user[0], text, parse_mode=parse_mode)
            success_count += 1
        except Exception:
            fail_count += 1
    
    return {
        'total': len(users),
        'success': success_count,
        'fail': fail_count
    }

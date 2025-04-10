import sqlite3
import config
import threading

class Database:
    _instance = None
    _local = threading.local()
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.db_name = config.DB_NAME
        self._create_tables_if_needed()

    def _get_connection(self):
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_name)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection

    def _get_cursor(self):
        return self._get_connection().cursor()

    def _create_tables_if_needed(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Таблица товаров
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            description TEXT,
            price REAL,
            image_url TEXT,
            available INTEGER DEFAULT 1
        )
        ''')
        
        # Таблица отзывов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            rating INTEGER,
            text TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username, first_name, last_name):
        cursor = self._get_cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
            (user_id, username, first_name, last_name)
        )
        self._get_connection().commit()
    
    def get_user(self, user_id):
        cursor = self._get_cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
    
    def add_product(self, name, category, description, price, image_url):
        cursor = self._get_cursor()
        cursor.execute(
            'INSERT INTO products (name, category, description, price, image_url) VALUES (?, ?, ?, ?, ?)',
            (name, category, description, price, image_url)
        )
        self._get_connection().commit()
        return cursor.lastrowid
    
    def get_products_by_category(self, category):
        cursor = self._get_cursor()
        cursor.execute('SELECT * FROM products WHERE category = ? AND available = 1', (category,))
        return cursor.fetchall()
    
    def get_product(self, product_id):
        cursor = self._get_cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return cursor.fetchone()
    
    def add_review(self, user_id, rating, text):
        cursor = self._get_cursor()
        cursor.execute(
            'INSERT INTO reviews (user_id, rating, text) VALUES (?, ?, ?)',
            (user_id, rating, text)
        )
        self._get_connection().commit()
        return cursor.lastrowid
    
    def get_reviews(self, limit=10):
        cursor = self._get_cursor()
        cursor.execute('''
        SELECT r.id, u.first_name, u.last_name, r.rating, r.text, r.date 
        FROM reviews r 
        JOIN users u ON r.user_id = u.user_id 
        ORDER BY r.date DESC LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
    
    def get_connection(self):
        return self._get_connection()
    
    def close(self):
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

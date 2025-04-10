import telebot
from telebot import types
import config

def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton('🛍 Каталог'),
        types.KeyboardButton('❓ FAQ'),
        types.KeyboardButton('📝 Оставить отзыв'),
        types.KeyboardButton('📱 Наши контакты'),
        types.KeyboardButton('🔍 О нас')
    ]
    keyboard.add(*buttons)
    return keyboard

def categories_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # Увеличиваем row_width до 2
    
    # Разбиваем категории на группы по 2 для более компактного отображения
    categories = config.SHOE_CATEGORIES
    
    # Добавляем кнопки по 2 в ряд
    for i in range(0, len(categories), 2):
        row_buttons = []
        row_buttons.append(types.InlineKeyboardButton(
            categories[i], 
            callback_data=f'category_{categories[i]}'
        ))
        
        # Добавляем вторую кнопку в ряд, если она есть
        if i + 1 < len(categories):
            row_buttons.append(types.InlineKeyboardButton(
                categories[i + 1], 
                callback_data=f'category_{categories[i + 1]}'
            ))
        
        keyboard.add(*row_buttons)
    
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_main'))
    return keyboard

def product_keyboard(product_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton('🛒 Заказать', url="https://vk.com/al_im.php?sel=-62624676&entrypoint=community_page"),  # Исправлено с url на callback_data
        types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_category')
    )
    return keyboard
def faq_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i, question in enumerate(config.FAQ.keys()):
        # Используем индекс вместо полного текста вопроса для callback_data
        keyboard.add(types.InlineKeyboardButton(question, callback_data=f'faq_{i}'))
    keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_main'))
    return keyboard

def contacts_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton('🌐 Наш сайт', url=config.WEBSITE_URL),
        types.InlineKeyboardButton('📱 Группа ВКонтакте', url=config.VK_URL),
        types.InlineKeyboardButton('📢 Telegram канал', url=config.TELEGRAM_GROUP_URL),
        types.InlineKeyboardButton('📍 Адреса магазинов', callback_data='show_addresses'),
        types.InlineKeyboardButton('⬅️ Назад', callback_data='back_to_main')
    )
    return keyboard

def review_rating_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    buttons = [types.InlineKeyboardButton(str(i), callback_data=f'rating_{i}') for i in range(1, 6)]
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton('⬅️ Отмена', callback_data='back_to_main'))
    return keyboard

def positive_review_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton('✅Отзыв на Яндексе, для п. Победы', url=config.YANDEX_REVIEW_URL),
        types.InlineKeyboardButton('✅Отзыв на Яндексе, для Московская ул', url="https://yandex.ru/maps/org/shoes_club/1169691228/?ll=45.014207%2C53.186704&utm_content=add_review&utm_medium=reviews&utm_source=maps-reviews-widget&z=16.01"),
        types.InlineKeyboardButton('✅Отзыв на Яндексе, для ул. Бакунина', url="https://yandex.ru/maps/org/shoes_club/123077778706/?ll=45.014813%2C53.199101&utm_content=add_review&utm_medium=reviews&utm_source=maps-reviews-widget&z=16.01"),
        types.InlineKeyboardButton('⬅️ В главное меню', callback_data='back_to_main')
    )
    return keyboard

def negative_review_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton('👨‍💼 Связаться с руководителем', url=f'https://t.me/MPV_SC'),  # Замените на реальный username
        types.InlineKeyboardButton('⬅️ В главное меню', callback_data='back_to_main')
    )
    return keyboard

def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton('📊 Статистика'),
        types.KeyboardButton('➕ Добавить товар'),
        types.KeyboardButton('📝 Просмотр отзывов'),
        types.KeyboardButton('📨 Рассылка'),
        types.KeyboardButton('⬅️ Выход из админки')
    ]
    keyboard.add(*buttons)
    return keyboard

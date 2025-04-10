import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import config
from database import Database
from keyboards import *
import utils

user_states = {}
user_temp_data = {}

class UserState:
    MAIN = 'main'
    WAITING_FOR_REVIEW_TEXT = 'waiting_for_review_text'
    ADMIN_ADDING_PRODUCT_NAME = 'admin_adding_product_name'
    ADMIN_ADDING_PRODUCT_CATEGORY = 'admin_adding_product_category'
    ADMIN_ADDING_PRODUCT_DESCRIPTION = 'admin_adding_product_description'
    ADMIN_ADDING_PRODUCT_PRICE = 'admin_adding_product_price'
    ADMIN_ADDING_PRODUCT_IMAGE = 'admin_adding_product_image'
    ADMIN_SENDING_BROADCAST = 'admin_sending_broadcast'

def handle_start(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    db = Database()
    db.add_user(user_id, username, first_name, last_name)
    user_states[user_id] = UserState.MAIN
    
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {first_name}! 👋\n\n"
        f"Добро пожаловать в бот магазина обуви. Здесь вы можете:\n"
        f"• Просмотреть наш каталог 🛍\n"
        f"• Получить ответы на частые вопросы ❓\n"
        f"• Оставить отзыв о нашем магазине 📝\n"
        f"• Узнать наши контакты 📱\n\n"
        f"Выберите интересующий вас раздел в меню ниже:",
        reply_markup=main_menu_keyboard()
    )

def handle_text(bot, message):
    user_id = message.from_user.id
    text = message.text
    
    if user_id not in user_states:
        user_states[user_id] = UserState.MAIN
    
    state = user_states[user_id]
    
    # Обработка состояний
    if state == UserState.WAITING_FOR_REVIEW_TEXT:
        handle_review_text(bot, message)
        return
    elif state == UserState.ADMIN_ADDING_PRODUCT_NAME:
        handle_admin_product_name(bot, message)
        return
    elif state == UserState.ADMIN_ADDING_PRODUCT_CATEGORY:
        handle_admin_product_category(bot, message)
        return
    elif state == UserState.ADMIN_ADDING_PRODUCT_DESCRIPTION:
        handle_admin_product_description(bot, message)
        return
    elif state == UserState.ADMIN_ADDING_PRODUCT_PRICE:
        handle_admin_product_price(bot, message)
        return
    elif state == UserState.ADMIN_ADDING_PRODUCT_IMAGE:
        handle_admin_product_image(bot, message)
        return
    elif state == UserState.ADMIN_SENDING_BROADCAST:
        handle_admin_broadcast(bot, message)
        return
    
    # Обработка команд из главного меню
    if text == '🛍 Каталог':
        bot.send_message(
            message.chat.id,
            "Выберите категорию обуви:",
            reply_markup=categories_keyboard()
        )
    elif text == '❓ FAQ':
        bot.send_message(
            message.chat.id,
            "Выберите интересующий вас вопрос:",
            reply_markup=faq_keyboard()
        )
    elif text == '📝 Оставить отзыв':
        bot.send_message(
            message.chat.id,
            "Оцените наш магазин от 1 до 5, где 5 - отлично(За вашу оценку, получите подарок на кассе):",
            reply_markup=review_rating_keyboard()
        )
    elif text == '📱 Наши контакты':
        bot.send_message(
            message.chat.id,
            "Наши контакты и социальные сети:",
            reply_markup=contacts_keyboard()
        )
    elif text == '🔍 О нас':
        bot.send_message(
            message.chat.id,
            "Мы - современный магазин обуви с широким ассортиментом для всей семьи. "
            "Наша миссия - предоставить качественную и стильную обувь по доступным ценам. "
            "Мы работаем напрямую с производителями, что позволяет нам предлагать лучшие цены."
        )
    # Обработка команд админа
    elif text == '📊 Статистика' and user_id in config.ADMIN_IDS:
        handle_admin_stats(bot, message)
    elif text == '➕ Добавить товар' and user_id in config.ADMIN_IDS:
        start_adding_product(bot, message)
    elif text == '📝 Просмотр отзывов' and user_id in config.ADMIN_IDS:
        handle_admin_reviews(bot, message)
    elif text == '📨 Рассылка' and user_id in config.ADMIN_IDS:
        start_broadcast(bot, message)
    elif text == '⬅️ Выход из админки' and user_id in config.ADMIN_IDS:
        user_states[user_id] = UserState.MAIN
        bot.send_message(
            message.chat.id,
            "Вы вышли из режима администратора.",
            reply_markup=main_menu_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Извините, я не понимаю эту команду. Пожалуйста, используйте меню для навигации.",
            reply_markup=main_menu_keyboard()
        )


def handle_callback(bot, call):
    user_id = call.from_user.id
    db = Database()
    
    # Обработка кнопки "Назад к категориям"
    if call.data == 'back_to_category':
        try:
            # Try to edit the message text
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Выберите категорию обуви:",
                reply_markup=categories_keyboard()
            )
        except telebot.apihelper.ApiTelegramException as e:
            # If editing fails (e.g., message has no text), delete the message and send a new one
            if "there is no text in the message to edit" in str(e):
                bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
                bot.send_message(
                    call.message.chat.id,
                    "Выберите категорию обуви:",
                    reply_markup=categories_keyboard()
                )
            else:
                # Re-raise other exceptions
                raise
        
        bot.answer_callback_query(call.id)
        return
    
    # Обработка кнопки "Назад" в главное меню
    elif call.data == 'back_to_main':
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            call.message.chat.id,
            "Выберите раздел:",
            reply_markup=main_menu_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # Обработка FAQ вопросов
    elif call.data.startswith('faq_'):
        faq_index = int(call.data.split('_')[1])
        questions = list(config.FAQ.keys())
        answers = list(config.FAQ.values())
        
        if faq_index < len(questions):
            question = questions[faq_index]
            answer = answers[faq_index]
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"*{question}*\n\n{answer}",
                parse_mode='Markdown',
                reply_markup=faq_keyboard()
            )
        bot.answer_callback_query(call.id)
        return
    
    # Обработка рейтинга отзыва
    elif call.data.startswith('rating_'):
        rating = int(call.data.split('_')[1])
        user_temp_data[user_id] = {'rating': rating}
        user_states[user_id] = UserState.WAITING_FOR_REVIEW_TEXT
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Вы поставили оценку: {'⭐' * rating}\n\nПожалуйста, напишите текст вашего отзыва:"
        )
        bot.answer_callback_query(call.id)
        return
    
    # В функции handle_callback добавьте следующий блок:
    elif call.data == 'show_addresses':
        addresses_text = (
            "📍 <b>Наши магазины:</b>\n\n"
            "🏢 <b>Shoes Club</b>\n"
            "Адрес: просп. Победы, 31, Пенза\n"
            "Время работы: 09:00-19:00\n"
            "Телефон: +703-723\n\n"
            
            "🏢 <b>Shoes Club</b>\n"
            "Адрес: Московская ул., 12, Пенза\n"
            "Время работы: 09:00-19:00\n"
            "Телефон: +703-723\n\n"
            
            "🏢 <b>Shoes Club</b>\n"
            "Адрес: ул. Бакунина, 27, Пенза\n"
            "Время работы: 09:00-19:00\n"
            "Телефон: +703-723"
        )
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton('🗺 Открыть карту', url="https://yandex.ru/maps/49/penza/chain/shoes_club/11446545906/filter/chain_id/11446545906/?ll=45.030536%2C53.200042&sctx=ZAAAAAgBEAAaKAoSCU1KQbeXfkZAEe%2Bs3Xahm0pAEhIJ7ginBS%2F6oj8RLJs5JLVQkj8iBgABAgMEBSgAOABA1Z8NSAFqAnJ1ggEUY2hhaW5faWQ6MTE0NDY1NDU5MDadAc3MzD2gAQCoAQC9AVF97dTCARGSuofAygO%2F%2F9WK%2BgbcpOCtBIICFGNoYWluX2lkOjExNDQ2NTQ1OTA2igIAkgIAmgIMZGVza3RvcC1tYXBzqgJkMTE0NDY1NDU5MDYsMjA3NDU2NTM5NTIsNDE5NTA3OTkwNiw2MDAzNzA0LDkwNDE0ODcxMjIsODA1NTUwOTM3LDE4ODk1MzkyNzY5NCw2MDAyMTAzLDYwMDM3MTksNjAwMzYzM7ACAQ%3D%3D&sll=45.030536%2C53.200042&sspn=0.246506%2C0.084524&utm_content=add_review&utm_medium=reviews&utm_source=maps-reviews-widget&z=13")
        )
        keyboard.add(types.InlineKeyboardButton('⬅️ Назад', callback_data='show_contacts'))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=addresses_text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        bot.answer_callback_query(call.id)
        return
    
    # Также добавьте обработчик для возврата к контактам:
    elif call.data == 'show_contacts':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Наши контакты и социальные сети:",
            reply_markup=contacts_keyboard()
        )
        bot.answer_callback_query(call.id)
        return
    
    # Обработка выбора категории
    elif call.data.startswith('category_'):
        category = call.data.replace('category_', '')
        products = db.get_products_by_category(category)
        
        if not products:
            bot.answer_callback_query(call.id, "В этой категории пока нет товаров")
            return
        
        user_temp_data[user_id] = {'current_category': category}
        
        # Сначала отправляем сообщение о категории
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Категория: {category}\nНайдено товаров: {len(products)}",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton('⬅️ Назад к категориям', callback_data='back_to_category')
            )
        )
        
        # Затем отправляем каждый товар отдельным сообщением
        for product in products:
            product_id, name, _, description, price, image_url, _ = product
            caption = f"<b>{name}</b>\n\n{description}\n\nЦена: {price} руб."
            
            if image_url:
                bot.send_photo(
                    call.message.chat.id,
                    image_url,
                    caption=caption,
                    parse_mode='HTML',
                    reply_markup=product_keyboard(product_id)
                )
            else:
                bot.send_message(
                    call.message.chat.id,
                    caption,
                    parse_mode='HTML',
                    reply_markup=product_keyboard(product_id)
                )
    
    # Убираем "часики" на кнопке для всех остальных callback
    bot.answer_callback_query(call.id)



def handle_review_text(bot, message):
    user_id = message.from_user.id
    text = message.text
    db = Database()
    
    if user_id not in user_temp_data or 'rating' not in user_temp_data[user_id]:
        bot.send_message(
            message.chat.id,
            "Произошла ошибка. Пожалуйста, начните процесс оценки заново.",
            reply_markup=main_menu_keyboard()
        )
        user_states[user_id] = UserState.MAIN
        return
    
    rating = user_temp_data[user_id]['rating']
    db.add_review(user_id, rating, text)
    
    user_states[user_id] = UserState.MAIN
    
    if rating >= 4:  # Положительный отзыв
        bot.send_message(
            message.chat.id,
            "Спасибо за ваш положительный отзыв! Мы очень рады, что вам понравился наш магазин. "
            "Будем благодарны, если вы также оставите отзыв на Яндексе:",
            reply_markup=positive_review_keyboard()
        )
    else:  # Отрицательный отзыв
        bot.send_message(
            message.chat.id,
            "Спасибо за ваш отзыв. Нам очень жаль, что у вас остались негативные впечатления. "
            "Мы хотели бы исправить ситуацию. Пожалуйста, свяжитесь с руководителем магазина:",
            reply_markup=negative_review_keyboard()
        )

# Функции для админки
def handle_admin_command(bot, message):
    user_id = message.from_user.id
    
    if user_id not in config.ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            "У вас нет доступа к этой команде."
        )
        return
    
    bot.send_message(
        message.chat.id,
        "Панель администратора:",
        reply_markup=admin_keyboard()
    )

def handle_admin_stats(bot, message):
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
    
    stats_text = (
        "📊 <b>Статистика магазина</b>\n\n"
        f"👥 Пользователей бота: {users_count}\n"
        f"🛍 Товаров в каталоге: {products_count}\n"
        f"📝 Отзывов получено: {reviews_count}\n"
        f"⭐ Средняя оценка: {avg_rating}/5"
    )
    
    bot.send_message(
        message.chat.id,
        stats_text,
        parse_mode='HTML'
    )

def start_adding_product(bot, message):
    user_id = message.from_user.id
    user_states[user_id] = UserState.ADMIN_ADDING_PRODUCT_NAME
    user_temp_data[user_id] = {}
    
    bot.send_message(
        message.chat.id,
        "Добавление нового товара.\n\nВведите название товара:"
    )

def handle_admin_product_name(bot, message):
    user_id = message.from_user.id
    user_temp_data[user_id]['name'] = message.text
    user_states[user_id] = UserState.ADMIN_ADDING_PRODUCT_CATEGORY
    
    # Создаем клавиатуру с категориями
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for category in config.SHOE_CATEGORIES:
        keyboard.add(types.KeyboardButton(category))
    
    bot.send_message(
        message.chat.id,
        "Выберите категорию товара:",
        reply_markup=keyboard
    )

def handle_admin_product_category(bot, message):
    user_id = message.from_user.id
    category = message.text
    
    if category not in config.SHOE_CATEGORIES:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите категорию из списка."
        )
        return
    
    user_temp_data[user_id]['category'] = category
    user_states[user_id] = UserState.ADMIN_ADDING_PRODUCT_DESCRIPTION
    
    bot.send_message(
        message.chat.id,
        "Введите описание товара:",
        reply_markup=types.ReplyKeyboardRemove()
    )

def handle_admin_product_description(bot, message):
    user_id = message.from_user.id
    user_temp_data[user_id]['description'] = message.text
    user_states[user_id] = UserState.ADMIN_ADDING_PRODUCT_PRICE
    
    bot.send_message(
        message.chat.id,
        "Введите цену товара (только число):"
    )

def handle_admin_product_price(bot, message):
    user_id = message.from_user.id
    price_text = message.text
    
    try:
        price = float(price_text)
        if price <= 0:
            raise ValueError("Цена должна быть положительным числом")
        
        user_temp_data[user_id]['price'] = price
        user_states[user_id] = UserState.ADMIN_ADDING_PRODUCT_IMAGE
        
        bot.send_message(
            message.chat.id,
            "Отправьте URL изображения товара (или напишите 'нет', если изображения нет):"
        )
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, введите корректную цену (только число)."
        )

def handle_admin_product_image(bot, message):
    user_id = message.from_user.id
    image_url = message.text
    db = Database()
    
    if image_url.lower() == 'нет':
        image_url = None
    
    user_temp_data[user_id]['image_url'] = image_url
    
    # Сохраняем товар в базу данных
    product_data = user_temp_data[user_id]
    db.add_product(
        product_data['name'],
        product_data['category'],
        product_data['description'],
        product_data['price'],
        product_data['image_url']
    )
    
    user_states[user_id] = UserState.MAIN
    
    bot.send_message(
        message.chat.id,
        "Товар успешно добавлен в каталог!",
        reply_markup=admin_keyboard()
    )

def handle_admin_reviews(bot, message):
    db = Database()
    reviews = db.get_reviews(10)  # Получаем последние 10 отзывов
    
    if not reviews:
        bot.send_message(
            message.chat.id,
            "Отзывов пока нет."
        )
        return
    
    for review in reviews:
        review_id, first_name, last_name, rating, text, date = review
        stars = "⭐" * rating
        
        review_text = (
            f"<b>Отзыв #{review_id}</b>\n"
            f"От: {first_name} {last_name}\n"
            f"Оценка: {stars} ({rating}/5)\n"
            f"Дата: {date}\n\n"
            f"{text}"
        )
        
        bot.send_message(
            message.chat.id,
            review_text,
            parse_mode='HTML'
        )

def start_broadcast(bot, message):
    user_id = message.from_user.id
    user_states[user_id] = UserState.ADMIN_SENDING_BROADCAST
    
    bot.send_message(
        message.chat.id,
        "Введите текст сообщения для рассылки всем пользователям:"
    )

def handle_admin_broadcast(bot, message):
    user_id = message.from_user.id
    broadcast_text = message.text
    db = Database()
    
    # Получаем всех пользователей
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    
    sent_count = 0
    for user in users:
        try:
            bot.send_message(
                user[0],
                f"📢 <b>Объявление от магазина обуви</b>\n\n{broadcast_text}",
                parse_mode='HTML'
            )
            sent_count += 1
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user[0]}: {e}")
    
    user_states[user_id] = UserState.MAIN
    
    bot.send_message(
        message.chat.id,
        f"Рассылка выполнена. Сообщение доставлено {sent_count} из {len(users)} пользователей.",
        reply_markup=admin_keyboard()
    )


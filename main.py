import telebot
import config
from handlers import *
from database import Database
import admin

# Инициализация бота
bot = telebot.TeleBot(config.BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    handle_start(bot, message)

# Обработчик команды /admin
@bot.message_handler(commands=['admin'])
def admin_command(message):
    handle_admin_command(bot, message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('faq_'))
def handle_faq_callback(call):
    # Извлекаем индекс вопроса из callback_data
    faq_index = int(call.data.split('_')[1])
    
    # Получаем вопрос и ответ из конфигурации
    questions = list(config.FAQ.keys())
    answers = list(config.FAQ.values())
    
    if faq_index < len(questions):
        question = questions[faq_index]
        answer = answers[faq_index]
        
        # Отправляем ответ пользователю
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"*{question}*\n\n{answer}",
            parse_mode='Markdown',
            reply_markup=faq_keyboard()
        )
    
    # Убираем "часики" на кнопке
    bot.answer_callback_query(call.id)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text_message(message):
    handle_text(bot, message)

# Обработчик callback-запросов (нажатия на inline-кнопки)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    handle_callback(bot, call)

if __name__ == '__main__':
    print("Бот запущен...")
    # Запуск бота в режиме polling
    bot.polling(none_stop=True, interval=0)

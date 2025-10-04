# main.py

import telebot
import os

# Получаем токен бота и ID администратора из переменных окружения
# Это более безопасно, чем хранить их прямо в коде
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

# Проверяем, что переменные заданы
if not BOT_TOKEN or not ADMIN_CHAT_ID:
    print("Ошибка: BOT_TOKEN и ADMIN_CHAT_ID должны быть установлены как переменные окружения.")
    exit()

# Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик для всех входящих текстовых сообщений
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    """
    Пересылает сообщение от любого пользователя администратору.
    """
    try:
        # Формируем сообщение для администратора
        user_info = message.from_user
        username = f"@{user_info.username}" if user_info.username else "N/A"
        forward_message = (
            f"🔔 Новое уведомление!\n\n"
            f"От пользователя: {user_info.first_name} {user_info.last_name or ''}\n"
            f"Username: {username}\n"
            f"User ID: {user_info.id}\n\n"
            f"Сообщение:\n«{message.text}»"
        )
        
        # Отправляем сообщение администратору
        bot.send_message(ADMIN_CHAT_ID, forward_message)
        
        # Опционально: можно отправить пользователю подтверждение, что сообщение получено
        # bot.send_message(message.chat.id, "Ваше сообщение было переслано администратору.")
        
    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")
        # В случае ошибки, можно уведомить администратора или залогировать
        bot.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при пересылке сообщения от пользователя {message.from_user.id}: {e}")

# Запускаем бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)


import telebot
import pymysql
import configsql

# Подключение к базе данных
mydb = pymysql.connect(
    host = configsql.host,
    user = configsql.user,
    password = configsql.password
)
mycursor = mydb.cursor()

# Токен вашего телеграм бота
TOKEN = configsql.TOKEN
# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Идентификаторы пользователей, которым разрешено использовать бота
allowedchatids = configsql.admin

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handlestart(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "I'm sorry, but I can't allow you to enter commands, since you are not listed in my code as the managing person.")
    else:
        bot.send_message(message.chat.id, "Hi! I am a MySQL database management bot developed by Web Arkhem.\Here are my commands:\n/create_db - Create a database\n/delete_db - Delete a database\n/create_table - Create a table\n/delete_table - delete a table\nNo commands can also be viewed in the 'Menu' tab")

# Обработчик команды /create_db
@bot.message_handler(commands=['create_db'])
def handle_create_db(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "I apologize, but I cannot allow you to enter commands, since you are not listed in my code as the managing person.")
    else:
        bot.send_message(message.chat.id, "Enter the name of the database:")
        bot.register_next_step_handler(message, create_db_command)

def create_db_command(message):
    try:
        mycursor.execute(f"CREATE DATABASE {message.text}")
        bot.send_message(message.chat.id, f"The database '{message.text}' has been successfully created.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"An error occurred while creating the database: {e}")

# Обработчик команды /delete_db
@bot.message_handler(commands=['delete_db'])
def handle_delete_db(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "I apologize, but I cannot allow you to enter commands, since you are not listed in my code as the managing person.")
    else:
        bot.send_message(message.chat.id, "Enter the name of the database to delete:")
        bot.register_next_step_handler(message, delete_db_command)

def delete_db_command(message):
    try:
        mycursor.execute(f"DROP DATABASE {message.text}")
        bot.send_message(message.chat.id, f"The database '{message.text}' has been successfully deleted.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"An error occurred while deleting the database: {e}")

# Обработчик команды /create_table
@bot.message_handler(commands=['create_table'])
def handle_create_table(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, "I apologize, but I cannot allow you to enter commands, since you are not listed in my code as the managing person.")
    else:
        bot.send_message(message.chat.id, " Enter the name of the database:")
        bot.register_next_step_handler(message, create_table_database)

def create_table_database(message):
    try:
        mycursor.execute(f"USE {message.text}")
        bot.send_message(message.chat.id, "Enter the name of the table:")
        bot.register_next_step_handler(message, create_table_name, message.text)
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"An error occurred while connecting to the database: {e}")

def create_table_name(message, database_name):
    try:
        table_name = message.text
        mycursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
        bot.send_message(message.chat.id, f"The table '{table_name}' was successfully created in the database '{database_name}'.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при создании таблицы: {e}")

# Обработчик команды /delete_table
@bot.message_handler(commands=['delete_table'])
def handle_delete_table(message):
    if message.chat.id not in allowedchatids:
        bot.send_message(message.chat.id, " I apologize, but I cannot allow you to enter commands, since you are not listed in my code as the managing person.")
    else:
        bot.send_message(message.chat.id, "Enter the name of the database:")
        bot.register_next_step_handler(message, delete_table_database)

def delete_table_database(message):
    try:
        mycursor.execute(f"USE {message.text}")
        bot.send_message(message.chat.id, "Enter the name of the table to delete:")
        bot.register_next_step_handler(message, delete_table_name, message.text)
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"An error occurred while connecting to the database: {e}")

def delete_table_name(message, database_name):
    try:
        table_name = message.text
        mycursor.execute(f"DROP TABLE {table_name}")
        bot.send_message(message.chat.id, f"The table '{table_name}' has been successfully deleted from the database '{database_name}'.")
    except pymysql.Error as e:
        bot.send_message(message.chat.id, f"An error occurred when deleting the table: {e}")

# Запуск бота
bot.polling()

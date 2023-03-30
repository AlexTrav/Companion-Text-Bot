import sqlite3 as sq


# Класс базы данных
class DataBase:

    # Инициализатор conn и cursor
    def __init__(self):
        self.conn = sq.connect('bot/db/database.db')
        self.cursor = self.conn.cursor()

    # Получить данные из таблицы
    def get_data(self, **kwargs):
        if 'where' in kwargs:
            self.cursor.execute(f'SELECT * FROM {kwargs["table"]} WHERE {kwargs["op1"]} = "{kwargs["op2"]}"')
        else:
            self.cursor.execute(f"SELECT * FROM {kwargs['table']}")
        return self.cursor.fetchall()

    # Проверка наличия пользователя в базе данных
    def checking_user(self, **kwargs):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        if not users:
            self.cursor.execute(
                f'INSERT INTO users(id, username, flname) VALUES ({kwargs["user_id"]}, "{kwargs["username"]}", "{kwargs["flname"]}")')
            self.conn.commit()
        else:
            self.cursor.execute(f'SELECT * FROM users WHERE id = {kwargs["user_id"]}')
            user = self.cursor.fetchall()
            if not user:
                self.cursor.execute(
                    f'INSERT INTO users(id, username, flname) VALUES ({kwargs["user_id"]}, "{kwargs["username"]}", "{kwargs["flname"]}")')
                self.conn.commit()

    # Обновить id модели у user-а
    def update_model_user(self, **kwargs):
        self.cursor.execute(f'UPDATE users SET model_id_selected = {kwargs["model_id"]} WHERE id = {kwargs["user_id"]}')
        self.conn.commit()


# Экземпляр класса DataBase
db = DataBase()

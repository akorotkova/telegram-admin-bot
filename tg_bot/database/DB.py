import asyncio
import time

import asyncpg

import tracemalloc
tracemalloc.start()

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]



class Database(metaclass=Singleton):



    # def __init__(self):
    #     print(123)

    async def connect(self, user, password, database, host):
        self.db = await asyncpg.connect(user=user, password=password,
                                           database=database, host=host, port=5432)





    async def close(self):
        await self.db.close()

    async def create_tables(self):
        # Создаем таблицу chats, если ее нет
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id_chat SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        ''')


        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id_user INTEGER PRIMARY KEY
            );
        ''')

        # Создаем таблицу settings_list, если ее нет
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS settings_list (
                id_settings SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                standard BOOLEAN NOT NULL
            );
        ''')

        # Создаем таблицу settings_chats, если ее нет
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS settings_chats (
                id_chat INTEGER NOT NULL REFERENCES chats (id_chat),
                id_settings INTEGER NOT NULL REFERENCES settings_list (id_settings),
                id_admin INTEGER NOT NULL,
                status INTEGER NOT NULL,
                PRIMARY KEY (id_chat, id_settings)
            );
        ''')


        await self.db.execute('''
        CREATE TABLE IF NOT EXISTS rules_chat (
        id_chat BIGINT PRIMARY KEY REFERENCES chats(id_chat),
        message TEXT NOT NULL
            );''')


        await self.db.execute('''
        CREATE TABLE IF NOT EXISTS info_user_in_chat (
            id_user BIGINT NOT NULL REFERENCES users(id_user),
            id_chat BIGINT NOT NULL REFERENCES chats(id_chat),
            message TEXT NOT NULL,
            id_admin BIGINT NOT NULL REFERENCES users(id_user),
            comment TEXT,
            status TEXT,
            time TIMESTAMP NOT NULL,
            PRIMARY KEY (id_user, id_chat, time)
        );''')


        await self.db.execute('''
        CREATE TABLE IF NOT EXISTS status_all_penalty (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );''')


        await self.db.execute('''
        CREATE TABLE IF NOT EXISTS speed_message (
                id SERIAL PRIMARY KEY,
                tag TEXT NOT NULL,
                id_chat INTEGER NOT NULL REFERENCES chats(id_chat),
                message TEXT NOT NULL
            );''')

    async def put_new_chat(self, id_chat: int, name: str):

        await self.db.execute("INSERT INTO chats (id_chat, name) VALUES ($1, $2)", id_chat, name)

    async def put_speed_message(self, tag: str, id_chat: int, message: str):
        await self.db.execute("INSERT INTO speed_message (tag, id_chat, message) VALUES ($1, $2, $3);", tag, id_chat, message)


    async def drop_all_table(self):
        await self.db.execute("""DROP SCHEMA public CASCADE; CREATE SCHEMA public;""")



async def main():
    # Пример использования)

    db = Database() # Инициализация. Делаем для подключения или если нужно обратиться к бд

    await db.connect(user='user', password='LlGMTNj3qux5YYoooNLX', host='localhost', database='mydatabase') # Подключение к базе. Нужно сделать один раз. Дальше можно просто юзать Database().
    # Данные для авторизации естественно берем свои
    # локально базу поднять можно в докере.
    # docker run --rm --name selectel-pgdocker -e POSTGRES_PASSWORD=LlGMTNj3qux5YYoooNLX -e POSTGRES_USER=user -e POSTGRES_DB=mydatabase -d -p 5432:5432  postgres

    await db.create_tables() # Создаем таблицы. Тут есть проверка на то что таблицы уже существуют. Так что можно просто вызвать при запуске бота




    db1 = Database() # собственно проверка)
    print(id(db), id(db1))

    await db1.put_new_chat(1, 'test') # Чат можно добавить только один раз. Дальше будет ошибка. Потом придумаем что сделать и как правильно писать их

    await db1.put_speed_message('джун', 1, '123') # Так добавляем сообщение




    # await db1.drop_all_table() # Удаляет все таблицы и все что в них могло быть. Так что для тестов норм.
    await db1.close()


if __name__ == '__main__':
    asyncio.run(main())

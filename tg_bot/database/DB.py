import asyncio
import time

import asyncpg


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print(123)

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
                tag TEXT NOT NULL,
                id_chat BIGINT NOT NULL REFERENCES chats(id_chat),
                message TEXT NOT NULL,
                PRIMARY KEY (tag, id_chat)
            );''')




    async def drop_all_table(self):
        await self.db.execute("""DROP SCHEMA public CASCADE; CREATE SCHEMA public;""")



async def main():
    db = Database()
    await db.connect(user='user', password='LlGMTNj3qux5YYoooNLX', host='172.17.0.2', database='mydatabase')
    await db.create_tables()


    db1 = Database()




    print(db, db1)

    await asyncio.sleep(2)

    await db1.drop_all_table()

    await db1.close()



asyncio.run(main())

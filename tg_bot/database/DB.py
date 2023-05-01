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
                name TEXT NOT NULL UNIQUE,
                standard TEXT NOT NULL
            );
        ''')

        # Создаем таблицу settings_chats, если ее нет
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS settings_chats (
                id_chat INTEGER NOT NULL REFERENCES chats (id_chat),
                id_settings INTEGER NOT NULL REFERENCES settings_list (id_settings),
                id_admin INTEGER NOT NULL,
                value TEXT NOT NULL,
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
                message TEXT NOT NULL,
                UNIQUE (tag, id_chat, message)
            );''')

    async def put_new_chat(self, id_chat: int, name: str):
        result = await self.db.execute("INSERT INTO chats (id_chat, name) VALUES ($1, $2) ON CONFLICT (id_chat) DO NOTHING;", id_chat, name)
        if result == 'INSERT 0 0':
            return "Уже есть в базе"
        return 0

    async def put_speed_message(self, tag: str, id_chat: int, message: str):
        """Добавляем новое быстрое сообщение
        В случае если сообщение уже есть вернет ТЕКСТОМ "Сообщение уже есть в базе"
        """
        query = """
            INSERT INTO speed_message (tag, id_chat, message) 
            VALUES ($1, $2, $3) 
            ON CONFLICT (tag, id_chat, message) DO NOTHING;
        """
        result = await self.db.execute(query, tag, id_chat, message)
        if result == 'INSERT 0 0':
            return "Сообщение уже есть в базе"
        return 0


    async def get_tags_for_chat(self, id_chat: int):
        """
        Получение всех тегов для чата
        :param id_chat:
        :return: list
        """
        query = 'SELECT DISTINCT tag FROM speed_message WHERE id_chat = $1;'
        results = await self.db.fetch(query, id_chat)
        return [result['tag'] for result in results]



    async def get_messages_by_tag_and_chat(self, id_chat: int, tag: str):
        """
        Получить быстрое сообщение по id чата и его тегу
        :param id_chat: id чата
        :param tag: тег
        :return:
        """
        query = 'SELECT * FROM speed_message WHERE id_chat = $1 AND tag = $2;'
        results = await self.db.fetch(query, id_chat, tag)
        return [dict(result) for result in results]

    async def delete_speed_message(self, id_chat: int, message: str, tag: str):
        query = "DELETE FROM speed_message WHERE id_chat = $1 AND message = $2 AND tag = $3"
        await self.db.execute(query, id_chat, message, tag)


    async def put_new_setting(self, name_setting: str, standard: str):
        """ метод для добавления настройки в таблицу стандартных. То есть его вызывать только при запуске бота.
    # пока нет обработки для добавления настройки налету. Потом что-нибудь придумаю

    """
        result = await self.db.execute("INSERT INTO settings_list (name, standard) VALUES ($1, $2) ON CONFLICT (name) DO NOTHING;;", name_setting, standard)
        if result == 'INSERT 0 0':
            return "Уже есть в базе"
        return 0




    async def drop_all_table(self):
        """Удаляем все таблицы"""
        await self.db.execute("""DROP SCHEMA public CASCADE; CREATE SCHEMA public;""")


    async def put_settings2chat(self, id_chat: int, settings_name : str, id_admin: int = 0):
        """
        Определение настройки для чата. Применять для
        1. нового чата
        2. При создании новой настроки
        :param id_chat:
        :param name: Имя настроки
        :param id_admin: по стандарту лучше ставить 0. Так будет понятно, что это внесино автоматом
        :return:
        """
        result = await self.db.execute('''
            INSERT INTO settings_chats (id_chat, id_settings, id_admin, value)
            SELECT $1, id_settings, $2, standard
            FROM settings_list
            WHERE name = $3 
            ON CONFLICT (id_chat, id_settings) DO NOTHING;;
        ''', id_chat, id_admin, settings_name)
        if result == 'INSERT 0 0':
            return "Уже есть в базе"
        return 0


    async def update_settings_chats_by_name(self, id_chat: int, name: str, id_admin: int, value: str):
        """
        Изменение настроек чата
        :param id_chat: id_chat
        :param name: Имя настройки
        :param id_admin: id_admin
        :param value: новое значение настройки
        :return:
        """
        query = '''
        UPDATE settings_chats
        SET id_admin = $1, value = $2
        FROM settings_list
        WHERE settings_chats.id_settings = settings_list.id_settings
        AND settings_list.name = $3
        AND settings_chats.id_chat = $4;
        '''
        await self.db.execute(query, id_admin, value, name, id_chat)

    async def get_setting_by_name(self, id_chat: int, settings_name: str):
        """
        Получение настройки чата
        :param id_chat:
        :param name:
        :return: value, id_admin если данные есть. Если нет - None
        {'value': 'новое значение', 'id_admin': 3} например
        """
        query = '''
        SELECT value, id_admin
        FROM settings_chats
        JOIN settings_list ON settings_chats.id_settings = settings_list.id_settings
        WHERE settings_list.name = $1
        AND settings_chats.id_chat = $2;
        '''
        result = await self.db.fetchrow(query, settings_name, id_chat)

        if result is None:
            return None

        return dict(result)

    async def get_settings_by_id_chat(self, id_chat: int):
        """
        Запрос все настроек для чата
        """
        query = '''
        SELECT settings_chats.id_chat, settings_chats.id_settings, settings_list.name, settings_chats.value, settings_chats.id_admin
        FROM settings_chats
        JOIN settings_list ON settings_chats.id_settings = settings_list.id_settings
        WHERE settings_chats.id_chat = $1
        '''
        results = await self.db.fetch(query, id_chat)
        settings = [dict(result) for result in results]
        return settings


    async def get_all_settings_standard(self):
        """
        Запрос всех настроек из таблицы стандартных
        :return:
        """
        query = '''
        SELECT id_settings, name, standard
        FROM settings_list
        '''
        results = await self.db.fetch(query)
        settings = [dict(result) for result in results]
        return settings




    async def update_list_chat_settings(self, id_chat:int):
        """
        Обновить список настроек чата. Вызвать это при добавлении чата в бота.
        :param id_chat:
        :return:
        """
        list_settings = await self.get_all_settings_standard()
        for element in list_settings:
            await self.put_settings2chat(id_chat=id_chat, settings_name=element["name"], id_admin=0)









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

    await db1.put_new_chat(id_chat=1, name='test') # Чат можно добавить только один раз. Ошибку убрал. Он просто вернет текстом, что данные уже есть в базе "Уже есть в базе"



    # *********************************** Настройки ****************************


    await db1.put_new_setting(name_setting="settings_test", standard='1') # метод для добавления настройки в таблицу стандартных. То есть его вызывать только при запуске бота.
    # Если настройка уже есть, то вернет "Уже есть в базе"



    await db1.put_settings2chat(id_chat=1, settings_name="settings_test", id_admin=0)
    # #  Определение настройки для чата. Применять для
    # #         1. нового чата
    # #         2. При создании новой настроки
    # Если вызвать еще раз - вернет "Уже есть в базе"
    # Происходит инициалзиция настройки для чата. То есть переносит из таблицы стандартных и делает привязку к чату


    settings_all = await db1.get_all_settings_standard() # запрос всех стандарных настроек из базы. На выходе массив словарей
    # пример [{'id_settings': 1, 'name': 'settings_test', 'standard': '1'}]
    print(f"{settings_all=}")
    # Если мы хотим посмотреть какие вообще настройки могут быть. Это сервисная штука и админы к ней доступа иметь не должны.
    # Но это будет нужно для добавления параметров в таблицы чата



    await db1.update_list_chat_settings(id_chat=1)
    #         Обновить список настроек чата. Вызвать это при добавлении чата в бота.
    # Это комбинация get_all_settings_standard и put_settings2chat



    await db1.update_settings_chats_by_name(id_chat=1, name='settings_test', id_admin=3, value='новое значение') # Обновление настройки для чата


    setting = await db1.get_setting_by_name(id_chat=1, settings_name='settings_test') # получаем параметры настройки и админа который ее редачил
    print(f"{setting=}")




    settings_chat = await db1.get_settings_by_id_chat(id_chat=1) # запрос всех настроек для чата
    print(f"{settings_chat=}")
    # пример вывода [{'id_chat': 1, 'id_settings': 1, 'name': 'settings_test', 'value': 'новое значение', 'id_admin': 3}]




    # ****************************************** Быстрые сообщения ***********************************


    test = await db1.put_speed_message(tag='тест', id_chat=1, message='123') # Так добавляем быстрое сообщение
    print(test)
    # Если оно уже есть в базе, то текстом вернет "Сообщение уже есть в базе". Если все хорошо 0



    # Запрос всех тегов у чата
    list_tegs_in_chat = await db1.get_tags_for_chat(id_chat=1)
    print(f"{list_tegs_in_chat=}")


    # Получить сообщения по тегу
    messages = await db1.get_messages_by_tag_and_chat(id_chat=1, tag='джун')
    print(messages)


    # удалить сообщение
    await db1.delete_speed_message(id_chat=1, message='123', tag="джун")


    # await db1.drop_all_table() # Удаляет все таблицы и все что в них могло быть. Так что для тестов норм.
    await db1.close()


if __name__ == '__main__':
    asyncio.run(main())

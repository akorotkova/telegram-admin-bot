from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class DbConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str
    

@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str) -> Config:
    '''
    Формирует конфигурации бота
    
    Args:
        path (str): путь до файла .env
    Returns:
        config (Config): объект, определяющий настройки бота
    '''
    env: Env = Env()
    env.read_env(path)  # читаем файл .env с переменными окружения
    
    token = env('BOT_TOKEN')
    admin_ids = [int(admin_id) for admin_id in env.list('ADMIN_IDS')]
    tg_bot = TgBot(token, admin_ids)
    
    database = env('DATABASE')
    db_host = env('DB_HOST')
    db_user = env('DB_USER')
    db_password=env('DB_PASSWORD')
    db = DbConfig(database, db_host, db_user, db_password)
    
    config = Config(tg_bot, db)

    return config

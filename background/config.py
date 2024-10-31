import os

from dotenv import load_dotenv

from peewee import SqliteDatabase


env = os.getenv('ENV', 'dev')
load_dotenv(dotenv_path=f".env.{env}")
print(f"[{env}] load ENV...")

broker_redis_url = os.getenv('BROKER_REDIS_URL', 'redis://127.0.0.1:6379/0')

config_file_path = os.path.abspath(__file__)
src_path = os.path.dirname(config_file_path)
data_path = os.path.join(src_path, '../data')

database_url = os.getenv('DATABASE_URL', f"{data_path}/background.db")
db = SqliteDatabase(database_url)
db.connect()

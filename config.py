from pathlib import Path
from env import DB_HOST, USER, PASSWORD, DB_PORT

ROOT_DIR = Path(__file__).parent

db_connection = {'db_host': DB_HOST, 'user': USER, 'password': PASSWORD, 'db_port': DB_PORT}

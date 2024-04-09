from pathlib import Path
from env import DB_HOST, USER, PASSWORD, DB_PORT

ROOT_DIR = Path(__file__).parent

db_connection = {'host': 'localhost', 'user': USER, 'password': PASSWORD, 'port': DB_PORT}

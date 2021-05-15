from uuid import uuid4

DEBUG = False
USER = 'flask_rest'
SENHA = 'Rp%X!hPq'
HOST = 'localhost'
PORT = 3306
SCHEMA = 'flask_rest_api'
SQLALCHEMY_DATABASE_URI = f"postgres://{USER}:{SENHA}@{HOST}/{SCHEMA}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = str(uuid4())
PROPAGATE_EXCEPTIONS = True

import os

DEBUG = os.environ.get('APP_DEBUG', True)
ADMIN = frozenset([
    "zengkyo@gmail.com"
])
SECRET_KEY = '123'
PORT = os.environ.get("APP_PORT", 5000)

# Здесь создаём объект Flask и подключаем конфигурацию

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config # Импортируем конфигурацию

# Инициализация приложения

app = Flask(__name__)
app.config.from_object(Config) # Подключаем конфигурацию из Config.py

db = SQLAlchemy(app)

from app import routes, models

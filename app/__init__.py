# Здесь создаём объект Flask и подключаем конфигурацию

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate  # Импортируем Flask-Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Подключаем конфигурацию из Config.py

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Инициализация Migrate
migrate = Migrate(app, db)  # Объект для миграций

# Указываем, какая страница будет использоваться для входа
login_manager.login_view = 'login'

# Регистрация функции user_loader
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

from app import routes, models


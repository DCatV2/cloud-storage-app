# Здесь создаём объект Flask и подключаем конфигурацию

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '153470'

from app import routes # Импортируем маршруты
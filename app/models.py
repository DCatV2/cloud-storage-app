from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False, default="user")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_created}')"

    # Метод для установки пароля (хеширование)
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Метод для проверки пароля
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # проверяем, администратор ли пользователь
    def is_admin(self):
        return self.role == "admin"

# Модель файла
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False) # Имя файла
    filepath = db.Column(db.String(255), nullable=False) # Путь к файлу
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow) # Дата загрузки
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # ID пользователя, который загрузил файл
    user = db.relationship('User', backref=db.backref('files', lazy=True)) # Связь с пользователем

    def __repr__(self):
        return f"File('{self.filename}', '{self.filepath}', '{self.uploaded_at}')"
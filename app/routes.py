# Простая главная страница
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import User
from flask_login import login_user, login_required

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Находим пользователя по имени
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Проверка пароля
            login_user(user)  # Входим в систему
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))  # Переход на главную страницу
        else:
            flash('Неверный логин или пароль', 'danger')  # Сообщение о неправильных данных
    
    return render_template('login.html')

@app.route("/")
@login_required
def index():
    return render_template('index.html')  # Загружаем HTML-шаблон
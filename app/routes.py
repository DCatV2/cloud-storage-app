# Простая главная страница
from flask import render_template, url_for, flash, redirect, request, send_from_directory
from app import app, db
from app.models import User
from flask_login import login_user, login_required, logout_user
import os
from werkzeug.utils import secure_filename
import unicodedata

# Маршрут авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Находим пользователя по имени
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Проверка пароля
            login_user(user)  # Входим в систему
            flash('Вы успешно вошли!', 'alert-success')
            return redirect(url_for('index'))  # Переход на главную страницу
        else:
            flash('Неверный логин или пароль', 'alert-danger')  # Сообщение о неправильных данных
    
    return render_template('login.html')


# Главная страница
@app.route("/")
@login_required
def index():
    files = os.listdir(app.config["UPLOAD_FOLDER"]) if os.path.exists(app.config["UPLOAD_FOLDER"]) else []
    return render_template("index.html", files=files)

# Выход из системы
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы.", "alert-info")
    return redirect(url_for('login')) # Перенаправляем на страницу входа

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads") # Папка для сохранения файлов
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt', 'docx', 'xls', 'xlsx', 'dwg', 'dxf'} # Разрешённые форматы

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Добавляем путь в конфиг

# Создаём папку, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Функция проверки допустимого типа файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Функция нормализации имени файла, чтобы сохранять кириллицу
def normalize_filename(filename):
    return unicodedata.normalize("NFC", filename)

# Маршрут для загрузки файлов
@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if "file" not in request.files:
        flash("Файл не выбран!", "alert-danger")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("Файл не выбран!", "alert-danger")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        safe_filename = secure_filename(file.filename) # Безопасное имя
        original_filename = normalize_filename(file.filename) # Сохраняем кириллицу
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], original_filename)
        file.save(file_path)
        flash(f"Файл '{original_filename}' успешно загружен!", "alert-success")
    else:
        flash("Недопустимый формат файла!", "alert-danger")

    return redirect(url_for("index"))

# Маршрут для скачивания файлов
@app.route("/download/<filename>")
@login_required
def download_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
    else:
        flash("Файл не найден!", "alert-danger")
        return redirect(url_for("index"))

# Маршрут для удаления файлов
@app.route("/delete/<filename>", methods=["POST"])
@login_required
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if os.path.exists(file_path): # Проверяем, существует ли файл
        os.remove(file_path) # Удаляем файл
        flash(f"Файл {filename} удалён!", "alert-success")
    else:
        flash("Файл не найден!", "alert-danger")

    return redirect(url_for("index"))
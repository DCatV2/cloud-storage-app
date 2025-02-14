# Простая главная страница

from app import app
from flask import render_template

@app.route('/')
def home():
    return 'Hello, Flask!'
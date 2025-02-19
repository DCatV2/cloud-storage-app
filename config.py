import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '153470'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Devilmaycry@localhost/dcat'  # Подключение к PostgreSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

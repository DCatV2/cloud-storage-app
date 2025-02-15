import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Devilmaycry@localhost/dcat'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

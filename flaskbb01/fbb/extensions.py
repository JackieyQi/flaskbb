# coding:utf8

from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache


csrf = CSRFProtect()

db = SQLAlchemy()

login_manager = LoginManager()

cache = Cache()
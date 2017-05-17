# coding:utf8
from flask import Flask
from flask_login import current_user
from fbb.user.views import user
from fbb.user.models import Guest, User

from fbb.extensions import (csrf, db, login_manager, cache)


from fbb.utils.helpers import time_utcnow
from fbb.utils.settings import flaskbb_config

def create_app(config=None):
    app = Flask("fbb")

    configure_app(app, config)
    # configure_celery_app(app, celery)
    configure_blueprints(app)
    configure_extensions(app)
    # configure_template_filters(app)
    configure_context_processors(app)
    configure_before_handlers(app)

def configure_app(app, config):
    app.config.from_object("fbb.configs.default.DefaultConfig")

def configure_blueprints(app):
    app.register_blueprint(user, url_prefix=app.config["USER_URL_PREFIX"])

def configure_extensions(app):
    csrf.init_app(app)
    db.init_app(app)
    cache.init_app(app)

    login_manager.login_view = app.config["LOGIN_VIEW"]
    login_manager.refresh_view = app.config["REAUTH_VIEW"]
    login_manager.login_message_category = app.config["LOGIN_MESSAGE_CATEGORY"]
    login_manager.needs_refresh_message_category = app.config["REFRESH_MESSAGE_CATEGORY"]
    login_manager.anonymous_user = Guest

    @login_manager.user_loader
    def load_user(user_id):
        user_instance = U

def configure_context_processors(app):
    @app.context_processor
    def inject_template2config():
        # 上下文处理器，用于所有模板中
        return dict(fbb_config=flaskbb_config)

def configure_before_handlers(app):
    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = time_utcnow()
            db.session.add(current_user)
            db.session.commit()

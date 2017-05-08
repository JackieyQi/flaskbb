# coding:utf8
import os


class DefaultConfig(object):
    basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__)))))

    # auth,used by login_manager
    LOGIN_VIEW = "auth.login"
    REAUTH_VIEW = "auth.refresh"
    LOGIN_MESSAGE_CATEGORY = "info"
    REFRESH_MESSAGE_CATEGORY = "info"

    USER_URL_PREFIX = "/user"

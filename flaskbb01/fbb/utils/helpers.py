# coding:utf8

from pytz import UTC
from datetime import datetime


def time_utcnow():
    return datetime.now(UTC)
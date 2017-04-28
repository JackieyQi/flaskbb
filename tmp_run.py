# coding:utf8

import os
from flaskbb.app import create_app
from flask_script import Manager

_base_path = os.path.dirname(os.path.abspath(__file__))
app = create_app(config=os.path.join(_base_path, "flaskbb.cfg"))
manager = Manager(app)
if __name__ == "__main__":
    manager.run()

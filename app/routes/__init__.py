from flask import Blueprint

main = Blueprint("main", __name__)

from .auth import auth as auth_blueprint
from .home import home as home_blueprint
from .motion_pictures import motion_pictures as motion_pictures_blueprint

main.register_blueprint(auth_blueprint)
main.register_blueprint(home_blueprint)
main.register_blueprint(motion_pictures_blueprint)

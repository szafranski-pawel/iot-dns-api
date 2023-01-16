import dataclasses
import datetime
from json import JSONEncoder
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if type(o) == datetime.timedelta:
            return str(o)
        elif type(o) == datetime.datetime:
            return o.isoformat()
        elif dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        else:
            return super().default(o)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = False
    app.json_encoder = CustomJSONEncoder

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import auth
        from . import main
        from . import api
        from . import dns
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(main.main_bp)
        app.register_blueprint(api.api_bp)
        app.register_blueprint(dns.dns_bp)

        db.create_all()

        return app

#!/usr/bin/env python3
from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Database Connection
mysql = MySQL()
db = SQLAlchemy()

# Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Using a development configuration
    app.config.from_object('config.DevConfig')

    # Database init
    mysql.init_app(app)
    db.init_app(app)

    # Login
    login_manager.init_app(app)

    # Api
    api = Api(app)

    with app.app_context():
        # Blueprint import
        from blueprints.auth import auth
        from blueprints.dlc_api import api_dlc
        from blueprints.dlc_mobile_devices import dlc_mobile_devices
        from blueprints.dlc_staff import dlc_staff
        from blueprints.dlc_staff_driving_licenses import dlc_staff_driving_licenses
        from blueprints.dlc_user_logins import dlc_user_logins
        from blueprints.main import main

        # Blueprint register
        app.register_blueprint(auth)
        app.register_blueprint(dlc_mobile_devices)
        app.register_blueprint(dlc_staff)
        app.register_blueprint(dlc_staff_driving_licenses)
        app.register_blueprint(dlc_user_logins)
        app.register_blueprint(main)

        # Add Api URL endpoint
        api.add_resource(api_dlc, '/api/dlc')

        return app

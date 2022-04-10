"""Database models."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app_dlc import db
import configparser

class User_dlc(UserMixin):
    def __init__(self, id="dlcadmin", active=True):
        self.name = ""
        self.password =""
        self.id = id
        self.active = active
        self._read_username_password()

    def _read_username_password(self):
        """Read username and password from /home/pi/dlt/conf/dlt.conf"""
        config = configparser.ConfigParser()
        config.read('/home/pi/dlt/config/dlc.conf')
        name = ""
        password = ""
        try:
            name = config['user']['name']
        except Exception as e:
            self.name = "dlcadmin"
        else:
            self.name = name
        try:
            password = config['user']['password']
        except Exception as e:
            password_hash = generate_password_hash('admin')
            self.password = password_hash
        else:
            self.password = password

    def check_password(self, input_password):
        """Returns true if input_password is correct"""
        return check_password_hash(self.password, input_password)

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'user_logins'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    staff_id = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

#https://blog.miguelgrinberg.com/post/two-factor-authentication-with-flask
#pip install flask-login
#pip install flask-sqlalchemy
#pip install flask-bootstrap
#pip install flask_wtf
#pip install onetimepass
#pip install PyQRCode

from werkzeug.security import generate_password_hash, check_password_hash
#from flask.ext.login import UserMixin
from flask_login import UserMixin
from app import db, lm

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

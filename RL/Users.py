from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class trader(UserMixin, db.Model):
#    _tablename_ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    trade_freq = db.Column(db.String(), nullable = True)

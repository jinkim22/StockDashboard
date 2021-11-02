from flask import Flask, render_template, request,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from wtf_form import *
from Users import trader
#pip install -U Flask-WTF
#pip3 install flask-login


app = Flask(__name__)
app.secret_key = 'COMS4111'

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:8080@localhost/trader'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Configure login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return trader.query.get(int(id))
"""
class trader(db.Model):
    _tablename_ = "trader"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    trade_freq = db.Column(db.String(), nullable = True)
"""

@app.route('/', methods = ['GET', 'POST'])
#@app.route('/')
def index():
#    return "hello"

    reg_form = RegistrationForm()
    """
    if reg_form.validate_on_submit():
       return 'GREAT SUCESS'
"""
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        user_object = trader.query.filter_by(username=username).first()
        if user_object:
            return "Username exist"

        user = trader(username = username, password= password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    #    return "Great success!"
    return render_template("index.html", form = reg_form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_ob = trader.query.filter_by(username = login_form.username.data).first()
        login_user(user_ob)
        return redirect(url_for('portfolio'))
    #    if current_user.is_authenticated:
    #        return "Logged in"
        return "Not logged"

    return render_template("login.html", form = login_form)

@app.route("/portfolio", methods=['GET', 'POST'])
#@login_required
def portfolio():
    if not current_user.is_authenticated:
        return "please log first"
    return "this is portfolio"

@app.route("/logout", methods = ['GET'])
def logout():
    logout_user()
    return "logged out"

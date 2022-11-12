from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
# import cx_Oracle
from flask_login import LoginManager

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'oracle://hr:hr@127.0.0.1:1521/xe'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://ovvipwjohlmjjv:86b4edb3c754eef2789f1c68e2abe6f189a747a03946b1128a55a3ad8981ed82@ec2-3-209-39-2.compute-1.amazonaws.com:5432/deqpsm1nalqfv5'
app.config['SECRET_KEY'] = 'hello123hello'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from poll import routes

with app.app_context():
    # db.drop_all()
    # print('db dropped')
    db.create_all()
    print('db created')

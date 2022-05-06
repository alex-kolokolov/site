from flask import Flask, render_template, abort, redirect
import os
from flask_login import LoginManager, login_user
from data import db_session
from data.items import Furniture
from data.role import Role, roles_to_users
from data.user import User
from data.images import Images
from sqlalchemy import orm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
from forms import LoginForm, RegisterForm
from auth import auth
from products import products
from admin import admin

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(admin, url_prefix='/admin')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_page():
    return render_template('index.html', title='Домашняя страница', )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_session.global_init("db/items.db")
    # for i in range(12):
    #     user = Furniture()
    #     user.name = "Полка 1"
    #     user.about = "Полка крутая"
    #     image = Image(name='../static/img/полка1.png')
    #     user.image.append(image)
    #     db_sess = db_session.create_session()
    #
    #     db_sess.commit()

    # db_sess = db_session.create_session()
    # admin = Role(name='Admin')
    # user = Role(name='User')
    # db_sess = db_session.create_session()
    # db_sess.add(admin)
    # db_sess.add(user)
    # user = db_sess.query(Furniture).filter(Furniture.id == 1).first()
    # image = Image(name='../static/img/полка1.png')
    # user.image.append(image)
    # db_sess.commit()
    # for i in user.image:
    #     print(i.name)

    app.run(host='0.0.0.0', port=port)

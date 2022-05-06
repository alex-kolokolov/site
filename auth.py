from flask import Blueprint, render_template
from flask import Flask, render_template, abort, redirect
import os
from flask_login import LoginManager, login_user, login_required, logout_user
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
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth_bp', __name__,
                 template_folder='templates',
                 static_folder='static', static_url_path='assets')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Authorization', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password_confirmation.data:
            if validate_email(form.email.data):
                db_sess = db_session.create_session()
                user = User()
                user.name = form.name.data
                user.email = form.email.data
                user.hashed_password = generate_password_hash(form.password.data)
                user.about = ''
                if form.admin.data:
                    role = db_sess.query(Role).filter_by(name='Admin').first()

                    # Если категории нет, создадим её
                    if role is None:

                        role = Role(name='Admin')
                        db_sess.add(role)

                        # Используем flush, чтобы получить id категории, которая будет добавлена
                        db_sess.flush()

                    user.role.append(role)
                else:
                    role = db_sess.query(Role).filter_by(name='User').first()

                    # Если категории нет, создадим её
                    if role is None:
                        role = Role(name='User')
                        db_sess.add(role)

                        # Используем flush, чтобы получить id категории, которая будет добавлена
                        db_sess.flush()

                    user.role.append(role)

                db_sess.add(user)
                db_sess.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            else:
                return render_template('register.html',
                                       message="Неверный адрес почты",
                                       form=form)
        else:
            return render_template('register.html',
                                   message="Пароли не совпадают",
                                   form=form)
    return render_template('register.html', title='регистрация', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

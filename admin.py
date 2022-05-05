import flask_login
from flask import Blueprint, render_template, request
from flask import Flask, render_template, abort, redirect, flash, request, redirect, url_for
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.items import Furniture
from data.role import Role, roles_to_users
from data.user import User
from data.images import Images
from sqlalchemy import orm
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
from forms import LoginForm, RegisterForm, ItemForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from email_validator import validate_email

UPLOAD_FOLDER = '../static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
admin = Blueprint('admin_bp', __name__,
                  template_folder='templates',
                  static_folder='static', static_url_path='assets')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin.route('/products')
@login_required
def items_page():
    user_id = flask_login.current_user.id
    db_sess = db_session.create_session()
    a = db_sess.query(User).filter_by(id=user_id).first().role[0]
    print(type(a))
    print(db_sess.query(User).filter_by(id=user_id).first().role[0].name == 'Admin')
    print(db_sess.query(Role).get(0))
    if db_sess.query(User).filter_by(id=user_id).first().role[0].name == 'Admin':
        items = db_sess.query(Furniture)
        for i in items:
            print(i.image[0].image)
        return render_template("admin_products.html", title='Товары', items=items)
    else:
        abort(404)


@admin.route('products/<int:id>', methods=['GET'])
@login_required
def product_page(id):
    db_sess = db_session.create_session()
    item = db_sess.query(Furniture).filter(Furniture.id == id).first()
    if item:
        return render_template("product.html", title=f'{item.name}', item=item)
    else:
        abort(404)


@admin.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_news():
    form = ItemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        item = Furniture()
        item.name = form.title.data
        item.about = form.content.data
        f = form.fileName.data
        filename = secure_filename(f.filename)
        if allowed_file(filename) and filename != '':
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'static\\img\\{filename}')
            print(file_path)
            f.save(file_path)
            image = Images(image=f'../static/img/{filename}')
            item.image.append(image)
            db_sess.add(item)
            db_sess.add(image)
            db_sess.commit()
            redirect('/admin/products')
        else:
            return render_template('add_item.html',
                                   message="Неверный формат файла",
                                   form=form)
    return render_template('add_item.html', title='Добавление новости',
                           form=form)


@admin.route('/product_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    item = db_sess.query(Furniture).filter(Furniture.id == id).first()
    if item:
        try:
            os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   f'static\\img\\{item.image[0].image.split("/")[-1]}'))
        except:
            pass
        db_sess.delete(item)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/admin/products')

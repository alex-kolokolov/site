from flask import Blueprint, render_template
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

products = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')


@products.route('/')
def items_page():
    db_session.global_init("db/items.db")
    db_sess = db_session.create_session()
    items = db_sess.query(Furniture)
    for item in items:
        print(item.image[0].image)
    return render_template("items.html", title='Товары', items=items)


@products.route('/<int:id>', methods=['GET'])
def product_page(id):
    db_session.global_init("db/items.db")
    db_sess = db_session.create_session()
    item = db_sess.query(Furniture).filter(Furniture.id == id).first()
    if item:
        return render_template("product.html", title=f'{item.name}', item=item)
    else:
        abort(404)
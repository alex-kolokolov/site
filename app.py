from flask import Flask, render_template
import os
from data import db_session
from data.items import Furniture
from sqlalchemy import orm

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main_page():  # put application's code here
    db_session.global_init("db/items.db")
    return render_template('index.html', title='Домашняя страница', )


@app.route('/items')
def items_page():
    db_session.global_init("db/items.db")
    return render_template("items.html", title='Товары')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

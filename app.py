import time

from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import FlaskForm

import wtforms.validators as wt_val

from wtforms import StringField, FloatField, BooleanField, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////work/database/db1.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'asdfasdfasdf'
app.config['PORT'] = 5001

db = SQLAlchemy(app)

class Item(db.Model):

    STATUS_ACTIVE = 0
    STATUS_DELETED = 1

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    static_enabled = db.Column(db.Boolean, nullable=False, default=False)

class NewItemForm(FlaskForm):

    title = StringField('title', validators=[wt_val.DataRequired()])
    price = FloatField('price', validators=[wt_val.DataRequired()])
    static_enabled = BooleanField('static_enabled', default=False)
    submit_field = SubmitField()


@app.route('/')
def hello():
    items = Item.query.all()
    return render_template(
        'items.html',
        items=items,
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = NewItemForm()
    if request.method == 'POST' and form.validate():
        item = Item()
        item.title = form.title.data
        item.static_enabled = form.static_enabled.data
        item.price = form.price.data
        db.session.add(item)
        db.session.commit()
        if item.static_enabled:
            make_static_page(item)
        return redirect('/')
    return render_template('new.html', form=form)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def item(id):
    time.sleep(1)
    return render_template('item_page.html', item=Item.query.get_or_404(id))


def make_static_page(item):
    with open('/work/static_pages/{}.html'.format(item.id), 'w') as o:
        o.write(render_template('item_page.html', item=item))


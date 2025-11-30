
from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os, io, csv, zipfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    day = db.Column(db.String(20))
    name = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    image = db.Column(db.String(200))

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.route('/')
def index():
    meals = Meal.query.order_by(Meal.week, Meal.id).all()
    return render_template('index.html', meals=meals)

@app.route('/shopping')
def shopping():
    meals = Meal.query.all()
    items = []
    for m in meals:
        for ing in m.ingredients.split(','):
            items.append(ing.strip())
    items = sorted(list(set(items)))
    return render_template('shopping.html', items=items)

@app.route('/export')
def export():
    meals = Meal.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Week','Day','Meal','Ingredients','Instructions'])
    for m in meals:
        writer.writerow([m.week,m.day,m.name,m.ingredients,m.instructions])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='meals_export.csv')

@app.route('/add', methods=['POST'])
def add():
    week = request.form['week']
    day = request.form['day']
    name = request.form['name']
    ing = request.form['ingredients']
    inst = request.form['instructions']
    file = request.files.get('image')
    filename = None
    if file and file.filename:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    m = Meal(week=week, day=day, name=name, ingredients=ing, instructions=inst, image=filename)
    db.session.add(m)
    db.session.commit()
    return redirect('/')

if __name__=='__main__':
    if not os.path.exists('meals.db'):
        with app.app_context():
            db.create_all()
    app.run(host='0.0.0.0', debug=True)

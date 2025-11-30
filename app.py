from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")

# SQLite DB
db_path = os.path.join(os.path.dirname(__file__), "meals.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    week = db.Column(db.Integer)
    day = db.Column(db.String(20))
    name = db.Column(db.String(200))
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    image = db.Column(db.String(200))

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# Routes
@app.route('/')
@login_required
def index():
    meals = Meal.query.filter_by(user_id=current_user.id).order_by(Meal.week, Meal.id).all()
    return render_template("shopping.html", meals=meals)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if User.query.filter_by(username=u).first():
            return "User already exists"
        user = User(username=u, password=generate_password_hash(p))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = User.query.filter_by(username=u).first()
        if user and check_password_hash(user.password, p):
            login_user(user)
            return redirect('/')
        return "Invalid username or password"
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/add', methods=['POST'])
@login_required
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

    m = Meal(
        user_id=current_user.id,
        week=week,
        day=day,
        name=name,
        ingredients=ing,
        instructions=inst,
        image=filename
    )
    db.session.add(m)
    db.session.commit()
    return redirect('/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
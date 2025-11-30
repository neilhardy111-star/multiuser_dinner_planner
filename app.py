from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# --- Dummy user ---
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# For simplicity, a single demo user
demo_user = User(1, "neilhardy")

@login_manager.user_loader
def load_user(user_id):
    if str(user_id) == str(demo_user.id):
        return demo_user
    return None

# --- Routes ---
@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    login_user(demo_user)
    return redirect(url_for("shopping"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/shopping")
@login_required
def shopping():
    # Sample meals
    meals = [
        {
            "id": 1,
            "week": 1,
            "day": "Monday",
            "name": "Spaghetti Bolognese",
            "ingredients": "Spaghetti, Beef, Tomato Sauce",
            "instructions": "Cook spaghetti. Cook beef. Mix with sauce.",
            "image": "spaghetti.jpg"
        },
        {
            "id": 2,
            "week": 1,
            "day": "Tuesday",
            "name": "Chicken Salad",
            "ingredients": "Chicken, Lettuce, Tomato, Dressing",
            "instructions": "Grill chicken. Chop veggies. Mix.",
            "image": "salad.jpg"
        },
        {
            "id": 3,
            "week": 1,
            "day": "Wednesday",
            "name": "Vegetable Stir Fry",
            "ingredients": "Broccoli, Carrots, Bell Pepper, Soy Sauce",
            "instructions": "Stir fry vegetables with soy sauce.",
            "image": None
        }
    ]
    return render_template("shopping.html", meals=meals)

if __name__ == "__main__":
    app.run(debug=True)

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
    # Sample 2-week meals
    sample_meals = [
        {"name": "Spaghetti Bolognese", "ingredients": "Spaghetti, Beef, Tomato Sauce", "instructions": "Cook spaghetti. Cook beef. Mix with sauce.", "image": "spaghetti.jpg"},
        {"name": "Chicken Salad", "ingredients": "Chicken, Lettuce, Tomato, Dressing", "instructions": "Grill chicken. Chop veggies. Mix.", "image": "salad.jpg"},
        {"name": "Vegetable Stir Fry", "ingredients": "Broccoli, Carrots, Bell Pepper, Soy Sauce", "instructions": "Stir fry vegetables with soy sauce.", "image": "stirfry.jpg"},
        {"name": "Chicken Curry", "ingredients": "Chicken, Curry Powder, Coconut Milk", "instructions": "Cook chicken. Add curry powder and coconut milk.", "image": "chickencurry.jpg"},
        {"name": "Omelette", "ingredients": "Eggs, Cheese, Ham", "instructions": "Beat eggs. Add fillings. Cook.", "image": "omelette.jpg"},
        {"name": "Tacos", "ingredients": "Taco Shells, Beef, Lettuce, Cheese", "instructions": "Cook beef. Assemble tacos.", "image": "taco.jpg"},
        {"name": "Pizza", "ingredients": "Dough, Tomato Sauce, Cheese, Toppings", "instructions": "Assemble and bake pizza.", "image": "pizza.jpg"},
        {"name": "Soup", "ingredients": "Vegetables, Broth", "instructions": "Chop vegetables. Boil in broth.", "image": "soup.jpg"},
        {"name": "Sandwich", "ingredients": "Bread, Ham, Cheese, Lettuce", "instructions": "Assemble sandwich.", "image": "sandwich.jpg"},
        {"name": "Lasagna", "ingredients": "Pasta Sheets, Beef, Tomato Sauce, Cheese", "instructions": "Layer ingredients and bake.", "image": "lasagna.jpg"},
        {"name": "Sushi", "ingredients": "Rice, Nori, Fish, Vegetables", "instructions": "Roll sushi.", "image": "sushi.jpg"},
        {"name": "Burger", "ingredients": "Buns, Beef Patty, Lettuce, Tomato", "instructions": "Cook patty. Assemble burger.", "image": "burger.jpg"},
        {"name": "Quiche", "ingredients": "Pastry, Eggs, Cheese, Vegetables", "instructions": "Mix filling. Bake in pastry.", "image": "quiche.jpg"},
        {"name": "Pasta Alfredo", "ingredients": "Pasta, Cream, Cheese", "instructions": "Cook pasta. Add sauce.", "image": "pasta.jpg"},
    ]

    # Assign meals to 2 weeks, 7 days per week
    meals = []
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    week = 1
    meal_id = 1
    for i in range(14):
        meal = sample_meals[i % len(sample_meals)].copy()
        meal["week"] = week
        meal["day"] = day_names[i % 7]
        meal["id"] = meal_id
        meals.append(meal)
        meal_id += 1
        if (i+1) % 7 == 0:
            week += 1

    return render_template("shopping.html", meals=meals)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from models import db, User

app = Flask(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
app.config["SECRET_KEY"]          = "change-this-before-going-to-production"
app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///bugtracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ── Extensions ─────────────────────────────────────────────────────────────────
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view     = "login"        # redirect here if @login_required fails
login_manager.login_message  = "Please log in to access that page."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


# ── Create tables on first run ─────────────────────────────────────────────────
with app.app_context():
    db.create_all()


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Already logged in — nothing to do here
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email",    "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm",  "")

        # ── Validation ─────────────────────────────────────────────────────────
        error = None
        if not username or not email or not password:
            error = "All fields are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."
        elif User.query.filter_by(username=username).first():
            error = "Username is already taken."
        elif User.query.filter_by(email=email).first():
            error = "An account with that email already exists."

        if error:
            flash(error, "danger")
            return render_template("signup.html",
                                   username=username, email=email)

        # ── Create user ────────────────────────────────────────────────────────
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Auto-login after signup
        login_user(user)
        flash(f"Welcome, {user.username}! Your account has been created.", "success")
        return redirect(url_for("dashboard"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()  # username or email
        password   = request.form.get("password",   "")
        remember   = request.form.get("remember") == "on"

        # Look up by username first, then email
        user = (
            User.query.filter_by(username=identifier).first() or
            User.query.filter_by(email=identifier.lower()).first()
        )

        if not user or not user.check_password(password):
            flash("Invalid username/email or password.", "danger")
            return render_template("login.html", identifier=identifier)

        login_user(user, remember=remember)
        flash(f"Welcome back, {user.username}!", "success")

        # Honour ?next= redirect (set by Flask-Login when bouncing to /login)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
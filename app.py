from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from datetime import datetime
from models import db, User, Bug

app = Flask(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
app.config["SECRET_KEY"]                     = "change-this-before-going-to-production"
app.config["SQLALCHEMY_DATABASE_URI"]        = "sqlite:///bugtracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ── Extensions ─────────────────────────────────────────────────────────────────
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view             = "login"
login_manager.login_message          = "Please log in to access that page."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# ── Auth routes ────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email",    "").strip().lower()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm",  "")

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
            return render_template("signup.html", username=username, email=email)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome, {user.username}! Your account has been created.", "success")
        return redirect(url_for("dashboard"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password   = request.form.get("password",   "")
        remember   = request.form.get("remember") == "on"

        user = (
            User.query.filter_by(username=identifier).first() or
            User.query.filter_by(email=identifier.lower()).first()
        )

        if not user or not user.check_password(password):
            flash("Invalid username/email or password.", "danger")
            return render_template("login.html", identifier=identifier)

        login_user(user, remember=remember)
        flash(f"Welcome back, {user.username}!", "success")
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ── Dashboard ──────────────────────────────────────────────────────────────────

@app.route("/dashboard")
@login_required
def dashboard():
    open_count        = Bug.query.filter_by(status="Open").count()
    in_progress_count = Bug.query.filter_by(status="In Progress").count()
    closed_count      = Bug.query.filter_by(status="Closed").count()
    total_count       = Bug.query.count()
    assigned_to_me    = Bug.query.filter_by(
                            assigned_to=current_user.id
                        ).filter(Bug.status != "Closed").count()
    recent_bugs       = Bug.query.order_by(Bug.created_at.desc()).limit(5).all()

    return render_template("dashboard.html",
                           open_count=open_count,
                           in_progress_count=in_progress_count,
                           closed_count=closed_count,
                           total_count=total_count,
                           assigned_to_me=assigned_to_me,
                           recent_bugs=recent_bugs)


# ── Bug routes ─────────────────────────────────────────────────────────────────

@app.route("/bugs")
@login_required
def bugs():
    status_filter    = request.args.get("status",    "")
    priority_filter  = request.args.get("priority",  "")
    assignee_filter  = request.args.get("assignee",  "")   # "me" | "none" | ""

    query = Bug.query

    if status_filter in Bug.STATUSES:
        query = query.filter_by(status=status_filter)
    if priority_filter in Bug.PRIORITIES:
        query = query.filter_by(priority=priority_filter)
    if assignee_filter == "me":
        query = query.filter_by(assigned_to=current_user.id)
    elif assignee_filter == "none":
        query = query.filter(Bug.assigned_to.is_(None))

    all_bugs = query.order_by(Bug.created_at.desc()).all()

    return render_template("bugs.html",
                           bugs=all_bugs,
                           status_filter=status_filter,
                           priority_filter=priority_filter,
                           assignee_filter=assignee_filter,
                           statuses=Bug.STATUSES,
                           priorities=Bug.PRIORITIES)


@app.route("/bugs/create", methods=["GET", "POST"])
@login_required
def create_bug():
    users = User.query.order_by(User.username).all()

    if request.method == "POST":
        title       = request.form.get("title",       "").strip()
        description = request.form.get("description", "").strip()
        priority    = request.form.get("priority",    "Medium")
        assignee_id = request.form.get("assigned_to", "")

        error = None
        if not title:
            error = "Title is required."
        elif not description:
            error = "Description is required."
        elif priority not in Bug.PRIORITIES:
            error = "Invalid priority."

        if error:
            flash(error, "danger")
            return render_template("create_bug.html",
                                   priorities=Bug.PRIORITIES,
                                   users=users,
                                   form=request.form)

        bug = Bug(
            title       = title,
            description = description,
            priority    = priority,
            status      = "Open",
            created_by  = current_user.id,
            assigned_to = int(assignee_id) if assignee_id else None,
        )
        db.session.add(bug)
        db.session.commit()
        flash(f"Bug #{bug.id} created successfully.", "success")
        return redirect(url_for("bug_detail", bug_id=bug.id))

    return render_template("create_bug.html",
                           priorities=Bug.PRIORITIES,
                           users=users,
                           form={})


@app.route("/bugs/<int:bug_id>")
@login_required
def bug_detail(bug_id):
    bug   = Bug.query.get_or_404(bug_id)
    users = User.query.order_by(User.username).all()
    return render_template("bug_detail.html",
                           bug=bug,
                           users=users,
                           statuses=Bug.STATUSES,
                           priorities=Bug.PRIORITIES)


@app.route("/bugs/<int:bug_id>/assign", methods=["POST"])
@login_required
def assign_bug(bug_id):
    bug     = Bug.query.get_or_404(bug_id)
    user_id = request.form.get("user_id", "")

    if user_id == "":
        bug.assigned_to = None
    else:
        user = User.query.get(int(user_id))
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("bug_detail", bug_id=bug_id))
        bug.assigned_to = user.id

    bug.updated_at = datetime.utcnow()
    db.session.commit()
    flash("Bug assignment updated.", "success")
    return redirect(url_for("bug_detail", bug_id=bug_id))


@app.route("/bugs/<int:bug_id>/assign-me", methods=["POST"])
@login_required
def assign_to_me(bug_id):
    """One-click assign the bug to the currently logged-in user."""
    bug             = Bug.query.get_or_404(bug_id)
    bug.assigned_to = current_user.id
    bug.updated_at  = datetime.utcnow()
    db.session.commit()
    flash("Bug assigned to you.", "success")
    return redirect(url_for("bug_detail", bug_id=bug_id))


@app.route("/bugs/<int:bug_id>/status", methods=["POST"])
@login_required
def update_status(bug_id):
    bug        = Bug.query.get_or_404(bug_id)
    new_status = request.form.get("status", "")

    if new_status not in Bug.STATUSES:
        flash("Invalid status.", "danger")
        return redirect(url_for("bug_detail", bug_id=bug_id))

    bug.status     = new_status
    bug.updated_at = datetime.utcnow()
    db.session.commit()
    flash(f"Status updated to '{new_status}'.", "success")
    return redirect(url_for("bug_detail", bug_id=bug_id))


@app.route("/test-s3")
def test_s3():
    return "Test route active."


if __name__ == "__main__":
    app.run(debug=True)
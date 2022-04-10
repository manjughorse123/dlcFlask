from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask import current_app
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

main = Blueprint('main', __name__)


@main.route("/")
@login_required
def index():
    return render_template("dlc_main_bs.html")

@main.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth.login'))

from functools import wraps

from flask import Blueprint, session, redirect, render_template, request
from werkzeug.security import check_password_hash

bp = Blueprint("auth", __name__)

password_hash = "scrypt:32768:8:1$gMLD6QaAn4Jc9O8G$b8b2b3f363d804c6e4feb453f71150eb620f3cf6b72d2e89d90f0a954496f51d68ac9048e329698db50a7d370c48a8ebd45ac7f92f6342be406dd8cba398b053"


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check password
        password = request.form["password"].lower()  # Case-insensitive
        if check_password_hash(password_hash, password):
            # Password correct, store in session and redirect using session url if set
            redirect_url = session.get("redirect", "/")
            session.clear()
            session.permanent = True
            session["password"] = password
            return redirect(redirect_url)
        return render_template("/pluseen/login.html", error_msg="Wachtwoord incorrect")
    # GET, render login page
    return render_template("/pluseen/login.html")


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        # Check if password is correct
        password: str | None = session.get("password")
        if password is not None and check_password_hash(password_hash, password):
            # Password correct, continue to view
            return view(**kwargs)
        # Password not set or incorrect, store url and continue to login page
        session["redirect"] = request.url
        return redirect("/login")

    return wrapped_view

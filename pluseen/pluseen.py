from flask import Blueprint, render_template, request

from pluseen import db

bp = Blueprint("pluseen", __name__)


@bp.route("/", methods=["GET"])
def home():
    """Overview of all options"""
    return render_template("/pluseen/home.html")


@bp.route("/pluseens", methods=["GET"])
def list_pluseens():
    """List pluseens"""
    pluseens = db.list_pluseens()
    return render_template("/pluseen/list_pluseens.html", pluseens=pluseens)


# @bp.route("/pluseens", methods=["POST"])
# def remove_pluseen():
#     """Remove pluseen (accessible from list_pluseens)"""
#     pluseen_name: str = request.form["pluseen_name"]
#     pluseen = db.get_pluseen(pluseen_name)
#     if pluseen is None:
#         return render_template("/pluseen/pluseen_not_found.html", pluseen_name=pluseen_name)
#     db.remove_pluseen(pluseen.id)
#     return render_template("/pluseen/removed_pluseen.html", pluseen_name=pluseen_name)


@bp.route("/pluseens/add", methods=["GET"])
def create_pluseen():
    """Add new pluseen"""
    return render_template("/pluseen/create_pluseen.html")


@bp.route("/pluseens/add", methods=["POST"])
def add_pluseen():
    """Adds new pluseen (accessible from create_pluseen)"""
    pluseen_name: str = request.form["pluseen_name"]
    if '/' in pluseen_name:
        return render_template("/pluseen/create_pluseen.html", error_msg="Pluseen naam mag geen \"/\" bevatten.")
    elif db.get_pluseen(pluseen_name) is not None:
        return render_template("/pluseen/create_pluseen.html", error_msg="Pluseen met dezelfde naam bestaat al.")
    db.add_pluseen(pluseen_name)
    return render_template("/pluseen/created_pluseen.html", pluseen_name=pluseen_name)


@bp.route("/deelnemers", methods=["GET"])
def list_deelnemers():
    """List deelnemers"""
    deelnemers = db.list_deelnemers()
    return render_template("/pluseen/list_deelnemers.html", deelnemers=deelnemers)


# @bp.route("/deelnemers", methods=["POST"])
# def remove_deelnemer():
#     """Removes deelnemer (accessible from list_deelnemers)"""
#     deelnemer_name: str = request.form["deelnemer_name"]
#     deelnemer = db.get_deelnemer(deelnemer_name)
#     if deelnemer is None:
#         return render_template("/pluseen/deelnemer_not_found.html", deelnemer_name=deelnemer_name)
#     db.remove_deelnemer(deelnemer.id)
#     return render_template("/pluseen/removed_deelnemer.html", deelnemer_name=deelnemer_name)


@bp.route("/deelnemers/add", methods=["GET"])
def create_deelnemer():
    """Add new deelnemer"""
    return render_template("/pluseen/create_deelnemer.html")


@bp.route("/deelnemers/add", methods=["POST"])
def add_deelnemer():
    """Adds new deelnemer (accessible from create_deelnemer)"""
    deelnemer_name: str = request.form["deelnemer_name"]
    if db.get_deelnemer(deelnemer_name) is not None:
        return render_template("/pluseen/create_deelnemer.html", error_msg="Deelnemer met dezelfde naam bestaat al.")
    db.add_deelnemer(deelnemer_name)
    return render_template("/pluseen/created_deelnemer.html", deelnemer_name=deelnemer_name)


@bp.route("/pluseen/<pluseen_name>", methods=["GET"])
def get_pluseen_statuses(pluseen_name: str):
    """Gets pluseen statuses"""
    pluseen = db.get_pluseen(pluseen_name)
    if pluseen is None:
        return render_template("/pluseen/pluseen_not_found.html", pluseen_name=pluseen_name)
    pluseen_statuses = db.get_statuses(pluseen.id)
    return render_template("/pluseen/pluseen_statuses.html", pluseen_name=pluseen_name, pluseen_statuses=pluseen_statuses)


@bp.route("/pluseen/<pluseen_name>", methods=["POST"])
def set_pluseen_status(pluseen_name: str):
    """Sets pluseen status (accessible from get_pluseen_statuses)"""
    pluseen = db.get_pluseen(pluseen_name)
    if pluseen is None:
        return render_template("/pluseen/pluseen_not_found.html", pluseen_name=pluseen_name)
    deelnemer_name: str = request.form["deelnemer_name"]
    deelnemer = db.get_status(pluseen.id, deelnemer_name)
    if deelnemer is None:
        return render_template("/pluseen/deelnemer_not_found.html", pluseen_name=pluseen_name, deelnemer_name=deelnemer_name)
    status = int(request.form["status"])
    if status < -1 or status > 1:
        return render_template("/pluseen/invalid_status.html", pluseen_name=pluseen_name, deelnemer_name=deelnemer_name, status=status)
    db.set_status(pluseen.id, deelnemer.id, status)
    return render_template("/pluseen/pluseen_status_changed.html", pluseen_name=pluseen_name, deelnemer_name=deelnemer_name, prev_status=deelnemer.status, status=status)

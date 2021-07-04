from typing import Optional

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


@bp.route("/pluseens/add", methods=["GET"])
def create_pluseen():
    """Add new pluseen"""
    return render_template("/pluseen/create_pluseen.html")


@bp.route("/pluseens/add", methods=["POST"])
def add_pluseen():
    """Adds new pluseen (accessible from create_pluseen)"""
    pluseen_name: str = request.form["pluseen_name"]
    if not pluseen_name or pluseen_name.isspace():
        return render_template("/pluseen/create_pluseen.html", error_msg="Pluseen naam mag niet leeg zijn.")
    if '/' in pluseen_name:
        return render_template("/pluseen/create_pluseen.html", error_msg="Pluseen naam mag geen \"/\" bevatten.")
    elif db.get_pluseen(pluseen_name) is not None:
        return render_template("/pluseen/create_pluseen.html", error_msg="Pluseen met dezelfde naam bestaat al.")
    pluseen_description: Optional[str] = request.form["pluseen_description"]
    if not pluseen_description or pluseen_description.isspace():
        pluseen_description = None
    else:
        pluseen_description = pluseen_description.replace("\r", "")
    db.add_pluseen(pluseen_name, pluseen_description)
    return render_template("/pluseen/created_pluseen.html", pluseen_name=pluseen_name)


@bp.route("/deelnemers", methods=["GET"])
def list_deelnemers():
    """List deelnemers"""
    deelnemers = db.list_deelnemers()
    return render_template("/pluseen/list_deelnemers.html", deelnemers=deelnemers)


@bp.route("/pluseen/<pluseen_name>", methods=["GET"])
def get_pluseen_statuses(pluseen_name: str):
    """Gets pluseen statuses"""
    pluseen = db.get_pluseen(pluseen_name)
    if pluseen is None:
        return render_template("/pluseen/pluseen_not_found.html", pluseen_name=pluseen_name)
    pluseen_statuses = db.get_statuses(pluseen.id)
    return render_template("/pluseen/pluseen_statuses.html", pluseen_name=pluseen_name, pluseen_description=pluseen.description, pluseen_statuses=pluseen_statuses)


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

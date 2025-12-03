# routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
)

# -------- AUTH (cookies) --------
from AUTH.auth import login, logout,register

# -------- EVENTS --------
from events.events import (
    list_events,
    create_event,
    get_event_details,
    update_event,
    delete_event,
)

# -------- MEMBERS --------
from members.members import (
    list_members,
    get_member_by_id,
    create_member,
    update_member,
    delete_member,
    view_profile,
)

# -------- CONTENT MANAGEMENT (content -> reports/submissions) --------
from content.content import (
    list_contents,
    get_content_by_id,
    create_content,
    update_content,
    delete_content,
)

# -------- REPORT MANAGEMENT --------
from content.content import (
    list_reports,
    get_report_by_id,
    create_report,
    update_report,
    delete_report,
    submit_report,
)

# -------- TEAMS --------
from teams.teams import (
    list_teams,
    get_team_by_id,
    create_team,
    update_team,
    delete_team,
)

routes = Blueprint("routes", __name__)

# AUTH ROUTES
@routes.route("/api/auth/register", methods=["POST"])
def register_route():
    return register()


@routes.route("/api/auth/login", methods=["POST"])
def login_route():
    return login()


@routes.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout_route():
    return logout()

# EVENTS ROUTES

@routes.route("/api/events", methods=["GET"])
@jwt_required()
def list_events_route():
    return list_events()  


@routes.route("/api/events/<int:event_id>", methods=["GET"])
@jwt_required()
def get_event_details_route(event_id):
    return get_event_details


@routes.route("/api/events/create", methods=["POST"])
@jwt_required()
def create_event_route():
    body, status = create_event()
    return jsonify(body), status


@routes.route("/api/events/update/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event_route(event_id):
    body, status = update_event(event_id)
    return jsonify(body), status


@routes.route("/api/events/delete/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event_route(event_id):
    body, status = delete_event(event_id)
    return jsonify(body), status

# =========================
# MEMBERS ROUTES
# =========================

@routes.route("/api/members", methods=["GET"])
@jwt_required()
def list_members_route():
    return list_members()


@routes.route("/api/members/<int:member_id>", methods=["GET"])
@jwt_required()
def get_member_route(member_id):
    body, status = get_member_by_id(member_id)
    return jsonify(body), status



@routes.route("/api/members", methods=["POST"])
@jwt_required()
def create_member_route():
    body, status = create_member()
    return jsonify(body), status


@routes.route("/api/members/<int:member_id>", methods=["PUT"])
@jwt_required()
def update_member_route(member_id):
    body, status = update_member(member_id)
    return jsonify(body), status


@routes.route("/api/members/<int:member_id>", methods=["DELETE"])
@jwt_required()
def delete_member_route(member_id):
    body, status = delete_member(member_id)
    return jsonify(body), status


@routes.route("/api/members/<int:member_id>/profile", methods=["GET"])
@jwt_required()
def view_profile_route(member_id):
    body, status = view_profile(member_id)
    return jsonify(body), status

# CONTENT MANAGEMENT ROUTES


@routes.route("/api/list_contents", methods=["GET"])
@jwt_required()
def list_contents_route():
    rows = list_contents()          
    return jsonify(rows), 200


@routes.route("/api/contents_by_id/<int:content_id>", methods=["GET"])
@jwt_required()
def get_content_route(content_id):
    body, status = get_content_by_id(content_id)
    return jsonify(body), status


@routes.route("/api/contents/create", methods=["POST"])
@jwt_required()
def create_content_route():
    body, status = create_content() 
    return jsonify(body), status


@routes.route("/api/contents/update/<int:content_id>", methods=["PUT"])
@jwt_required()
def update_content_route(content_id):
    body, status = update_content(content_id)
    return jsonify(body), status


@routes.route("/api/contents/delete/<int:content_id>", methods=["DELETE"])
@jwt_required()
def delete_content_route(content_id):
    body, status = delete_content(content_id)
    return jsonify(body), status


# ---------- REPORTS ----------
@routes.route("/api/reports", methods=["GET"])
@jwt_required()
def list_reports_route():
    result = list_reports()         
    return jsonify(result), 200


@routes.route("/api/reports/byid/<int:report_id>", methods=["GET"])
@jwt_required()
def get_report_route(report_id):
    body, status = get_report_by_id(report_id)
    return jsonify(body), status


@routes.route("/api/reports/create", methods=["POST"])
@jwt_required()
def create_report_route():
    body, status = create_report()
    return jsonify(body), status


@routes.route("/api/reports/update/<int:report_id>", methods=["PUT"])
@jwt_required()
def update_report_route(report_id):
    body, status = update_report(report_id)
    return jsonify(body), status


@routes.route("/api/reports/delete/<int:report_id>", methods=["DELETE"])
@jwt_required()
def delete_report_route(report_id):
    body, status = delete_report(report_id)
    return jsonify(body), status


@routes.route("/api/reports/<int:report_id>/submit", methods=["POST"])
@jwt_required()
def submit_report_route(report_id):
    body, status = submit_report(report_id)
    return jsonify(body), status








# TEAMS ROUTES

@routes.route("/api/teams", methods=["GET"])
@jwt_required()
def list_teams_route():
    return list_teams()


@routes.route("/api/teams/<int:team_id>", methods=["GET"])
@jwt_required()
def get_team_route(team_id):
    body , status = get_team_by_id(team_id)
    return jsonify(body),status


@routes.route("/api/teams", methods=["POST"])
@jwt_required()
def create_team_route():
    body, status = create_team()
    return jsonify(body), status


@routes.route("/api/teams/<int:team_id>", methods=["PUT"])
@jwt_required()
def update_team_route(team_id):
    body, status = update_team(team_id)
    return jsonify(body), status


@routes.route("/api/teams/<int:team_id>", methods=["DELETE"])
@jwt_required()
def delete_team_route(team_id):
    body, status = delete_team(team_id)
    return jsonify(body), status







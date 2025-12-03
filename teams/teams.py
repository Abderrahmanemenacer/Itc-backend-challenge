from extension import db
from models import Team
from flask import request,jsonify

def list_teams():
    teams = Team.query.order_by(Team.id).all()
    team =  [
        {
            "id": t.id,
            "team_name": t.team_name,
            "description": t.description,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "is_active": t.is_active,
            "members_count": len(t.members),
        }
        for t in teams
    ]
    return jsonify(team),200



def get_team_by_id(team_id):
    t = Team.query.get(team_id)
    if not t:
        return {"error": "Team not found"}, 404

    body = {
        "id": t.id,
        "team_name": t.team_name,
        "description": t.description,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "is_active": t.is_active,
        "members_count": len(t.members),
    }
    return body, 200


def create_team():
    data = request.get_json() or {}
    team_name = data.get("team_name")
    description = data.get("description")

    if not team_name:
        return {"error": "team_name is required"}, 400

    new_team = Team(
        team_name=team_name,
        description=description,
    )
    db.session.add(new_team)
    db.session.commit()

    return {"message": "Team created successfully", "id": new_team.id}, 201


def update_team(team_id):
    data = request.get_json() or {}
    t = Team.query.get(team_id)
    if not t:
        return {"error": "Team not found"}, 404

    if "team_name" in data:
        t.team_name = data["team_name"]

    if "description" in data:
        t.description = data["description"]

    if "is_active" in data:
        t.is_active = bool(data["is_active"])

    db.session.commit()
    return {"message": "Team updated successfully", "id": t.id}, 200


def delete_team(team_id):
    t = Team.query.get(team_id)
    if not t:
        return {"error": "Team not found"}, 404

    db.session.delete(t)
    db.session.commit()

    return {"message": "Team deleted successfully", "id": team_id}, 200

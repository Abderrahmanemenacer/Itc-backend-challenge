from datetime import datetime
from werkzeug.security import generate_password_hash
from extension import db
from models import Member
from flask import jsonify,request

def list_members():
    members = Member.query.order_by(Member.id).all()
    member = [
        {
            "id": m.id,
            "name": m.member_name,
            "email": m.email,
            "role": m.role,
            "level": m.level,
            "status": m.status,
            "last_active": m.last_active.isoformat() if m.last_active else None,
            "major": m.major,
            "profile_picture": m.profile_picture
        }
        for m in members
    ]
    return jsonify(member),200
def get_member_by_id(member_id):
    m = Member.query.get(member_id)
    if not m:
        return {"error": "Member not found"}, 404

    memberById =  {
        "id": m.id,
        "name": m.member_name,
        "email": m.email,
        "role": m.role,
        "level": m.level,
        "status": m.status,
        "major": m.major,
        "birthday": m.birthday.isoformat() if m.birthday else None,
        "profile_picture": m.profile_picture,
        "last_active": m.last_active.isoformat() if m.last_active else None,
    }
    return memberById,200
def create_member():
    data = request.get_json() or {}
    member_name = data.get("member_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "Member")
    major = data.get("major")
    level = data.get("level", 0)
    birthday = data.get("birthday")  

    if not member_name or not email or not password:
        return {"error": "member_name, email, password are required"}, 400

    if Member.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 400

    try:
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date() if birthday else None
    except ValueError:
        return {"error": "birthday must be 'YYYY-MM-DD'"}, 400

    new_member = Member(
        member_name=member_name,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        major=major,
        level=int(level),
        birthday=birthday_date,
        status="active",
        last_active=None,
    )

    db.session.add(new_member)
    db.session.commit()

    return {"message": "Member created successfully", "id": new_member.id}, 201


def update_member(member_id):
    data = request.get_json() or {}
    m = Member.query.get(member_id)
    if not m:
        return {"error": "Member not found"}, 404

    if "member_name" in data:
        m.member_name = data["member_name"]

    if "email" in data:
        new_email = data["email"]
        exists = Member.query.filter(Member.email == new_email, Member.id != member_id).first()
        if exists:
            return {"error": "Email already exists"}, 400
        m.email = new_email

    if "password" in data and data["password"]:
        m.password_hash = generate_password_hash(data["password"])

    if "role" in data:
        m.role = data["role"]

    if "major" in data:
        m.major = data["major"]

    if "level" in data:
        m.level = int(data["level"])

    if "status" in data:
        if data["status"] not in ("active", "inactive", "removed"):
            return {"error": "status must be active/inactive/removed"}, 400
        m.status = data["status"]

    if "birthday" in data:
        try:
            m.birthday = datetime.strptime(data["birthday"], "%Y-%m-%d").date() if data["birthday"] else None
        except ValueError:
            return {"error": "birthday must be 'YYYY-MM-DD'"}, 400

    db.session.commit()
    return {"message": "Member updated successfully", "id": m.id}, 200
def delete_member(member_id):
    m = Member.query.get(member_id)
    if not m:
        return {"error": "Member not found"}, 404

    db.session.delete(m)
    db.session.commit()
    return {"message": "Member deleted successfully", "id": member_id}, 200
def view_profile(member_id):
    return get_member_by_id(member_id)


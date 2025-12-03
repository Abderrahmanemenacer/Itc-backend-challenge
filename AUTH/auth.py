from datetime import datetime,timezone
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    unset_jwt_cookies,
    set_access_cookies,
    set_refresh_cookies
)
from extension import db
from models import Member
def register():
    data = request.get_json() or {}

    member_name = data.get("member_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "Member")
    major = data.get("major", None)

    if not member_name or not email or not password:
        return jsonify({"error": "member_name, email and password are required"}), 400

    existing = Member.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "Email already registered"}), 400

    password_hash = generate_password_hash(password)

    new_member = Member(
        member_name=member_name,
        email=email,
        password_hash=password_hash,
        role=role,
        major=major,
        level=0,
        status="active",
    )

    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member registered successfully"}), 201



def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    member = Member.query.filter_by(email=email).first()
    if not member or not check_password_hash(member.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    member.status = "active"
    member.last_active = datetime.now(timezone.utc)
    db.session.commit()

    access_token = create_access_token(identity=str(member.id))
    refresh_token = create_refresh_token(identity=str(member.id))

    resp = jsonify({
        "message": "Login successful",
        "member": {
            "id": member.id,
            "name": member.member_name,
            "email": member.email,
            "role": member.role,
            "status": member.status,
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
    })

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200
def logout():
    response = jsonify({"message": "Logged out"})
    unset_jwt_cookies(response)
    return response, 200
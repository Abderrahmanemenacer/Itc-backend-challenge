# content/content.py
from datetime import datetime,timezone
from extension import db
from models import Content, Report, Member
from flask import request,jsonify

def list_contents():
    contents = Content.query.order_by(Content.created_at).all()

    rows = []
    for c in contents:
        for r in c.reports:  # r is Report
            rows.append({
                "report_id": r.id,
                "content_id": c.id,
                "content_title": c.title,
                "content_type": c.content_type,

                "submitted_by": r.submitted_by,
                "submitted_by_name": r.member.member_name if r.member else None,

                "status": r.status,
                "submission_date": r.submission_date.isoformat() if r.submission_date else None,
                "file_path": r.file_path,
                "action": r.action,
            })

    return rows



def get_content_by_id(content_id):
    """
    Returns one content item + all its submissions (reports).
    """
    c = Content.query.get(content_id)
    if not c:
        return {"error": "Content not found"}, 404

    reports = []
    for r in c.reports:
        reports.append({
            "report_id": r.id,
            "report_title": r.title,
            "submitted_by": r.submitted_by,
            "submitted_by_name": r.member.member_name if r.member else None,
            "status": r.status,
            "submission_date": r.submission_date.isoformat() if r.submission_date else None,
            "file_path": r.file_path,
            "action": r.action,
        })

    body = {
        "content_id": c.id,
        "content_title": c.title,
        "content_type": c.content_type,
        "description": c.description,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "reports": reports,
        "reports_count": len(reports),
    }
    return body, 200


def create_content():
    data = request.get_json() or {}
    title = data.get("title")
    content_type = data.get("content_type")  
    description = data.get("description")

    if not title or not content_type:
        return {"error": "title and content_type are required"}, 400

    if content_type not in ("task", "quiz", "playlist"):
        return {"error": "content_type must be task/quiz/playlist"}, 400

    new_content = Content(
        title=title,
        content_type=content_type,
        description=description,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(new_content)
    db.session.commit()

    return {"message": "Content created successfully", "id": new_content.id}, 201


def update_content(content_id):
    data = request.get_json() or {}
    c = Content.query.get(content_id)
    if not c:
        return {"error": "Content not found"}, 404

    if "title" in data:
        c.title = data["title"]

    if "content_type" in data:
        if data["content_type"] not in ("task", "quiz", "playlist"):
            return {"error": "content_type must be task/quiz/playlist"}, 400
        c.content_type = data["content_type"]

    if "description" in data:
        c.description = data["description"]

    db.session.commit()
    return {"message": "Content updated successfully", "id": c.id}, 200


def delete_content(content_id):
    c = Content.query.get(content_id)
    if not c:
        return {"error": "Content not found"}, 404

    db.session.delete(c)
    db.session.commit()
    return {"message": "Content deleted successfully", "id": content_id}, 200



def list_reports():
    reports = Report.query.order_by(Report.id).all()
    result = []
    for r in reports:
        result.append({
            "id": r.id,
            "report_title": r.title,
            "status": r.status,
            "submission_date": r.submission_date.isoformat() if r.submission_date else None,
            "file_path": r.file_path,
            "action": r.action,
            "content_id": r.content_id,
            "content_title": r.content.title if r.content else None,
            "submitted_by": r.submitted_by,
            "submitted_by_name": r.member.member_name if r.member else None,
        })
    return result


def get_report_by_id(report_id):
    r = Report.query.get(report_id)
    if not r:
        return {"error": "Report not found"}, 404

    body = {
        "id": r.id,
        "report_title": r.title,
        "status": r.status,
        "submission_date": r.submission_date.isoformat() if r.submission_date else None,
        "file_path": r.file_path,
        "action": r.action,

        "content_id": r.content_id,
        "content_title": r.content.title if r.content else None,
        "submitted_by": r.submitted_by,
        "submitted_by_name": r.member.member_name if r.member else None,
    }
    return body, 200


def create_report():
    data = request.get_json() or {}
    content_id = data.get("content_id")
    submitted_by = data.get("submitted_by")
    title = data.get("title")

    if not content_id or not submitted_by or not title:
        return {"error": "content_id, submitted_by, title are required"}, 400

    content = Content.query.get(content_id)
    if not content:
        return {"error": "Content not found"}, 404

    member = Member.query.get(submitted_by)
    if not member:
        return {"error": "Member not found"}, 404

    new_report = Report(
        content_id=content_id,
        submitted_by=submitted_by,
        title=title,
        status="pending",
        submission_date=None,
        file_path=None,
        action="none",
    )
    db.session.add(new_report)
    db.session.commit()

    return {"message": "Report created successfully", "id": new_report.id}, 201


def update_report(report_id):
    data = request.get_json() or {}
    r = Report.query.get(report_id)
    if not r:
        return {"error": "Report not found"}, 404

    if "title" in data:
        r.title = data["title"]

    if "status" in data:
        if data["status"] not in ("pending", "submitted", "late", "approved", "revision_requested"):
            return {"error": "Invalid status"}, 400
        r.status = data["status"]

    if "action" in data:
        if data["action"] not in ("none", "send_reminder", "approve", "request_revision"):
            return {"error": "Invalid action"}, 400
        r.action = data["action"]

    if "file_path" in data:
        r.file_path = data["file_path"]

    if "submission_date" in data:
        # accept either None or ISO string
        if data["submission_date"] is None:
            r.submission_date = None
        else:
            try:
                r.submission_date = datetime.fromisoformat(data["submission_date"])
            except ValueError:
                return {"error": "submission_date must be ISO format"}, 400

    db.session.commit()
    return {"message": "Report updated successfully", "id": r.id}, 200


def delete_report(report_id):
    r = Report.query.get(report_id)
    if not r:
        return {"error": "Report not found"}, 404

    db.session.delete(r)
    db.session.commit()
    return {"message": "Report deleted successfully", "id": report_id}, 200


def submit_report(report_id):
    data = request.get_json() or {}
    r = Report.query.get(report_id)
    if not r:
        return {"error": "Report not found"}, 404

    file_path = data.get("file_path")
    if not file_path:
        return {"error": "file_path is required to submit"}, 400

    r.file_path = file_path
    r.status = "submitted"
    r.submission_date = datetime.now(timezone.utc)
    r.action = "none"

    db.session.commit()
    return {"message": "Report submitted successfully", "id": r.id}, 200

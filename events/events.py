from datetime import datetime
from extension import db
from models import Event, Member
from flask import jsonify,request


def list_events():
    events = Event.query.order_by(Event.event_date).all()

    result = []
    for event in events:
        result.append({
            "id": event.id,
            "name": event.event_name,
            "type": event.event_type,
            "date": event.event_date.isoformat() if event.event_date else None,
            "location": event.location,
            "description": event.description,
            "attendes": len(event.members),  
        })

    return jsonify(result) , 200
def get_event_details(event_id):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404


    body = {
        "id": event.id,
        "name": event.event_name,
        "type": event.event_type,
        "date": event.event_date.isoformat() if event.event_date else None,
        "location": event.location,
        "description": event.description,
        "attendes" : [m.id for m in event.members]}

    return jsonify(body), 200

def create_event():
    data = request.get_json() or {}
    name = data.get("event_name")
    event_type = data.get("event_type")
    event_date = data.get("event_date")  
    location = data.get("location")
    description = data.get("description")

    if not name or not event_type or not event_date:
        return {"error": "event_name, event_type and event_date are required"}, 400, None

    try:
        event_date = datetime.strptime(event_date, "%Y-%m-%d %H:%M")
    except ValueError:
        return {"error": "event_date must be in format 'YYYY-MM-DD HH:MM'"}, 400, None

    new_event = Event(
        event_name=name,
        event_type=event_type,
        event_date=event_date,
        location=location,
        description=description,
    )

    db.session.add(new_event)
    db.session.commit()

    return {
        "message": "Event created successfully",
        "event": {
            "id": new_event.id,
            "name": new_event.event_name,
            "type": new_event.event_type,
            "date": new_event.event_date,
            "location": new_event.location,
            "description": new_event.description,
        },
    }, 201

def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404
    data = request.get_json() or {}

    if "event_name" in data:
        event.event_name = data["event_name"]

    if "event_type" in data:
        event.event_type = data["event_type"]

    if "event_date" in data:
        try:
            event.event_date = datetime.strptime(data["event_date"], "%Y-%m-%d %H:%M")
        except ValueError:
            return {"error": "event_date must be in format 'YYYY-MM-DD HH:MM'"}, 400

    if "location" in data:
        event.location = data["location"]

    if "description" in data:
        event.description = data["description"]

    db.session.commit()

    return {"message": "Event updated successfully", "id": event.id}, 200


def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    db.session.delete(event)
    db.session.commit()

    return {"message": "Event deleted successfully", "id": event_id}, 200



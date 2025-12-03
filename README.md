# ITC Leader Dashboard Backend (Flask + PostgreSQL)

This repository contains the backend API for a “Leader Dashboard” system.  
The backend is built with Flask and returns JSON responses (no Jinja templates). It is designed to be consumed by a separate frontend (dashboard UI).

---

## 1) What this backend provides (Project Scope)

Main features implemented:

- Authentication
  - Register
  - Login (JWT tokens)
  - Logout
- Events management
  - List events
  - Get event details
  - Create / Update / Delete event
  - Attendees count based on many-to-many relationship with members
- Members management
  - List members
  - Get member by ID
  - Create / Update / Delete member
  - View profile endpoint
  - Member fields include: last_active, birthday, profile_picture
- Teams management
  - List teams
  - Get team by ID
  - Create / Update / Delete team
  - Members count (team.members length)
- Content & Reports management
  - Content: task/quiz/playlist (leader creates)
  - Report: student submission for a content item (file/status/action/submission_date)
  - One Content can have many Reports
  - API responses include submitted_by and submitted_by_name based on Report → Member relationship

---

## 2) Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy
- PostgreSQL (pgAdmin)
- Flask-JWT-Extended (JWT auth)
- Flask-CORS
- python-dotenv
- Werkzeug security (password hashing)

---

## 3) Repository Structure

Typical structure: 
ItcProject/
AUTH/
auth.py
events/
events.py
members/
members.py
teams/
teams.py
content/
content.py

init.py
routes.py
models.py
extension.py
config.py
run.py
requirements.txt (or req2.txt)
.gitignore
.env (NOT COMMITTED)

Important:
- `routes.py` holds all route decorators and connects endpoints to module functions.
- `models.py` contains table definitions and relationships.
- `config.py` loads `.env` and sets Flask configuration.
- `__init__.py` creates the app and registers the blueprint.

---

## 4) Database Design (High Level)

Entities:
- Member
- Team
- Event
- Content
- AUTh

Relations:
- Member ↔ Team (many-to-many) via `member_teams`
- Member ↔ Event (many-to-many) via `members_events`
- Content → Report (one-to-many)
- Member → Report (one-to-many)

Concept:
- Content = task/quiz/playlist created by leader
- Report = submission created by member for a content item (status + file + date + action)

---

## 5) Environment Variables (.env)

Create a `.env` file in the project root:

```env
SECRET_KEY=super-secret
JWT_SECRET_KEY=ITC
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/postgres



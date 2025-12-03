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
# Project API - Endpoints Documentation

## Base URL
All endpoints start with:

/api

## Auth (JWT)
Most endpoints are protected using JWT.
Send the token in headers for protected routes:

Authorization: Bearer <YOUR_JWT_TOKEN>

Content-Type: application/json (for POST/PUT requests with JSON body)

---

# 1) AUTH ROUTES

## Register
- Method: POST
- URL: /api/auth/register
- Auth: No

Purpose: Create a new user account.

Example body:
{
  "email": "user@example.com",
  "password": "StrongPassword123",
  "name": "John Doe"
}

Example response:
{
  "message": "User created successfully"
}

---

## Login
- Method: POST
- URL: /api/auth/login
- Auth: No

Purpose: Login and receive JWT token.

Example body:
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}

Example response:
{
  "access_token": "YOUR_JWT_TOKEN"
}

---

## Logout
- Method: POST
- URL: /api/auth/logout
- Auth: Yes (JWT required)

Purpose: Logout current user (depends on backend logic: blacklist token, etc.)

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

Example response:
{
  "message": "Logged out successfully"
}

---

# 2) EVENTS ROUTES (JWT REQUIRED)

## List Events
- Method: GET
- URL: /api/events
- Auth: Yes

Purpose: Get all events.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Get Event Details
- Method: GET
- URL: /api/events/<event_id>
- Auth: Yes

Purpose: Get one event details by ID.

Example:
GET /api/events/12

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

Important note:
In your code, the route returns `get_event_details` (function reference) instead of calling it.
It should likely be:
return get_event_details(event_id)

---

## Create Event
- Method: POST
- URL: /api/events/create
- Auth: Yes

Purpose: Create a new event.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "title": "Weekly Meeting",
  "date": "2025-12-05",
  "location": "Room A",
  "description": "Team weekly sync"
}

Responses:
- Success: returns JSON body + HTTP status code from backend
- Error: returns JSON body + HTTP status code from backend

---

## Update Event
- Method: PUT
- URL: /api/events/update/<event_id>
- Auth: Yes

Purpose: Update an event by ID.

Example:
PUT /api/events/update/12

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "title": "Updated title",
  "location": "Room B"
}

---

## Delete Event
- Method: DELETE
- URL: /api/events/delete/<event_id>
- Auth: Yes

Purpose: Delete an event by ID.

Example:
DELETE /api/events/delete/12

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

# 3) MEMBERS ROUTES (JWT REQUIRED)

## List Members
- Method: GET
- URL: /api/members
- Auth: Yes

Purpose: Get all members.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Get Member By ID
- Method: GET
- URL: /api/members/<member_id>
- Auth: Yes

Purpose: Get a member by ID.

Example:
GET /api/members/5

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Create Member
- Method: POST
- URL: /api/members
- Auth: Yes

Purpose: Create a new member.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "name": "Member Name",
  "email": "member@example.com",
  "phone": "123456789"
}

---

## Update Member
- Method: PUT
- URL: /api/members/<member_id>
- Auth: Yes

Purpose: Update a member by ID.

Example:
PUT /api/members/5

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "name": "New Name"
}

---

## Delete Member
- Method: DELETE
- URL: /api/members/<member_id>
- Auth: Yes

Purpose: Delete a member by ID.

Example:
DELETE /api/members/5

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## View Member Profile
- Method: GET
- URL: /api/members/<member_id>/profile
- Auth: Yes

Purpose: View profile details for a member.

Example:
GET /api/members/5/profile

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

# 4) CONTENT MANAGEMENT ROUTES (JWT REQUIRED)

## List Contents
- Method: GET
- URL: /api/list_contents
- Auth: Yes

Purpose: Get all contents.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

Response:
Returns rows (JSON array) with HTTP 200.

---

## Get Content By ID
- Method: GET
- URL: /api/contents_by_id/<content_id>
- Auth: Yes

Purpose: Get content by ID.

Example:
GET /api/contents_by_id/10

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Create Content
- Method: POST
- URL: /api/contents/create
- Auth: Yes

Purpose: Create new content.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "title": "Content title",
  "body": "Content body text"
}

---

## Update Content
- Method: PUT
- URL: /api/contents/update/<content_id>
- Auth: Yes

Purpose: Update content by ID.

Example:
PUT /api/contents/update/10

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "title": "Updated title"
}

---

## Delete Content
- Method: DELETE
- URL: /api/contents/delete/<content_id>
- Auth: Yes

Purpose: Delete content by ID.

Example:
DELETE /api/contents/delete/10

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

# 5) REPORTS ROUTES (JWT REQUIRED)

## List Reports
- Method: GET
- URL: /api/reports
- Auth: Yes

Purpose: Get all reports.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

Response:
Returns result (JSON) with HTTP 200.

---

## Get Report By ID
- Method: GET
- URL: /api/reports/byid/<report_id>
- Auth: Yes

Purpose: Get report by ID.

Example:
GET /api/reports/byid/7

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Create Report
- Method: POST
- URL: /api/reports/create
- Auth: Yes

Purpose: Create a report.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "title": "Monthly Report",
  "content": "Report details..."
}

---

## Update Report
- Method: PUT
- URL: /api/reports/update/<report_id>
- Auth: Yes

Purpose: Update report by ID.

Example:
PUT /api/reports/update/7

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "title": "Updated report title"
}

---

## Delete Report
- Method: DELETE
- URL: /api/reports/delete/<report_id>
- Auth: Yes

Purpose: Delete report by ID.

Example:
DELETE /api/reports/delete/7

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Submit Report
- Method: POST
- URL: /api/reports/<report_id>/submit
- Auth: Yes

Purpose: Submit a report (example: change status to submitted).

Example:
POST /api/reports/7/submit

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

# 6) TEAMS ROUTES (JWT REQUIRED)

## List Teams
- Method: GET
- URL: /api/teams
- Auth: Yes

Purpose: Get all teams.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Get Team By ID
- Method: GET
- URL: /api/teams/<team_id>
- Auth: Yes

Purpose: Get one team by ID.

Example:
GET /api/teams/3

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Create Team
- Method: POST
- URL: /api/teams
- Auth: Yes

Purpose: Create a new team.

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "name": "Data Team",
  "description": "Team description here"
}

---

## Update Team
- Method: PUT
- URL: /api/teams/<team_id>
- Auth: Yes

Purpose: Update a team by ID.

Example:
PUT /api/teams/3

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>
Content-Type: application/json

Example body:
{
  "name": "Updated Team Name"
}

---

## Delete Team
- Method: DELETE
- URL: /api/teams/<team_id>
- Auth: Yes

Purpose: Delete a team by ID.

Example:
DELETE /api/teams/3

Headers:
Authorization: Bearer <YOUR_JWT_TOKEN>

---

## Common HTTP Status Codes (typical)
- 200 OK: Request success
- 201 Created: Resource created
- 400 Bad Request: Missing/invalid data
- 401 Unauthorized: Missing or invalid token
- 403 Forbidden: No permission
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server error




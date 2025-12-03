# models.py
from extension import db



class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.BigInteger, primary_key=True)
    member_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)
    major = db.Column(db.String(100))
    birthday = db.Column(db.Date)
    last_active = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(255))
    status = db.Column(
        db.Enum(
            "active",
            "inactive",
            name="member_status_enum",
            create_type=False, 
        ),
        nullable=False,
    )
    teams = db.relationship(
        "Team",
        secondary="member_teams",
        back_populates="members",
    )
    events = db.relationship(
        "Event",
        secondary="members_events",
        back_populates="members",
    )
    reports = db.relationship("Report", back_populates="member")




class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.BigInteger, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    members = db.relationship(
        "Member",
        secondary="member_teams",
        back_populates="teams",
    )


class MemberTeam(db.Model):
    __tablename__ = "member_teams"

    member_id = db.Column(
        db.BigInteger,
        db.ForeignKey("member.id", ondelete="CASCADE"),
        primary_key=True,
    )
    team_id = db.Column(
        db.BigInteger,
        db.ForeignKey("team.id", ondelete="CASCADE"),
        primary_key=True,
    )

class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.BigInteger, primary_key=True)
    event_name = db.Column(db.String(150), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)

    members = db.relationship(
        "Member",
        secondary="members_events",
        back_populates="events",
    )


class MemberEvent(db.Model):
    __tablename__ = "members_events"

    member_id = db.Column(
        db.BigInteger,
        db.ForeignKey("member.id", ondelete="CASCADE"),
        primary_key=True,
    )
    event_id = db.Column(
        db.BigInteger,
        db.ForeignKey("event.id", ondelete="CASCADE"),
        primary_key=True,
    )


class Content(db.Model):
    __tablename__ = "content"

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    content_type = db.Column(
        db.Enum(
            "task",
            "quiz",
            "playlist",
            name="content_type_enum",
            create_type=False,
        ),
        nullable=False,
    )

    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)

    reports = db.relationship("Report", back_populates="content")


class Report(db.Model):
    __tablename__ = "report"

    id = db.Column(db.BigInteger, primary_key=True)

    content_id = db.Column(
        db.BigInteger,
        db.ForeignKey("content.id", ondelete="CASCADE"),
    )
    submitted_by = db.Column(
        db.BigInteger,
        db.ForeignKey("member.id", ondelete="CASCADE"),
    )

    title = db.Column(db.String(200), nullable=False)

    status = db.Column(
        db.Enum(
            "pending",
            "submitted",
            "late",
            "approved",
            "revision_requested",
            name="content_status_enum",
            create_type=False,
        ),
        nullable=False,
    )

    submission_date = db.Column(db.DateTime)
    file_path = db.Column(db.String(255))

    action = db.Column(
        db.Enum(
            "none",
            "send_reminder",
            "approve",
            "request_revision",
            name="content_action_enum",
            create_type=False,
        ),
        nullable=False,
    )

    content = db.relationship("Content", back_populates="reports")
    member = db.relationship("Member", back_populates="reports")

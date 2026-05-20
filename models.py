from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import hashlib
import os

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer,     primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    bugs_created  = db.relationship("Bug", foreign_keys="Bug.created_by",
                                    backref="creator",  lazy="dynamic")
    bugs_assigned = db.relationship("Bug", foreign_keys="Bug.assigned_to",
                                    backref="assignee", lazy="dynamic")
    comments      = db.relationship("Comment", backref="author", lazy="dynamic")

    def set_password(self, plain_text: str) -> None:
        salt               = os.urandom(16).hex()
        hashed             = hashlib.sha256(f"{salt}{plain_text}".encode()).hexdigest()
        self.password_hash = f"{salt}:{hashed}"

    def check_password(self, plain_text: str) -> bool:
        try:
            salt, hashed = self.password_hash.split(":", 1)
            candidate    = hashlib.sha256(f"{salt}{plain_text}".encode()).hexdigest()
            return candidate == hashed
        except ValueError:
            return False

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"


class Bug(db.Model):
    __tablename__ = "bugs"

    PRIORITIES = ["Low", "Medium", "High"]
    STATUSES   = ["Open", "In Progress", "Closed"]

    id          = db.Column(db.Integer,     primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=False)
    priority    = db.Column(db.String(20),  nullable=False, default="Medium")
    status      = db.Column(db.String(20),  nullable=False, default="Open")
    created_by  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    # One bug → many comments; deleting a bug cascades to its comments
    comments    = db.relationship("Comment", backref="bug",
                                  lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Bug id={self.id} title={self.title!r} status={self.status!r}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id         = db.Column(db.Integer, primary_key=True)
    content    = db.Column(db.Text,    nullable=False)
    author_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bug_id     = db.Column(db.Integer, db.ForeignKey("bugs.id"),   nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Comment id={self.id} bug_id={self.bug_id} author_id={self.author_id}>"
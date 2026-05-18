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

    # ── Password helpers ───────────────────────────────────────────────────────

    def set_password(self, plain_text: str) -> None:
        """Hash and store a plain-text password. Never stores the raw value."""
        salt             = os.urandom(16).hex()
        hashed           = hashlib.sha256(f"{salt}{plain_text}".encode()).hexdigest()
        self.password_hash = f"{salt}:{hashed}"

    def check_password(self, plain_text: str) -> bool:
        """Return True if plain_text matches the stored hash."""
        try:
            salt, hashed = self.password_hash.split(":", 1)
            candidate    = hashlib.sha256(f"{salt}{plain_text}".encode()).hexdigest()
            return candidate == hashed
        except ValueError:
            return False

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
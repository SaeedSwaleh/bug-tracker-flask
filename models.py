import hashlib
import os


class User:
    def __init__(self, id: int, username: str, email: str, password_hash: str):
        self.id            = id
        self.username      = username
        self.email         = email
        self.password_hash = password_hash

    # ── Password helpers ───────────────────────────────────────────────────────

    @staticmethod
    def hash_password(plain_text: str) -> str:
        """Hash a plain-text password with a random salt. Returns 'salt:hash'."""
        salt   = os.urandom(16).hex()
        hashed = hashlib.sha256(f"{salt}{plain_text}".encode()).hexdigest()
        return f"{salt}:{hashed}"

    def check_password(self, plain_text: str) -> bool:
        """Verify a plain-text password against the stored hash."""
        salt, hashed = self.password_hash.split(":", 1)
        candidate    = hashlib.sha256(f"{salt}{plain_text}".encode()).hexdigest()
        return candidate == hashed

    # ── Representation ─────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} email={self.email!r}>"
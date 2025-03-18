import hashlib

def hash_password(password: str) -> str:
    """Compute a SHA-256 hash for the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

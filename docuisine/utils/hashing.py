from hashlib import sha256


def hash_in_sha256(string: str) -> str:
    """Encrypt the given string using SHA-256."""
    return sha256(string.encode()).hexdigest()

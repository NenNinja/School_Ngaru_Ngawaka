import hashlib
import hmac
import secrets
import sqlite3
import os

HASH_ITERATIONS = 200_000

def get_connection(dbPath):
    global conn, cursor
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

def setup_db():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                salt          TEXT    NOT NULL,
                password_hash TEXT    NOT NULL
            )
        """)
    cursor.execute("PRAGMA table_info(users)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    if "pin_salt" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN pin_salt TEXT")
    if "pin_hash" not in existing_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN pin_hash TEXT")

def _hash_secret(secret: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        secret.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )
    return digest.hex()

def _new_salt() -> bytes:
    return secrets.token_bytes(16)

def register_user(username: str, password: str) -> bool:
    salt = _new_salt()
    password_hash = _hash_secret(password, salt)

    try:
        conn.execute(
            "INSERT INTO users (username, salt, password_hash) "
            "VALUES (?, ?, ?)",
            (username, salt.hex(), password_hash),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # UNIQUE constraint on username failed — that username exists already
        return False

def verify_login(username: str, password: str) -> dict | None:
    """
    Check a username/password pair.
    Returns a dict with the user's info if correct, or None if the
    username doesn't exist or the password is wrong.
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT username, salt, password_hash FROM users WHERE username=?",
        (username,),
    )
    row = cur.fetchone()

    if row is None:
        print("wrong username or password")
        return None

    stored_username, salt_hex, stored_hash = row
    salt = bytes.fromhex(salt_hex)
    attempt_hash = _hash_secret(password, salt)

    if hmac.compare_digest(attempt_hash, stored_hash):
        return {"username": stored_username}
    return None

def change_password(username: str, new_password: str) -> bool:
    """Update an existing user's password. Returns True if the user existed."""
    salt = _new_salt()
    password_hash = _hash_secret(new_password, salt)
    
    cur = conn.execute(
        "UPDATE users SET salt=?, password_hash=? WHERE username=?",
        (salt.hex(), password_hash, username),
    )
    conn.commit()
    return cur.rowcount > 0

def close_connection():
    conn.commit()
    conn.close()

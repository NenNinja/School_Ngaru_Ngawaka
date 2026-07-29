"""
auth.py
Login / authentication layer for the Ranui Family Clothing Allowance App.

Adds two login paths on top of database.py:

  1. Parent / guardian login: user+

  2. Child quick-login: pin

They are hashed with
PBKDF2-HMAC-SHA256 and a random per-user salt, using Python's built-in
hashlib — no extra dependency required.
"""

import sqlite3
import os
import hashlib
import hmac
import secrets

from database import get_connection, DB_PATH


# ── Hashing helpers ─────────────────────────────────────────
#
# We never store a password/PIN directly. Instead we store:
#   - a random salt (unique per user)
#   - the PBKDF2-HMAC-SHA256 hash of (salt + password)
#
# On login, we redo the same hash with the stored salt and compare the
# result using a constant-time comparison (hmac.compare_digest), so an
# attacker can't learn anything from how long the check takes.

HASH_ITERATIONS = 200_000  # deliberately slow, to resist brute-forcing


def _hash_secret(secret: str, salt: bytes) -> str:
    """Hash a password/PIN with the given salt. Returns a hex string."""
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        secret.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )
    return digest.hex()


def _new_salt() -> bytes:
    return secrets.token_bytes(16)


# ── Schema setup ────────────────────────────────────────────

def init_auth_db():
    """
    Create the users table (parent/guardian logins) if it doesn't exist,
    and add PIN columns to the children table if they're not already
    there. Safe to call every time the app starts.
    """
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                salt          TEXT    NOT NULL,
                password_hash TEXT    NOT NULL,
                role          TEXT    NOT NULL DEFAULT 'parent'
            )
        """)

        # SQLite has no "ADD COLUMN IF NOT EXISTS", so we check the
        # existing columns first via PRAGMA table_info before altering.
        cur.execute("PRAGMA table_info(children)")
        existing_cols = {row[1] for row in cur.fetchall()}

        if "pin_salt" not in existing_cols:
            cur.execute("ALTER TABLE children ADD COLUMN pin_salt TEXT")
        if "pin_hash" not in existing_cols:
            cur.execute("ALTER TABLE children ADD COLUMN pin_hash TEXT")

        conn.commit()


# ── Parent / guardian login ─────────────────────────────────

def register_user(username: str, password: str, role: str = "parent") -> bool:
    """
    Create a new parent/guardian login. Returns True on success,
    False if the username is already taken.
    """
    salt = _new_salt()
    password_hash = _hash_secret(password, salt)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, salt, password_hash, role) "
                "VALUES (?, ?, ?, ?)",
                (username, salt.hex(), password_hash, role),
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
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT username, salt, password_hash, role FROM users WHERE username=?",
            (username,),
        )
        row = cur.fetchone()

    if row is None:
        return None  # no such user — don't reveal that in the error message shown to the user

    stored_username, salt_hex, stored_hash, role = row
    salt = bytes.fromhex(salt_hex)
    attempt_hash = _hash_secret(password, salt)

    if hmac.compare_digest(attempt_hash, stored_hash):
        return {"username": stored_username, "role": role}
    return None


def change_password(username: str, new_password: str) -> bool:
    """Update an existing user's password. Returns True if the user existed."""
    salt = _new_salt()
    password_hash = _hash_secret(new_password, salt)

    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE users SET salt=?, password_hash=? WHERE username=?",
            (salt.hex(), password_hash, username),
        )
        conn.commit()
        return cur.rowcount > 0


# ── Child quick-login (PIN) ─────────────────────────────────

def set_child_pin(child_name: str, pin: str) -> bool:
    """
    Set (or reset) a child's login PIN. Returns True if the child exists.
    PIN should be a short numeric string, e.g. "4821" — but any string works.
    """
    salt = _new_salt()
    pin_hash = _hash_secret(pin, salt)

    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE children SET pin_salt=?, pin_hash=? WHERE name=?",
            (salt.hex(), pin_hash, child_name),
        )
        conn.commit()
        return cur.rowcount > 0


def verify_child_pin(child_name: str, pin: str) -> bool:
    """Check a child's PIN. Returns True if it matches."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT pin_salt, pin_hash FROM children WHERE name=?",
            (child_name,),
        )
        row = cur.fetchone()

    if row is None or row[0] is None or row[1] is None:
        return False  # no such child, or no PIN has been set yet

    salt_hex, stored_hash = row
    salt = bytes.fromhex(salt_hex)
    attempt_hash = _hash_secret(pin, salt)
    return hmac.compare_digest(attempt_hash, stored_hash)


# ── Demo / manual test ──────────────────────────────────────
#
# Running this file directly (python auth.py) sets up the database and
# walks through a login and PIN example, printing the results so you
# can see it actually working.

if __name__ == "__main__":
    from database import init_db

    print("Setting up database...")
    init_db()
    init_auth_db()

    print("\n--- Parent login ---")
    created = register_user("mum", "MyPassword123")
    print("register_user('mum', 'MyPassword123') ->", created)
    if not created:
        print("  (username 'mum' already exists from a previous run — that's fine)")

    print("verify_login('mum', 'MyPassword123')   ->", verify_login("mum", "MyPassword123"))
    print("verify_login('mum', 'wrongpassword')    ->", verify_login("mum", "wrongpassword"))

    print("\n--- Child PIN login ---")
    print("set_child_pin('Nikau', '4821')          ->", set_child_pin("Nikau", "4821"))
    print("verify_child_pin('Nikau', '4821')       ->", verify_child_pin("Nikau", "4821"))
    print("verify_child_pin('Nikau', '0000')       ->", verify_child_pin("Nikau", "0000"))

    print("\nDone. Run this file again — since 'mum' now already exists,")
    print("register_user() will correctly return False the second time.")
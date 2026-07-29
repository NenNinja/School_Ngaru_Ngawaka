"""
database.py
SQLite persistence layer for the Ranui Family Clothing Allowance App.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "ranui.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS children (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL UNIQUE,
                balance REAL    NOT NULL DEFAULT 300.00
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name  TEXT    NOT NULL,
                amount      REAL    NOT NULL,
                description TEXT,
                timestamp   TEXT    NOT NULL
            )
        """)

        # Seed children if table is empty
        cur.execute("SELECT COUNT(*) FROM children")
        if cur.fetchone()[0] == 0:
            for name in ["Nikau", "Hana", "Tia"]:
                cur.execute("INSERT INTO children (name, balance) VALUES (?, 300.00)", (name,))

        conn.commit()


# ── Children ────────────────────────────────────────────────

def load_children() -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, balance FROM children ORDER BY id")
        return [{"name": row[0], "balance": row[1]} for row in cur.fetchall()]


def save_balance(name: str, balance: float):
    with get_connection() as conn:
        conn.execute("UPDATE children SET balance=? WHERE name=?", (balance, name))
        conn.commit()


def reset_all_balances():
    with get_connection() as conn:
        conn.execute("UPDATE children SET balance=300.00")
        conn.commit()


# ── Transactions ────────────────────────────────────────────

def record_transaction(child_name: str, amount: float, description: str = ""):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO transactions (child_name, amount, description, timestamp) VALUES (?,?,?,?)",
            (child_name, amount, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()


def get_transactions(child_name: str = None) -> list[dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        if child_name:
            cur.execute(
                "SELECT child_name, amount, description, timestamp FROM transactions "
                "WHERE child_name=? ORDER BY timestamp DESC",
                (child_name,)
            )
        else:
            cur.execute(
                "SELECT child_name, amount, description, timestamp FROM transactions "
                "ORDER BY timestamp DESC"
            )
        cols = ["child_name", "amount", "description", "timestamp"]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def clear_transactions():
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions")
        conn.commit()

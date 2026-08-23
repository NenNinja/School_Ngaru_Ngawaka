from NENTkintLib import *
import hashlib
import hmac
import secrets
import sqlite3
import os

HASH_ITERATIONS = 200_000

class BlogDB:
    def __init__(self, dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()

    def setup_db(self):
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id            INTEGER PRIMARY KEY AUTOINCREMENT   ,
                        username      TEXT    NOT NULL UNIQUE             ,
                        salt          TEXT    NOT NULL                    ,
                        password_hash TEXT    NOT NULL                    ,
                        colors        TEXT
                    )
                """)
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS posts (
                        id            INTEGER PRIMARY   KEY AUTOINCREMENT ,
                        author_id     INTEGER NOT NULL                    ,
                        title         TEXT    NOT NULL  UNIQUE            ,
                        content       TEXT    NOT NULL                    ,
                        timestamp     DATETIME DEFAULT  CURRENT_TIMESTAMP ,
                        FOREIGN KEY  (author_id) REFERENCES users(id)
                        ON DELETE CASCADE
                    )
                """)

    def new_post(self, username, title, content):
        """Create a new blog post."""
        author_id = self.cursor.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if not author_id:
            raise ValueError("User not found")
        self.cursor.execute(
            "INSERT INTO posts (author_id, title, content) VALUES (?, ?, ?)",
            (author_id[0], title, content)
        )
        self.conn.commit() 

    def get_post(self, title):
        """Retrieve a specific post by its title."""
        self.cursor.execute(
            "SELECT u.username, p.title, p.content, p.timestamp FROM posts p JOIN users u ON p.author_id = u.id WHERE p.title=?",
            (title,)
        )
        return self.cursor.fetchone()

    def get_posts(self, username):
        """Retrieve all posts by a specific user."""
        author_id = self.cursor.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if not author_id:
            raise ValueError("User not found")
        self.cursor.execute(
            "SELECT title, content, timestamp FROM posts WHERE author_id=? ORDER BY timestamp DESC",
            (author_id[0],)
        )
        return self.cursor.fetchall()

    def get_all_posts(self):
        """Retrieve all posts from all users."""
        self.cursor.execute(
            "SELECT u.username, p.title, p.content, p.timestamp FROM posts p JOIN users u ON p.author_id = u.id ORDER BY p.timestamp DESC"
        )
        return self.cursor.fetchall()

    def delete_post(self, username, title):
        """Delete a specific post by its title."""
        author_id = self.cursor.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if not author_id:
            raise ValueError("User not found")
        self.cursor.execute("DELETE FROM posts WHERE author_id=? AND title=?", (author_id[0], title))
        self.conn.commit()

    def edit_post(self, username, old_title, new_title, new_content):
        """Edit a specific post by its title."""
        author_id = self.cursor.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if not author_id:
            raise ValueError("User not found")
        self.cursor.execute(
            "UPDATE posts SET title=?, content=? WHERE author_id=? AND title=?",
            (new_title, new_content, author_id[0], old_title)
        )
        self.conn.commit()

    def close_connection(self):
        self.conn.commit()
        self.conn.close()


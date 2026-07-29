import os
import sqlite3

DB_PATH = "testing.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
"""
Database Management Module (RECOM.ai)
SQLite3-backed persistence for user authentication, bookmarks, and interaction feedback.
"""

import sqlite3
import hashlib
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portal_database.db")


def init_db():
    """Initializes tables for users, bookmarks, and rating feedback if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Saved Items (Bookmarks) Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            item_id INTEGER NOT NULL,
            item_title TEXT NOT NULL,
            extra_info TEXT,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, category, item_id)
        )
    """)

    # User Feedback Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            item_id INTEGER NOT NULL,
            feedback_type TEXT NOT NULL, -- 'like', 'dislike', 'star'
            rating_value REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def _hash_password(password: str, salt: str = "recom_ai_salt_v1") -> str:
    """Hashes a password with SHA-256 and salt for secure storage."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def register_user(username: str, password: str):
    """
    Registers a new user account.
    Returns: (user_id, message) or (None, error_message)
    """
    init_db()
    clean_user = username.strip()
    if not clean_user or not password:
        return None, "Username and password cannot be empty."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (clean_user, _hash_password(password))
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id, f"Welcome to RECOM.ai, {clean_user}!"
    except sqlite3.IntegrityError:
        conn.close()
        return None, "Username already exists. Please choose a different username."


def login_user(username: str, password: str):
    """
    Verifies user credentials.
    Returns: (user_id, message) or (None, error_message)
    """
    init_db()
    clean_user = username.strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (clean_user,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash = row[1]
        salted_hash = _hash_password(password)
        legacy_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if stored_hash in (salted_hash, legacy_hash):
            return row[0], f"Welcome back, {clean_user}!"
    return None, "Invalid username or password. Please try again."


def save_bookmark(user_id: int, category: str, item_id: int, item_title: str, extra_info: dict = None):
    """
    Saves an item to the user's bookmarks.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    extra_str = json.dumps(extra_info) if extra_info else ""
    try:
        cursor.execute(
            """
            INSERT OR REPLACE INTO saved_items (user_id, category, item_id, item_title, extra_info)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, category, item_id, item_title, extra_str)
        )
        conn.commit()
        conn.close()
        return True, f"Saved '{item_title}' to your bookmarks!"
    except Exception as e:
        conn.close()
        return False, f"Could not save item: {str(e)}"


def remove_bookmark(user_id: int, category: str, item_id: int):
    """Removes an item from the user's bookmarks."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM saved_items WHERE user_id = ? AND LOWER(category) = LOWER(?) AND item_id = ?",
        (user_id, category, item_id)
    )
    conn.commit()
    conn.close()
    return True, "Item removed from bookmarks."


def get_bookmarks(user_id: int):
    """Retrieves all bookmarked items for a user."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, category, item_id, item_title, extra_info, saved_at
        FROM saved_items
        WHERE user_id = ?
        ORDER BY saved_at DESC
        """,
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    bookmarks = []
    seen = set()
    for row_id, cat, i_id, title, extra_raw, s_at in rows:
        dedup_key = (cat.strip().lower(), i_id)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        parsed_extra = {}
        if extra_raw:
            try:
                parsed_extra = json.loads(extra_raw)
            except Exception:
                parsed_extra = {}
        bookmarks.append({
            "id": row_id,
            "category": cat,
            "item_id": i_id,
            "title": title,
            "extra_info": parsed_extra,
            "saved_at": s_at
        })
    return bookmarks


def save_feedback(user_id: int, category: str, item_id: int, feedback_type: str, rating_val: float = None):
    """Records user interaction feedback ('like', 'dislike', 'star')."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_feedback (user_id, category, item_id, feedback_type, rating_value)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, category, item_id, feedback_type, rating_val)
    )
    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", os.path.abspath(DB_PATH))
    # Test registration and login
    uid, msg = register_user("testuser", "securepass123")
    print(f"Register: {msg} (ID: {uid})")
    uid_login, msg_login = login_user("testuser", "securepass123")
    print(f"Login: {msg_login} (ID: {uid_login})")

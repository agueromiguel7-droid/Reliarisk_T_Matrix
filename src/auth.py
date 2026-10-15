import sqlite3
import hashlib
import secrets
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users.db")

def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Generates PBKDF2 HMAC SHA-256 hash with a cryptographically secure salt."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return hashed, salt

def _get_connection():
    return sqlite3.connect(DB_PATH)

def init_auth_db():
    """Initializes the SQLite users table and ensures default admin exists."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER NOT NULL DEFAULT 1
        )
    """)
    conn.commit()

    # Verify if admin exists
    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    admin_row = cursor.fetchone()
    if not admin_row:
        # Default credentials requested by user
        default_admin_pass = "Coromoto_22"
        pwd_hash, salt = _hash_password(default_admin_pass)
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt, name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            ("admin", pwd_hash, salt, "Administrador del Sistema", "admin", 1)
        )
        conn.commit()
    conn.close()

def authenticate(username: str, password: str):
    """
    Authenticates a user by username and password.
    Returns user dict if valid and active, else None.
    """
    if not username or not password:
        return None

    username = username.strip().lower()
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, password_hash, salt, name, role, is_active FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    uname, stored_hash, salt, name, role, is_active = row
    if not is_active:
        return None

    calc_hash, _ = _hash_password(password, salt)
    if calc_hash == stored_hash:
        return {
            "username": uname,
            "name": name,
            "role": role
        }
    return None

def create_user(username: str, password: str, name: str, role: str = "user") -> tuple[bool, str]:
    """
    Creates a new user with hashed password.
    """
    username = username.strip().lower()
    name = name.strip()
    
    if not username or len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."
    if not password or len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    if not name:
        return False, "El nombre no puede estar vacío."
    if role not in ["admin", "user"]:
        role = "user"

    pwd_hash, salt = _hash_password(password)

    conn = _get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, salt, name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, pwd_hash, salt, name, role, 1)
        )
        conn.commit()
        return True, f"Usuario '{username}' creado exitosamente."
    except sqlite3.IntegrityError:
        return False, f"El usuario '{username}' ya existe."
    except Exception as e:
        return False, f"Error al crear usuario: {str(e)}"
    finally:
        conn.close()

def list_users() -> list[dict]:
    """Returns list of all registered users without exposing password hashes."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, name, role, created_at, is_active
        FROM users
        ORDER BY role DESC, username ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    users = []
    for r in rows:
        users.append({
            "id": r[0],
            "username": r[1],
            "name": r[2],
            "role": r[3],
            "created_at": r[4],
            "is_active": bool(r[5])
        })
    return users

def delete_user(username: str) -> tuple[bool, str]:
    """Deletes a user. The default 'admin' cannot be deleted."""
    username = username.strip().lower()
    if username == "admin":
        return False, "No se puede eliminar al usuario administrador principal ('admin')."

    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if not cursor.fetchone():
        conn.close()
        return False, f"El usuario '{username}' no existe."

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    return True, f"Usuario '{username}' eliminado correctamente."

def update_password(username: str, new_password: str) -> tuple[bool, str]:
    """Updates password for a specific user."""
    username = username.strip().lower()
    if not new_password or len(new_password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."

    pwd_hash, salt = _hash_password(new_password)
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ?, salt = ? WHERE username = ?", (pwd_hash, salt, username))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected > 0:
        return True, "Contraseña actualizada correctamente."
    return False, "No se encontró el usuario especificado."

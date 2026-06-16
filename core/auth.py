import bcrypt
from core.database import get_connection
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
def register_user(email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "message": "Email is already registerd"}
    hashed = hash_password(password)
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Account created successfully"}
def login_user(email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return {"success": False, "message": "Email does not exist"}
    if not verify_password(password, user["password"]):
        return {"success": False, "message": "Incorrect password"}
    return {
        "success": True,
        "message": "Logged in successfully",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "plan": user["plan"],
            "credits": user["credits"]
        }
    }
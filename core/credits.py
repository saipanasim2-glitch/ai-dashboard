from core.database import get_connection
PLAN_LIMITS = {
    "free": 3,
    "pro": 100
 }
def get_user_credits(user_id: int) -> int:
    conn = get_connection()
    row = conn.execute(
        "SELECT credits FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row["credits"] if row else 0
def consume_credit(user_id: int) -> dict:
    credits = get_user_credits(user_id)
    if credits <= 0:
        return {
            "success": False,
            "message": "Out of credits! Please upgrade to get more."
        }
    conn = get_connection()
    conn.execute(
        "UPDATE users SET credits = credits - 1 WHERE id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()
    return {"success": True, "remaining": credits - 1}
def reset_credits(user_id: int, plan: str):
    limit = PLAN_LIMITS.get(plan, 3)
    conn = get_connection()
    conn.execute("UPDATE users SET credits = ? WHERE id = ?", (limit, user_id))
    conn.commit()
    conn.close()
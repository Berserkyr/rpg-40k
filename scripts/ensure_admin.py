from backend.auth import hash_password
from backend.database import connect, get_account, init_db

init_db()
conn = connect()
existing = get_account("admin")
pw = hash_password("admin123")
if existing:
    conn.execute("UPDATE users SET role = 'admin', password_hash = ? WHERE id = 'admin'", (pw,))
else:
    conn.execute(
        "INSERT INTO users (id, display_name, password_hash, role, created_at, last_seen_at) "
        "VALUES ('admin', 'admin', ?, 'admin', datetime('now'), datetime('now'))",
        (pw,),
    )
conn.commit()
conn.close()
print("VPS admin role:", get_account("admin")["role"])

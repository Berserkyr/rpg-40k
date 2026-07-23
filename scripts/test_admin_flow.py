import json
import urllib.request

# Login
login_data = json.dumps({"username": "admin", "password": "admin123"}).encode()
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/auth/login",
    data=login_data,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
print("Login role:", data["user"]["role"])
token = data["access_token"]

# Test /api/models/generate authorization (dry check: expect 200 or non-403)
gen_data = json.dumps({
    "model_types": ["weapon"],
    "faction": "Imperial",
    "count": 1,
    "complexity": "simple",
}).encode()
req2 = urllib.request.Request(
    "http://127.0.0.1:8000/api/models/generate",
    data=gen_data,
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    method="POST",
)
try:
    with urllib.request.urlopen(req2, timeout=120) as resp:
        result = json.loads(resp.read())
    print("Generate OK:", result.get("message"))
except urllib.error.HTTPError as e:
    print("Generate HTTP", e.code, e.read().decode()[:200])

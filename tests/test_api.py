import random

from fastapi.testclient import TestClient

import backend.api as api


def _auth_headers(client, username=None, password="secret42"):
    """Crée un compte et retourne les en-têtes Authorization Bearer."""
    name = username or f"tester{random.randint(1000, 9999)}"
    resp = client.post("/api/auth/register", json={"username": name, "password": password})
    if resp.status_code == 409:
        resp = client.post("/api/auth/login", json={"username": name, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, resp.json()["user"]["id"]


def _client_with_temp_save(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "SAVE_DIR", tmp_path)
    api._session = None
    api._sessions.clear()
    return TestClient(api.app)


def test_health_endpoint():
    client = TestClient(api.app)
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "survivant-de-ruche-api"
    assert "database" in data


def test_state_requires_authentication():
    client = TestClient(api.app)
    response = client.get("/api/state")
    assert response.status_code == 401


def test_register_and_login_flow():
    client = TestClient(api.app)
    name = f"flow{random.randint(1000, 9999)}"

    reg = client.post("/api/auth/register", json={"username": name, "password": "secret42"})
    assert reg.status_code == 201
    assert reg.json()["user"]["role"] == "player"
    assert reg.json()["access_token"]

    dup = client.post("/api/auth/register", json={"username": name, "password": "secret42"})
    assert dup.status_code == 409

    bad = client.post("/api/auth/login", json={"username": name, "password": "wrong"})
    assert bad.status_code == 401

    ok = client.post("/api/auth/login", json={"username": name, "password": "secret42"})
    assert ok.status_code == 200
    assert ok.json()["access_token"]


def test_invalid_token_is_rejected():
    client = TestClient(api.app)
    response = client.get("/api/state", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401


def test_admin_route_forbidden_for_player(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    headers, _ = _auth_headers(client)
    response = client.get("/api/users", headers=headers)
    assert response.status_code == 403


def test_state_endpoint_returns_character(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    headers, user_id = _auth_headers(client)
    response = client.get("/api/state", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["character"]["name"] == "Karimus"
    assert data["user"]["id"] == user_id
    assert "current_zone" in data
    assert "inventory" in data


def test_state_endpoint_isolates_users(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    headers_a, id_a = _auth_headers(client)
    headers_b, id_b = _auth_headers(client)

    alpha = client.get("/api/state", headers=headers_a).json()
    beta = client.get("/api/state", headers=headers_b).json()

    assert alpha["user"]["id"] == id_a
    assert beta["user"]["id"] == id_b
    assert alpha["user"]["id"] != beta["user"]["id"]


def test_roll_endpoint_returns_2d6_total(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    headers, _ = _auth_headers(client)
    response = client.post("/api/roll", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert 2 <= data["total"] <= 12
    assert len(data["values"]) == 2


def test_loot_endpoint_updates_state(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    headers, _ = _auth_headers(client)
    response = client.post("/api/loot", json={"command": "loot", "args": ["standard"]}, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "inventory" in data
    assert "state" in data


def test_combat_start_endpoint_creates_active_combat(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    headers, _ = _auth_headers(client)
    response = client.post("/api/combat/start", json={"faction": "tyranide", "level": "standard"}, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["combat"]["active"] is True
    assert data["state"]["combat"]["active"] is True


def test_password_is_hashed_not_stored_in_clear(tmp_path, monkeypatch):
    from backend.database import get_account

    client = _client_with_temp_save(tmp_path, monkeypatch)
    name = f"hash{random.randint(1000, 9999)}"
    client.post("/api/auth/register", json={"username": name, "password": "secret42"})

    account = get_account(name)
    assert account["password_hash"]
    assert account["password_hash"] != "secret42"
    assert account["password_hash"].startswith("$2")

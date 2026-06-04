from fastapi.testclient import TestClient

import backend.api as api


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


def test_create_user_endpoint_registers_player():
    client = TestClient(api.app)
    response = client.post("/api/users", json={"user_id": "Joueur Test", "display_name": "Joueur Test"})

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["id"] == "joueur-test"
    assert data["user"]["display_name"] == "Joueur Test"


def test_state_endpoint_returns_character(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    response = client.get("/api/state")

    assert response.status_code == 200
    data = response.json()
    assert data["character"]["name"] == "Karimus"
    assert data["user"]["id"] == "default"
    assert "current_zone" in data
    assert "inventory" in data


def test_state_endpoint_isolates_users(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)

    alpha = client.get("/api/state", headers={"X-User-Id": "Alpha"}).json()
    beta = client.get("/api/state", headers={"X-User-Id": "Beta"}).json()

    assert alpha["user"]["id"] == "alpha"
    assert beta["user"]["id"] == "beta"
    assert alpha["user"]["id"] != beta["user"]["id"]


def test_roll_endpoint_returns_2d6_total():
    client = TestClient(api.app)
    response = client.post("/api/roll")

    assert response.status_code == 200
    data = response.json()
    assert 2 <= data["total"] <= 12
    assert len(data["values"]) == 2


def test_loot_endpoint_updates_state(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    response = client.post("/api/loot", json={"command": "loot", "args": ["standard"]})

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "inventory" in data
    assert "state" in data


def test_combat_start_endpoint_creates_active_combat(tmp_path, monkeypatch):
    client = _client_with_temp_save(tmp_path, monkeypatch)
    response = client.post("/api/combat/start", json={"faction": "tyranide", "level": "standard"})

    assert response.status_code == 200
    data = response.json()
    assert data["combat"]["active"] is True
    assert data["state"]["combat"]["active"] is True

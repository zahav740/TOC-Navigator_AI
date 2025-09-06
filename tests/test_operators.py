def test_create_operator(client):
    response = client.post("/operators/", json={"name": "Alice"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data


def test_read_operators_returns_all(client):
    client.post("/operators/", json={"name": "Alice"})
    client.post("/operators/", json={"name": "Bob"})

    response = client.get("/operators/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {op["name"] for op in data} == {"Alice", "Bob"}


def test_read_operator_by_id(client):
    created = client.post("/operators/", json={"name": "Alice"}).json()
    operator_id = created["id"]

    response = client.get(f"/operators/{operator_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == operator_id
    assert data["name"] == "Alice"


def test_update_operator(client):
    created = client.post("/operators/", json={"name": "Alice"}).json()
    operator_id = created["id"]

    response = client.put(f"/operators/{operator_id}", json={"name": "Bob"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bob"


def test_delete_operator(client):
    created = client.post("/operators/", json={"name": "Alice"}).json()
    operator_id = created["id"]

    response = client.delete(f"/operators/{operator_id}")
    assert response.status_code == 204

    response = client.get(f"/operators/{operator_id}")
    assert response.status_code == 404

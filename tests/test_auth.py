def test_register(client):
    response = client.post("/auth/register", json={
        "email": "new@example.com",
        "username": "newuser",
        "password": "password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["role"] == "client"


def test_register_duplicate_email(client, registered_user):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "different",
        "password": "password123",
    })
    assert response.status_code == 400


def test_login(client, registered_user):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, registered_user):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpass",
    })
    assert response.status_code == 401


def test_get_me(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_unauthorized_access(client):
    response = client.get("/auth/me")
    assert response.status_code == 403

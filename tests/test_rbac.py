def test_admin_can_list_users(client, admin_headers):
    response = client.get("/auth/users", headers=admin_headers)
    assert response.status_code == 200


def test_client_cannot_list_users(client, auth_headers):
    response = client.get("/auth/users", headers=auth_headers)
    assert response.status_code == 403


def test_admin_can_update_role(client, admin_headers, registered_user):
    user_id = registered_user["id"]
    response = client.put(
        f"/auth/users/{user_id}/role",
        json={"role": "analyst"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["role"] == "analyst"


def test_client_cannot_delete_document(client, auth_headers):
    response = client.delete("/documents/999", headers=auth_headers)
    assert response.status_code == 403

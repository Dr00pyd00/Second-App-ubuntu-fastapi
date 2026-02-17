
from app.tests.conftest import client
from fastapi.testclient import TestClient

# ===============================
# USER CREATION =================
# ===============================

# Create User SUCCESS ========================================================================
def test_create_user_success(client: TestClient):
    """Create user for test"""

    # 1. Prepare datas:
    user_data = {
        "username":"testuser",
        "password":"test123"
    }

    # 2.  on exectute la requete:
    response = client.post("/users/", json=user_data)

    # 3. on verifie si ca colle:
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data
    # ne pas voir le password en sortie:
    assert "password" not in data

# Create User Username TOO SHORT =====================================================
def test_create_user_username_too_short(client: TestClient):

    user_data = {
        "username":"a",
        "password":"password123"
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 422  # Unprocessable Entity generer par le validator Pydantic.
    # print(response.text)
    assert "string_too_short" in response.text.lower()

# Create User Username prohibed chars ===================================================
def test_create_user_username_unauthorized_chars(client: TestClient):

    user_data = {
        "username":"test@user",
        "password":"password123"
    }

    response = client.post("/users", json=user_data)

    # print(response.text)

    assert response.status_code == 422  # Unprocessable Entity generer par le validator Pydantic.
    assert "value error" in response.text.lower()
    assert "must be alphanumeric" in response.text.lower()
    

# Create User Password not alphanumeric ==================================================
def test_create_user_password_not_alphanumeric(client: TestClient):

    user_data = {
        "username":"abcd",
        "password":"123644"
    }

    response = client.post("/users", json=user_data)
    
    assert response.status_code == 422  # Unprocessable Entity generer par le validator Pydantic.
    # print(response.text) 
    assert "value error" in response.text.lower()
    assert "must have at least one alphabetic" in response.text.lower()


# Create User Password too short ==========================================================
def test_create_user_password_too_short(client: TestClient):

    user_data = {
        "username":"abcd",
        "password":"a"
    }

    response = client.post("/users", json=user_data)

    # print(response.text) 
    
    assert response.status_code == 422  # Unprocessable Entity generer par le validator Pydantic.
    assert "string_too_short" in response.text.lower()
    assert "at least 5 characters" in response.text.lower()



# ===============================
# GET USER =================
# ===============================

# Get user by id SUCCESS: ( RIEN a voir avec get_user_bvy_id_or_404 que j'ai créé)
def test_get_user_by_id_success(client: TestClient):

    user_data = {
        "username":"usertest",
        "password":"password123"
    }

    user_creation_response = client.post("/users", json=user_data)
    # verifie que le User a bien été creer
    assert user_creation_response.status_code == 201
    # recupere l'id pour aller le chercher:
    user_id = user_creation_response.json()["id"]
    print(f"id de l'user: { user_id}")

    # maintenant verifier si on peut le retrouver:
    response = client.get(f"/users/{user_id}")
    data = response.json()

    assert response.status_code == 200 
    # print(data)
    assert "created_at" in data
    assert "username" in data



# Get user by id FAILED : unknown id:
 
def test_get_user_by_id_failed(client: TestClient):

    user_data = {
        "username":"usertest",
        "password":"password123"
    }

    user_creation_response = client.post("/users", json=user_data)
    # verifie que le User a bien été creer
    assert user_creation_response.status_code == 201
    # recupere l'id pour aller le chercher:
    user_id = user_creation_response.json()["id"]
    print(f"id de l'user: { user_id}")

    # maintenant verifier si on peut le retrouver:
    response = client.get(f"/users/999999999")
    data = response.json()

    assert response.status_code == 404 
    # print(data)
    assert "not found" in response.text.lower()





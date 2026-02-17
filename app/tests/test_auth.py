from fastapi.testclient import TestClient

from app.tests.conftest import client



# ===================
# ==== LOGIN ========
# ===================

# Login SUCCESS ===============================================
def test_login_sucess(client: TestClient):

    # creer un user:
    user_data = {
        "username":"testusername",
        "password":"password123" 
        }

    user_creation_response = client.post("/users", json=user_data)
    assert user_creation_response.status_code == 201  # assure que le user est bien créér

    # je me login avec les data de l'user present en db test:
    login_response = client.post("/login", data=user_data)     # ATTENTION IL FAUT METTRE DATA et pas json ...
    # print(login_response.text)

    assert login_response.status_code == 200

    # verifier si j'ai bien le token:
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# Login Wrong Password ===========================================================
def test_login_wrong_password(client: TestClient):

    # creer un user:
    user_data = {
        "username":"testusername",
        "password":"password123" 
        }

    user_creation_response = client.post("/users", json=user_data)
    assert user_creation_response.status_code == 201  # assure que le user est bien créér

    wrong_pw_user_data = {
        "username":"testusername",
        "password":"Password123" 
        }


    # je me login avec un MAUVAIS password:
    login_response = client.post("/login", data=wrong_pw_user_data)     # ATTENTION IL FAUT METTRE DATA et pas json ...
    # print(login_response.text)

    assert login_response.status_code == 401
    assert "invalid credentials" in login_response.text.lower()


# Login Wrong Username =====================================================
def test_login_wrong_username(client: TestClient):

    # creer un user:
    user_data = {
        "username":"testusername",
        "password":"password123" 
        }

    user_creation_response = client.post("/users", json=user_data)
    assert user_creation_response.status_code == 201  # assure que le user est bien créér

    wrong_usename_user_data = {
        "username":"testusername2",
        "password":"password123" 
        }

    # je me login avec un MAUVAIS username:
    login_response = client.post("/login", data=wrong_usename_user_data)     # ATTENTION IL FAUT METTRE DATA et pas json CAR: c'est pas un pydantic c'est Oauth2PasswordRequestForm!
    # print(login_response.text)
    assert login_response.status_code == 401
    assert "invalid credentials" in login_response.text.lower()


# =======================
# ==== Protected Route ==
# =======================

# ici je teste si la route /me sans etre login fonctionne par exemple

# Get /me SUCCESS:
def test_get_me_success(client: TestClient):
    # creation d'un user:
    user_data = {
        "username":"testuser",
        "password":"password123"
    }
    user_creation_response = client.post("/users", json=user_data)
    assert user_creation_response.status_code == 201

    # il me faut le token via login:
    login_response = client.post("/login", data=user_data)
    assert login_response.status_code == 200
    print(f"le token est: {login_response.json()["access_token"]}")

    # maintent je dois /me avec un token coherent car j'ai get_user dans le path:
    me_response = client.get(
        "/users/me",
        headers= {"Authorization":f"Bearer {login_response.json()["access_token"]}"}
          )
    
    assert me_response.status_code == 200
    data = me_response.json()
    assert "username" in data
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "created_at" in data


# Get /me FAILED (no token):
def test_get_me_without_token(client: TestClient):

    me_response = client.get("users/me")
    print(me_response.text)
    assert me_response.status_code == 401


   


                              

                                    
    
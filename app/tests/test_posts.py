from fastapi.testclient import TestClient

from app.tests.conftest import client



# =================
# CREATION
# =================

# Create Post with token: SUCCESS ===========================
def test_create_post_with_token(client:TestClient):
    # d'abord il me faut un user
    user_creation_response = client.post(
        url="/users/",
        json={
            "username":"testuser",
            "password":"password123"
        }
    )

    assert user_creation_response.status_code == 201
    assert user_creation_response.json()["username"] == "testuser"

    # maintenant je dois login et avoir un token:
    login_response = client.post(
        url="/login/",
        data={
            "username":"testuser",
            "password":"password123"
        }
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert "bearer" in login_response.json()["token_type"]
    assert len(login_response.json()["access_token"]) > 20   # le token doit avoir au moins 20 char

    # maintenant je creer un post avec un token dans le header:
    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }

    post_create_response = client.post(
        url="/posts/",
        headers={"Authorization":f"Bearer {login_response.json()["access_token"]}"},
        json=post_data
    )

    # print(post_create_response.text)

    assert post_create_response.status_code == 201


# Create Post without token: FAILED =================================
def test_create_post_without_token(client:TestClient):

    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }

    # creation d'un post sans etre login: donc pas de token en header
    create_reponse = client.post(
        url="/posts/",
        json=post_data)

    assert create_reponse.status_code == 401
    assert "not authenticated" in create_reponse.text.lower()



# =================
# DELETE
# =================

# Delete Post when not exist:
def test_delete_not_existing_post(client:TestClient):
    # creation d'un user:
    user_creation_response = client.post(
        url="/users/",
        json={
            "username":"testuser",
            "password":"password123"
        }
    )
    
    # maintenant je dois login et avoir un token:
    login_response = client.post(
        url="/login/",
        data={
            "username":"testuser",
            "password":"password123"
        }
    )

    # maintenant je creer un post avec un token dans le header:
    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }

    post_create_response = client.post(
        url="/posts/",
        headers={"Authorization":f"Bearer {login_response.json()["access_token"]}"},
        json=post_data
    )

    # maitenant je delete un post qui n'est pas celui que j'ai creer :
    post_test_id = 43
    assert post_test_id != post_create_response.json()["id"]
    # print(f"post_test_id = {post_test_id} \n real_post_id = {post_create_response.json()["id"]}")
    delete_response = client.delete(
        url=f"/posts/{post_test_id}",
        headers={"Authorization":f"Bearer {login_response.json()["access_token"]}"}
    )

    assert delete_response.status_code == 404
    assert "not found" in delete_response.text.lower()



# Delete Post when exist:
def test_delete_existing_post(client:TestClient):
    # creation d'un user:
    user_creation_response = client.post(
        url="/users/",
        json={
            "username":"testuser",
            "password":"password123"
        }
    )
    
    # maintenant je dois login et avoir un token:
    login_response = client.post(
        url="/login/",
        data={
            "username":"testuser",
            "password":"password123"
        }
    )

    # maintenant je creer un post avec un token dans le header:
    post_data = {
        "title":"testtitle",
        "content":"testcontent"
    }

    post_create_response = client.post(
        url="/posts/",
        headers={"Authorization":f"Bearer {login_response.json()["access_token"]}"},
        json=post_data
    )

    # maitenant je delete un post qui n'est pas celui que j'ai creer :
    post_test_id = post_create_response.json()["id"]

    delete_response = client.delete(
        url=f"/posts/{post_test_id}",
        headers={"Authorization":f"Bearer {login_response.json()["access_token"]}"}
    )

    assert delete_response.status_code == 204

    # essayer de le chercher:
    try_find_post_response = client.get(
        url=f"/posts/{post_test_id}"
    )
    print(try_find_post_response.text)
    assert try_find_post_response.status_code == 404
    assert "not found" in try_find_post_response.text.lower()

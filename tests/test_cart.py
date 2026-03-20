def test_add_item_to_cart(client):
    product = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Desc",
        "price": 29.99,
    })
    product_id = product.json()["data"]["id"]

    response = client.post("/cart/1/items", json={"productId": product_id})
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["productId"] == product_id
    assert data["title"] == "Remera"
    assert data["unitPrice"] == 29.99
    assert "addedAt" in data


def test_add_item_product_not_found(client):
    response = client.post("/cart/1/items", json={"productId": 999})
    assert response.status_code == 404


def test_get_cart(client):
    product = client.post("/products", json={
        "sellerId": 1,
        "title": "Producto A",
        "description": "Desc",
        "price": 10.00,
    })
    product_id = product.json()["data"]["id"]

    client.post("/cart/1/items", json={"productId": product_id})
    client.post("/cart/1/items", json={"productId": product_id})

    response = client.get("/cart/1")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["userId"] == 1
    assert len(data["items"]) == 2
    assert data["totalPrice"] == 20.00


def test_get_cart_empty(client):
    response = client.get("/cart/999")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == []
    assert data["totalPrice"] == 0

def test_delete_cart_item(client):
    product = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Desc",
        "price": 10.00,
    })
    product_id = product.json()["data"]["id"]

    item = client.post("/cart/1/items", json={"productId": product_id})
    item_id = item.json()["data"]["id"]

    response = client.delete(f"/cart/1/items/{item_id}")
    assert response.status_code == 204

    cart = client.get("/cart/1")
    assert len(cart.json()["data"]["items"]) == 0


def test_delete_cart_item_not_found(client):
    response = client.delete("/cart/1/items/999")
    assert response.status_code == 404


def test_delete_cart_item_wrong_user(client):
    product = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Desc",
        "price": 10.00,
    })
    product_id = product.json()["data"]["id"]

    item = client.post("/cart/1/items", json={"productId": product_id})
    item_id = item.json()["data"]["id"]

    response = client.delete(f"/cart/2/items/{item_id}")
    assert response.status_code == 404


def test_delete_product_removes_cart_items(client):
    product = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Desc",
        "price": 10.00,
    })
    product_id = product.json()["data"]["id"]

    client.post("/cart/1/items", json={"productId": product_id})
    client.post("/cart/2/items", json={"productId": product_id})

    client.delete(f"/products/{product_id}")

    cart1 = client.get("/cart/1")
    assert len(cart1.json()["data"]["items"]) == 0
    cart2 = client.get("/cart/2")
    assert len(cart2.json()["data"]["items"]) == 0

def test_wipe_cart(client):
    product = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Desc",
        "price": 10.00,
    })
    product_id = product.json()["data"]["id"]

    client.post("/cart/1/items", json={"productId": product_id})
    client.post("/cart/1/items", json={"productId": product_id})

    response = client.delete("/cart/1")
    assert response.status_code == 204

    cart = client.get("/cart/1")
    assert len(cart.json()["data"]["items"]) == 0
    assert cart.json()["data"]["totalPrice"] == 0


def test_wipe_cart_empty(client):
    response = client.delete("/cart/999")
    assert response.status_code == 204
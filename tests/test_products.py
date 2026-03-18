def test_create_product(client):
    response = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Remera negra talle L",
        "price": 29.99,
    })
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["title"] == "Remera"
    assert data["sellerId"] == 1
    assert data["price"] == 29.99
    assert "id" in data
    assert "createdAt" in data
    assert "updatedAt" in data


def test_list_products(client):
    client.post("/products", json={
        "sellerId": 1,
        "title": "Producto 1",
        "description": "Desc 1",
        "price": 10.00,
    })
    client.post("/products", json={
        "sellerId": 2,
        "title": "Producto 2",
        "description": "Desc 2",
        "price": 20.00,
    })

    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 2
    assert data[0]["id"] < data[1]["id"]


def test_get_product(client):
    create = client.post("/products", json={
        "sellerId": 1,
        "title": "Remera",
        "description": "Desc",
        "price": 15.00,
    })
    product_id = create.json()["data"]["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == product_id


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_update_product(client):
    create = client.post("/products", json={
        "sellerId": 1,
        "title": "Original",
        "description": "Desc",
        "price": 10.00,
    })
    product_id = create.json()["data"]["id"]

    response = client.put(f"/products/{product_id}", json={
        "title": "Actualizado",
        "description": "Nueva desc",
        "price": 25.00,
    })
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["title"] == "Actualizado"
    assert data["price"] == 25.00
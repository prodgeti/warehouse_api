from fastapi.testclient import TestClient


def test_create_product(client: TestClient):
    response = client.post("/products", json={
        "name": "Test Product",
        "description": "This is a test product",
        "price": 10.5,
        "stock_quantity": 100
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "This is a test product"
    assert data["price"] == 10.5
    assert data["stock_quantity"] == 100


def test_get_product(client: TestClient):

    product = {
        "name": "Test Product",
        "description": "Test",
        "price": 5.0,
        "stock_quantity": 50
    }
    response = client.post("/products", json=product)
    product_id = response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product"


def test_update_product(client: TestClient):

    product = {
        "name": "Update Product",
        "description": "Test",
        "price": 15.0,
        "stock_quantity": 30
    }
    response = client.post("/products", json=product)
    product_id = response.json()["id"]

    update_data = {
        "name": "Updated Product",
        "description": "Updated",
        "price": 20.0,
        "stock_quantity": 25
    }
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 20.0


def test_delete_product(client: TestClient):

    product = {
        "name": "Delete Product",
        "description": "Test",
        "price": 20.0,
        "stock_quantity": 15
    }
    response = client.post("/products", json=product)
    product_id = response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted"}

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404

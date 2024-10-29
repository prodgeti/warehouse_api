from fastapi.testclient import TestClient


def test_create_order(client: TestClient):
    response = client.post(
        "/orders",
        json={
            "created_date": "2024-10-28",
            "status": "в процессе"
        }
    )
    assert response.status_code == 200


def test_get_order(client: TestClient):
    response = client.post(
        "/orders",
        json={
            "created_date": "2024-10-28",
            "status": "в процессе"
        }
    )
    assert response.status_code == 200
    order_id = response.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200


def test_update_order_status(client: TestClient):

    response = client.post(
        "/orders",
        json={
            "created_date": "2024-10-28",
            "status": "в процессе"
        }
    )
    assert response.status_code == 200
    order_id = response.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "отправлен"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "отправлен"


def test_add_order_item(client: TestClient):
    product_response = client.post("/products", json={
        "name": "Order Product",
        "description": "Product for order",
        "price": 15.0,
        "stock_quantity": 20
    })
    assert product_response.status_code == 200
    product_id = product_response.json()["id"]

    order_response = client.post(
        "/orders",
        json={"created_date": "2024-10-28", "status": "в процессе"}
    )
    assert order_response.status_code == 200
    order_id = order_response.json()["id"]

    item_response = client.post(
        f"/orders/{order_id}/items",
        json={"product_id": product_id, "quantity": 2}
    )
    assert item_response.status_code == 200

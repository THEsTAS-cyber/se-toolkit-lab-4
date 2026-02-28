"""End-to-end tests for the GET /interactions endpoint."""
import httpx


def test_get_interactions_returns_200(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert isinstance(response.json(), list)

# Keep
def test_get_interactions_with_item_id_filter(client: httpx.Client) -> None:
    response = client.get("/interactions/", params={"item_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(item["item_id"] == 1 for item in data)

# Keep
def test_get_interactions_with_zero_item_id(client: httpx.Client) -> None:
    """Граничный случай: фильтрация по item_id=0."""
    response = client.get("/interactions/", params={"item_id": 0})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(item["item_id"] == 0 for item in data)

# Keep
def test_get_interactions_with_negative_item_id(client: httpx.Client) -> None:
    """Граничный случай: фильтрация по отрицательному item_id."""
    response = client.get("/interactions/", params={"item_id": -1})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(item["item_id"] == -1 for item in data)

# Keep
def test_get_interactions_with_large_item_id(client: httpx.Client) -> None:
    """Граничный случай: фильтрация по большому item_id."""
    large_id = 2**31 - 1
    response = client.get("/interactions/", params={"item_id": large_id})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(item["item_id"] == large_id for item in data)
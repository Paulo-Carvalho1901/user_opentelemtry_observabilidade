# tests/test_main.py
def test_ping(client):
    response = client.get("/test-trace")
    assert response.status_code == 200
    assert response.json() == {"status": "trace ok"}

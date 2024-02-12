from fastapi.testclient import TestClient

from app.main import app


def test_ping_deve_retornar_200_e_pong():
    client = TestClient(app)  # Arrange

    response = client.get('/ping')  # Act

    assert response.status_code == 200  # Assert
    assert response.json() == { 'ping': 'pong!' } # Assert
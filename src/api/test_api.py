import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parents[0]))

from fastapi.testclient import TestClient

from server import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "healthy"}

def test_token():
    response = client.post(
        '/token', 
        {'username': 'kduwadi', 'password': 'password'}
    )
    assert response.status_code == 200
    print(response.json())
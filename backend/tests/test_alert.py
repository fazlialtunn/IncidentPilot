from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code==200
    assert r.json()['status']=='ok'

def test_webhook_alert():
    payload = {"service":"checkout-service","severity":"critical","summary":"Payment error"}
    r = client.post('/webhook/alert', json=payload)
    assert r.status_code==200
    assert 'incident_id' in r.json()

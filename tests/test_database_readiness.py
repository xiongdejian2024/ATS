from fastapi.testclient import TestClient


def test_health_and_ready_detect_missing_schema_without_disclosing_details():
    from main import app
    from database import engine, Base
    client = TestClient(app)
    assert client.get('/health').status_code == 200
    assert client.get('/ready').json() == {'status': 'ready'}
    Base.metadata.tables['agent_log_cursors'].drop(engine)
    response = client.get('/ready')
    assert response.status_code == 503
    assert response.json() == {'status': 'not_ready'}
    assert client.get('/health').status_code == 200

import pytest
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from core.origin_access import OriginAccessMiddleware

KEY = 'synthetic-only-' * 4


def client():
    app = FastAPI()
    @app.get('/ready')
    async def ready():
        return {'ready': True}
    @app.websocket('/ws/agent')
    async def websocket(socket: WebSocket):
        await socket.accept()
        await socket.send_text('downstream identity still required')
    app.add_middleware(OriginAccessMiddleware, required=True, service_key=KEY)
    return TestClient(app)


@pytest.mark.parametrize('value', ['', KEY, 'Bearer wrong', 'bearer ' + KEY, 'Bearer ' + KEY + ' '])
def test_http_missing_or_wrong_origin_identity_rejected(value):
    assert client().get('/ready', headers={'X-ATS-Origin-Authorization': value}).status_code == 403


def test_valid_origin_identity_reaches_original_app():
    assert client().get('/ready', headers={'X-ATS-Origin-Authorization': 'Bearer ' + KEY}).json() == {'ready': True}


def test_duplicate_header_is_not_accepted():
    assert client().get('/ready', headers=[('X-ATS-Origin-Authorization', 'Bearer ' + KEY)] * 2).status_code == 403


def test_agent_websocket_has_no_gate_bypass():
    with pytest.raises(WebSocketDisconnect) as error:
        with client().websocket_connect('/ws/agent'):
            pass
    assert error.value.code == 1008
    with client().websocket_connect('/ws/agent', headers={'X-ATS-Origin-Authorization': 'Bearer ' + KEY}) as socket:
        assert socket.receive_text() == 'downstream identity still required'


@pytest.mark.parametrize('key', ['', 'short', KEY + '\n', KEY + '\r'])
def test_missing_or_malformed_configuration_fails_closed(key):
    with pytest.raises(ValueError):
        OriginAccessMiddleware(None, required=True, service_key=key)

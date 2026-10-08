"""Additional server-to-server gate; never replaces ATS user/Agent identity."""
import secrets


class OriginAccessMiddleware:
    def __init__(self, app, *, required=False, service_key=''):
        if required and (len(service_key) < 32 or '\r' in service_key or '\n' in service_key):
            raise ValueError('Origin access requires a securely configured service key')
        self.app = app
        self.required = required
        self.expected = ('Bearer ' + service_key).encode('utf-8')

    async def __call__(self, scope, receive, send):
        if self.required and scope['type'] in {'http', 'websocket'}:
            values = [value for name, value in scope.get('headers', [])
                      if name.lower() == b'x-ats-origin-authorization']
            if len(values) != 1 or not secrets.compare_digest(values[0], self.expected):
                if scope['type'] == 'websocket':
                    await send({'type': 'websocket.close', 'code': 1008})
                else:
                    await send({'type': 'http.response.start', 'status': 403,
                                'headers': [(b'content-type', b'application/json')]})
                    await send({'type': 'http.response.body', 'body': b'{"detail":"Origin access denied"}'})
                return
        await self.app(scope, receive, send)

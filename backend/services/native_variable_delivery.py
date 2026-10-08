"""Capability gating before claim and sending to that exact authenticated session."""

import json

CAPABILITY = "native_http_variables_v1"
PROCESSORS_CAPABILITY = "native_http_processors_v1"
WIRE_LIMIT = 12 * 1024 * 1024  # Agent websocket reception is bounded to 16 MiB.


def requires_variables(message):
    return any(
        case.get("initialVariables")
        or any(
            r.get("initialVariables") or r.get("environmentVariables")
            for r in case.get("requests", [])
        )
        for case in message.get("native_cases", []) or []
    )


def validate_budget(message):
    if len(json.dumps(message, ensure_ascii=False).encode()) > WIRE_LIMIT:
        raise ValueError("原生HTTP冻结消息超过12MiB，请减少场景步骤或变量声明")
    return message


def required_capabilities(message):
    required = {CAPABILITY} if requires_variables(message) else set()
    if any(c.get('globalPreProcessors') or c.get('globalPostProcessors') or any(r.get('reportPhases') or r.get('preProcessors') or r.get('postProcessors') or (r.get('mockResponse') or {}).get('enable') for r in c.get('requests', [])) for c in message.get('native_cases', []) or []):
        required.add(PROCESSORS_CAPABILITY)
    from services.native_hooks import hooks
    if any(hooks(message)):
        required.add('script_jobs_v1')
    return required


def requires_extensions(message):
    return bool(required_capabilities(message))


def session_for(manager, environment_id, message):
    from services.native_hooks import required_node
    node = required_node(message)
    if node and node != environment_id:
        return None
    session = manager.sessions.get(environment_id)
    if (
        session
        and getattr(session, 'protocol_version', 0) >= 2
        and manager.is_live(session)
        and manager.is_current(session)
        and getattr(session, "auth_received", False)
        and required_capabilities(message) <= set(getattr(session, "capabilities", ()))
    ):
        return session
    return None


async def send(manager, environment_id, message, session):
    if requires_extensions(message):
        return await manager.send_session(session, message)
    return await manager.send_message(environment_id, message)

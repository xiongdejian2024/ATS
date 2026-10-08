"""Capability gating before claim and sending to that exact authenticated session."""

import json

CAPABILITY = "native_http_variables_v1"
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


def session_for(manager, environment_id, message):
    session = manager.sessions.get(environment_id)
    if (
        session
        and manager.is_live(session)
        and manager.is_current(session)
        and getattr(session, "auth_received", False)
        and CAPABILITY in getattr(session, "capabilities", ())
    ):
        return session
    return None


async def send(manager, environment_id, message, session):
    if requires_variables(message):
        return await manager.send_session(session, message)
    return await manager.send_message(environment_id, message)

#!/usr/bin/env python3
"""Launch an isolated ATS software lab on loopback; never reuse the user's DB."""

import argparse
import asyncio
import os
import socket
import sys
import tempfile
import uuid
import json
import re
import signal
from datetime import date
from pathlib import Path


async def main(args):
    root = Path(__file__).resolve().parents[1]
    directory = Path(tempfile.mkdtemp(prefix="ats-local-lab-"))
    os.environ["DATABASE_URL"] = "sqlite:///" + str(directory / "ats.sqlite")
    os.environ["ENVIRONMENT"] = "test"
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "backend"))
    import httpx
    import uvicorn
    from main import app
    from database import Base, engine, SessionLocal
    from models import User
    from core.security import get_password_hash
    from agent.agent import Agent
    from agent.config import Config
    from agent.websocket_client import WebSocketClient
    from agent.sat_runner import terminate_process

    scheduler_task = None
    if args.management:
        from fastapi import Request
        from services.task_scheduler import scheduler_loop

        @app.post("/api/v1/lab-model/chat/completions")
        async def local_model(request: Request):
            """仅在隔离验收进程提供协议替身，不接外部供应商。"""
            data = await request.json()
            system = data.get("messages", [{}])[0].get("content", "")
            match = re.search(r"严格生成 (\d+) 条", system)
            if match:
                case_type = re.search(r"用例类型 (\w+)", system).group(1)
                content = json.dumps({"cases": [dict(name=f"软件验收草稿 {i + 1}", type=case_type,
                    priority="P2", precondition="隔离软件环境", requirement_ref="LAB-ONLY",
                    steps=[{"action": "输入测试参数", "expected": "返回对应校验提示"}],
                    tags=["软件验收"]) for i in range(int(match.group(1)))]}, ensure_ascii=False)
            else:
                content = "软件验收模型替身连接成功。此回答仅用于验证协议与会话保存。"
            return {"choices": [{"message": {"role": "assistant", "content": content}}]}

    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        db.add(
            User(
                id=str(uuid.uuid4()),
                username="local_demo",
                email="local_demo@example.com",
                password_hash=get_password_hash("ats-local-demo"),
            )
        )
        db.commit()
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", args.port))
    port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="error", lifespan="off"))
    serving = asyncio.create_task(server.serve(sockets=[sock]))
    while not server.started:
        await asyncio.sleep(0.05)
    if args.management:
        scheduler_task = asyncio.create_task(scheduler_loop())
    client = httpx.AsyncClient(base_url=f"http://127.0.0.1:{port}/api/v1")
    login = (
        await client.post(
            "/auth/login", json={"username": "local_demo", "password": "ats-local-demo"}
        )
    ).json()["data"]
    client.headers["Authorization"] = "Bearer " + login["access_token"]

    async def post(path, data):
        response = await client.post(path, json=data)
        response.raise_for_status()
        return response.json()["data"]

    project = await post("/projects", {"name": "SAT / ECU 离线软件验收"})
    cases = []
    for code in ["sat_import", "ecu_positive", "ecu_negative", "ecu_lifecycle"]:
        cases.append(
            await post(
                "/test-cases",
                {
                    "project_id": project["id"],
                    "case_code": code,
                    "name": code,
                    "type": "functional",
                    "is_automated": True,
                },
            )
        )
    ids = [case["id"] for case in cases]
    plan = await post(
        "/test-plans",
        {
            "project_id": project["id"],
            "name": "离线计划",
            "startDate": date.today().isoformat(),
            "testCaseIds": ids,
        },
    )
    environment = await post(
        "/environments",
        {
            "name": "本机软件节点",
            "remoteWorkDir": str(directory / "agent"),
            "reconnectDelay": "1",
        },
    )
    config = Config()
    config.work_dir = directory / "agent"
    config.work_dir.mkdir()
    config.sat_root, config.ecu_root = args.sat_root, args.ecu_root
    config.monitor_interval = 2
    agent = Agent(config)
    agent.work_dir, agent.running = config.work_dir, True
    agent.ws_client = WebSocketClient(
        f"ws://127.0.0.1:{port}/ws/agent",
        environment["token"],
        on_message=agent.on_message,
        on_connect=agent.on_connect,
    )
    assert await agent.ws_client.connect()
    receiving = asyncio.create_task(agent.ws_client.receive_messages())
    monitoring = asyncio.create_task(agent._monitor_loop())
    while not agent.environment_id:
        await asyncio.sleep(0.02)
    await post(
        f'/test-plans/{plan["id"]}/suites',
        {
            "plan_id": plan["id"],
            "name": "SAT / ECU 离线验收",
            "environment_id": environment["id"],
            "execution_command": "xat --mode offline",
            "case_ids": ids,
        },
    )
    frontend = await asyncio.create_subprocess_exec(
        "npm",
        "run",
        "dev",
        "--",
        "--host",
        "127.0.0.1",
        "--port",
        str(args.frontend_port),
        "--strictPort",
        cwd=str(root / "frontend"),
        env=dict(os.environ, ATS_BACKEND_URL=f"http://127.0.0.1:{port}"),
        start_new_session=(os.name == "posix"),
    )
    print(
        f"LAB http://127.0.0.1:{args.frontend_port} ; local_demo / ats-local-demo ; state {directory}",
        flush=True,
    )
    stop_event = asyncio.Event()
    if os.name == "posix":
        for stop_signal in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_running_loop().add_signal_handler(stop_signal, stop_event.set)
    try:
        await stop_event.wait()
    finally:
        if scheduler_task:
            scheduler_task.cancel()
            await asyncio.gather(scheduler_task, return_exceptions=True)
        await agent.stop()
        receiving.cancel()
        monitoring.cancel()
        await asyncio.gather(receiving, monitoring, return_exceptions=True)
        await terminate_process(frontend)
        server.should_exit = True
        await serving
        await client.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    base = Path(__file__).resolve().parents[2]
    parser.add_argument("--sat-root", default=str(Path(__file__).resolve().parents[1] / "xat"))
    parser.add_argument("--ecu-root", default=str(Path(__file__).resolve().parents[1] / "xat/packages/ecu"))
    parser.add_argument("--port", type=int, default=8800)
    parser.add_argument("--frontend-port", type=int, default=3300)
    parser.add_argument("--management", action="store_true", help="启用隔离任务调度和本地模型协议替身，便于四模块浏览器验收")
    try:
        asyncio.run(main(parser.parse_args()))
    except KeyboardInterrupt:
        pass

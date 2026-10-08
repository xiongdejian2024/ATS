"""Bounded default CI pressure test; ATS_LOG_SOAK_SECONDS=180 runs local soak."""

import asyncio
import json
import os
import time
import tracemalloc
from pathlib import Path

import pytest
from loguru import logger

from agent.log_spool import LogDelivery, LogSpool
from services.agent_log_ingest import persist_log_batch
from models.test_suite import TestSuiteLog as SuiteLog
from test_plan_orchestration import plan_lab
from test_agent_log_delivery import add_task, payload


@pytest.mark.asyncio
async def test_sustained_outage_slow_ack_and_drain(plan_lab, tmp_path):
    db, _ = plan_lab
    add_task(db)
    seconds = max(3, float(os.environ.get("ATS_LOG_SOAK_SECONDS", "3")))
    spool = LogSpool(tmp_path / "soak.sqlite", max_bytes=65536, max_records=128)
    metrics = dict(
        duration_seconds=seconds,
        produced_messages=0,
        produced_utf8_bytes=0,
        sent_batches=0,
        wire_records=0,
        durable_ack_calls=0,
        peak_spool_bytes=0,
        peak_spool_records=0,
        peak_sqlite_bytes=0,
        heartbeat_ticks=0,
        longest_heartbeat_gap=0,
        peak_ack_tasks=0,
    )
    start = time.monotonic()
    pending = set()

    class Client:
        connected = True

        async def send_message(self, message):
            metrics["sent_batches"] += 1
            metrics["wire_records"] += len(message["records"])
            response, _ = persist_log_batch(db, "node", message)
            assert response["type"] == "log_batch_ack", response
            fraction = (time.monotonic() - start) / seconds
            delay = 0.12 if 0.4 <= fraction < 0.7 else 0.001

            async def acknowledge():
                await asyncio.sleep(delay)
                if self.connected:
                    delivery.acknowledge(response)
                    metrics["durable_ack_calls"] += 1

            task = asyncio.create_task(acknowledge())
            pending.add(task)
            task.add_done_callback(pending.discard)
            metrics["peak_ack_tasks"] = max(metrics["peak_ack_tasks"], len(pending))
            return True

    client = Client()
    delivery = LogDelivery(spool, client, logger, retry_seconds=0.1)
    delivery.negotiate(dict(capabilities=["log_batch_v1"]))

    async def transport_phases():
        await asyncio.sleep(seconds * 0.2)
        client.connected = False
        await asyncio.sleep(seconds * 0.2)
        client.connected = True
        delivery.wake()

    stop_heartbeat = asyncio.Event()

    async def heartbeat():
        previous = time.monotonic()
        while not stop_heartbeat.is_set():
            await asyncio.sleep(0.02)
            now = time.monotonic()
            metrics["heartbeat_ticks"] += 1
            metrics["longest_heartbeat_gap"] = max(
                metrics["longest_heartbeat_gap"], now - previous
            )
            previous = now

    phases = asyncio.create_task(transport_phases())
    pulse = asyncio.create_task(heartbeat())
    tracemalloc.start()
    try:
        while time.monotonic() - start < seconds:
            for _ in range(10):
                text = f'{metrics["produced_messages"]:08d} ' + "日志😀" * 20
                await delivery.enqueue(payload(text))
                metrics["produced_messages"] += 1
                metrics["produced_utf8_bytes"] += len(text.encode())
                used = spool.usage()
                metrics["peak_spool_bytes"] = max(
                    metrics["peak_spool_bytes"], used["bytes"]
                )
                metrics["peak_spool_records"] = max(
                    metrics["peak_spool_records"], used["records"]
                )
                metrics["peak_sqlite_bytes"] = max(
                    metrics["peak_sqlite_bytes"], spool.path.stat().st_size
                )
            await asyncio.sleep(0.05)
        await phases
        deadline = time.monotonic() + 10
        while spool.usage()["records"] and time.monotonic() < deadline:
            await asyncio.sleep(0.01)
        metrics["final_spool"] = spool.usage()
        metrics["elapsed_seconds"] = time.monotonic() - start
        metrics["python_traced_peak_bytes"] = tracemalloc.get_traced_memory()[1]

        raw = db.query(SuiteLog.message).scalar()
        metrics["persisted_utf8_bytes"] = len(raw.encode())
        metrics["persisted_lines"] = len(raw.splitlines())
        assert metrics["persisted_lines"] == metrics["produced_messages"]
        assert (
            metrics["persisted_utf8_bytes"]
            == metrics["produced_utf8_bytes"] + metrics["produced_messages"] - 1
        )
        assert metrics["final_spool"]["records"] == 0
        assert (
            metrics["peak_spool_bytes"] <= 65536
            and metrics["peak_spool_records"] <= 128
        )
        assert metrics["peak_sqlite_bytes"] <= spool.page_limit * 4096
        assert metrics["peak_ack_tasks"] <= 5
        assert metrics["longest_heartbeat_gap"] < 2
        report = os.environ.get("ATS_LOG_SOAK_REPORT")
        if report:
            Path(report).write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        print("DURABLE_LOG_SOAK " + json.dumps(metrics, sort_keys=True))
    finally:
        tracemalloc.stop()
        stop_heartbeat.set()
        await pulse
        phases.cancel()
        await asyncio.gather(phases, return_exceptions=True)
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        await delivery.close()

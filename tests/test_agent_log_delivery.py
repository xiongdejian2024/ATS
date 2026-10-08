"""Isolated durable logs: restart, lost ACKs, bounded soak and explicit quotas."""

import asyncio
import json
import tracemalloc
import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy import event
from loguru import logger

from agent.log_spool import (
    LogSpool,
    LogDelivery,
    SpoolFull,
    MAX_BATCH_BYTES,
    MAX_BATCH_RECORDS,
)
from test_plan_orchestration import plan_lab
from models.task_queue import TaskQueue
from models.test_suite import TestSuiteLog as SuiteLog
from models.agent_log import AgentLogCursor, AgentTaskLog
from services.agent_log_ingest import persist_log_batch


def payload(text="hello", **kwargs):
    return dict(
        type="test_suite_log",
        suite_id="suite-0",
        execution_id="exec",
        message=text,
        **kwargs
    )


def batch(*texts, stream_id=None, first=1):
    return dict(
        type="log_batch",
        stream_id=stream_id or str(uuid.uuid4()),
        records=[
            dict(sequence=i, payload=payload(text))
            for i, text in enumerate(texts, first)
        ],
    )


def add_task(db):
    db.add(
        TaskQueue(
            id="task",
            suite_id="suite-0",
            execution_id="exec",
            environment_id="node",
            executor_id="owner",
            status="running",
        )
    )
    db.commit()


def test_spool_restart_quota_and_ack_bounds(tmp_path):
    path = tmp_path / "logs.sqlite"
    spool = LogSpool(path, max_bytes=16384, max_records=2)
    stream = spool.stream_id
    spool.append(payload("first"))
    spool.append(payload("second"))
    with pytest.raises(SpoolFull):
        spool.append(payload("never accepted"))
    before = spool.batch()
    assert not spool.acknowledge(100)
    assert not spool.acknowledge(True)
    spool.close()
    restarted = LogSpool(path, max_bytes=16384, max_records=2)
    assert restarted.stream_id == stream and restarted.batch() == before
    assert restarted.acknowledge(1)
    assert restarted.append(payload("third")) == 3
    restarted.close()
    final = LogSpool(path, max_bytes=16384, max_records=2)
    assert [r["sequence"] for r in final.batch()["records"]] == [2, 3]
    final.close()


def test_spool_high_volume_reuses_bounded_disk_and_memory(tmp_path):
    path = tmp_path / "soak.sqlite"
    spool = LogSpool(path, max_bytes=256 * 1024, max_records=128)
    tracemalloc.start()
    max_file = 0
    # >30 MiB total input through a 256 KiB spool, no growing in-memory list.
    for iteration in range(400):
        for index in range(20):
            spool.append(payload("日志😀" * 400))
        current = spool.batch()
        assert len(current["records"]) <= MAX_BATCH_RECORDS
        assert (
            sum(
                len(
                    json.dumps(
                        r["payload"], ensure_ascii=False, separators=(",", ":")
                    ).encode()
                )
                for r in current["records"]
            )
            <= MAX_BATCH_BYTES
        )
        max_file = max(max_file, path.stat().st_size)
        while current["records"]:
            spool.acknowledge(current["records"][-1]["sequence"])
            current = spool.batch()
        max_file = max(max_file, path.stat().st_size)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 3 * 1024 * 1024
    assert max_file <= spool.page_limit * 4096
    assert spool.usage()["records"] == 0
    assert path.stat().st_size < 128 * 1024
    spool.close()


@pytest.mark.asyncio
async def test_backpressure_waits_without_evicting_and_resumes_after_ack(tmp_path):
    spool = LogSpool(tmp_path / "logs.sqlite", max_bytes=16384, max_records=1)
    client = SimpleNamespace(connected=False)
    delivery = LogDelivery(spool, client, logger, retry_seconds=0.01)
    await delivery.enqueue(payload("first"))
    producer = asyncio.create_task(delivery.enqueue(payload("second")))
    await asyncio.sleep(0.03)
    assert not producer.done() and spool.usage()["records"] == 1
    assert spool.batch()["records"][0]["payload"]["message"] == "first"
    delivery.sent_through = 1
    delivery.acknowledge(
        dict(type="log_batch_ack", stream_id=spool.stream_id, through_sequence=1)
    )
    await asyncio.wait_for(producer, 0.5)
    assert spool.batch()["records"][0]["payload"]["message"] == "second"
    await delivery.close()


@pytest.mark.asyncio
async def test_disk_full_backpressures_and_cancellation_is_prompt(
    tmp_path, monkeypatch
):
    spool = LogSpool(tmp_path / "logs.sqlite")
    delivery = LogDelivery(
        spool, SimpleNamespace(connected=False), logger, retry_seconds=0.01
    )

    def full(_):
        raise SpoolFull("disk full")

    monkeypatch.setattr(spool, "append", full)
    task = asyncio.create_task(delivery.enqueue(payload("retained in producer")))
    await asyncio.sleep(0.02)
    assert not task.done()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(task, 0.2)
    await delivery.close()


def test_batch_persists_once_and_detects_gap_and_cross_node(plan_lab):
    db, _ = plan_lab
    add_task(db)
    message = batch("first😀", "second")
    response, deltas = persist_log_batch(db, "node", message)
    assert response["type"] == "log_batch_ack" and response["through_sequence"] == 2
    assert db.query(SuiteLog.message).scalar() == "first😀\nsecond"
    assert deltas[-1][1]["endOffset"] == len("first😀\nsecond")
    again, duplicates = persist_log_batch(db, "node", message)
    assert again == response and duplicates == [] and db.query(SuiteLog).count() == 1
    gap, _ = persist_log_batch(
        db, "node", batch("too far", stream_id=message["stream_id"], first=4)
    )
    assert gap["reason"] == "gap" and gap["expected_sequence"] == 3
    from models import Environment
    db.add(Environment(id="other-node", name="Other authenticated node"))
    db.commit()
    wrong, _ = persist_log_batch(db, "other-node", batch("not owned"))
    assert wrong["reason"] == "execution_not_owned"
    overlap, deltas = persist_log_batch(
        db, "node", batch("second", "third", stream_id=message["stream_id"], first=2)
    )
    assert overlap["through_sequence"] == 3 and len(deltas) == 1
    assert db.query(SuiteLog.message).scalar() == "first😀\nsecond\nthird"


def test_commit_failure_cannot_ack_or_advance_cursor(plan_lab, monkeypatch):
    db, _ = plan_lab
    add_task(db)
    message = batch("must survive")
    original = db.commit
    monkeypatch.setattr(
        db,
        "commit",
        lambda: (_ for _ in ()).throw(OSError("simulated fsync/database failure")),
    )
    with pytest.raises(OSError):
        persist_log_batch(db, "node", message)
    assert db.query(SuiteLog).count() == 0 and db.query(AgentLogCursor).count() == 0
    monkeypatch.setattr(db, "commit", original)
    response, _ = persist_log_batch(db, "node", message)
    assert (
        response["type"] == "log_batch_ack"
        and db.query(SuiteLog.message).scalar() == "must survive"
    )


def test_ingestion_does_not_load_full_history_and_preserves_raw(plan_lab):
    db, _ = plan_lab
    add_task(db)
    text = "old😀" * 100000
    db.add(
        SuiteLog(id="existing", suite_id="suite-0", execution_id="exec", message=text)
    )
    db.commit()
    statements = []

    def capture(_c, _cu, statement, _p, _ctx, _many):
        statements.append(statement)

    event.listen(db.bind, "before_cursor_execute", capture)
    try:
        response, deltas = persist_log_batch(db, "node", batch("new😀"))
    finally:
        event.remove(db.bind, "before_cursor_execute", capture)
    assert response["type"] == "log_batch_ack"
    assert not any(
        s.lstrip().upper().startswith("SELECT")
        and "test_suite_logs.message AS test_suite_logs_message" in s
        for s in statements
    )
    assert deltas[0][1]["endOffset"] == len(text + "\nnew😀")
    assert db.query(SuiteLog.message).scalar() == text + "\nnew😀"


def test_raw_quota_nack_is_atomic_and_no_evidence_evicted(plan_lab, monkeypatch):
    import services.agent_log_ingest as ingest

    db, _ = plan_lab
    add_task(db)
    monkeypatch.setattr(ingest, "MAX_EXECUTION_LOG_BYTES", 8)
    message = batch("first", "second")
    response, deltas = persist_log_batch(db, "node", message)
    assert response["reason"] == "execution_log_quota" and deltas == []
    assert db.query(SuiteLog).count() == 0 and db.query(AgentLogCursor).count() == 0


@pytest.mark.asyncio
async def test_lost_ack_reconnect_and_restarted_spool_replays_without_duplicate(
    plan_lab, tmp_path
):
    db, _ = plan_lab
    add_task(db)
    spool = LogSpool(tmp_path / "logs.sqlite")
    sends, delivery = [], None

    class Client:
        connected = True

        async def send_message(self, message):
            sends.append(message)
            response, _ = persist_log_batch(db, "node", message)
            if len(sends) == 1:
                self.connected = False  # commit happened but ACK lost
            else:
                delivery.acknowledge(response)
            return True

    client = Client()
    delivery = LogDelivery(spool, client, logger, retry_seconds=0.01)
    delivery.negotiate(dict(capabilities=["log_batch_v1"]))
    await delivery.enqueue(payload("survives disconnect😀"))
    await asyncio.sleep(0.04)
    assert spool.usage()["records"] == 1 and db.query(SuiteLog).count() == 1
    await delivery.close()
    restarted = LogSpool(tmp_path / "logs.sqlite")
    client.connected = True
    delivery = LogDelivery(restarted, client, logger, retry_seconds=0.01)
    delivery.negotiate(dict(capabilities=["log_batch_v1"]))
    for _ in range(50):
        if restarted.usage()["records"] == 0:
            break
        await asyncio.sleep(0.01)
    assert restarted.usage()["records"] == 0 and len(sends) == 2
    assert db.query(SuiteLog.message).scalar() == "survives disconnect😀"
    await delivery.close()


@pytest.mark.asyncio
async def test_large_unicode_chunks_reconstruct_without_extra_newlines(
    plan_lab, tmp_path
):
    db, _ = plan_lab
    add_task(db)
    spool = LogSpool(tmp_path / "logs.sqlite")

    class Client:
        connected = True

        async def send_message(self, message):
            response, _ = persist_log_batch(db, "node", message)
            delivery.acknowledge(response)
            return True

    delivery = LogDelivery(spool, Client(), logger, retry_seconds=0.01)
    delivery.negotiate(dict(capabilities=["log_batch_v1"]))
    text = "日志😀" * 30000
    await delivery.enqueue(payload(text))
    for _ in range(100):
        if not spool.usage()["records"]:
            break
        await asyncio.sleep(0.01)
    assert spool.usage()["records"] == 0
    assert db.query(SuiteLog.message).scalar() == text
    await delivery.close()


def test_direct_task_logs_persist_and_legacy_upgrade_gets_new_stream(
    plan_lab, tmp_path
):
    db, _ = plan_lab
    spool = LogSpool(tmp_path / "logs.sqlite")
    spool.append(dict(type="task_log", task_id="manual", message="socket-sent"))
    spool.append(dict(type="task_log", task_id="manual", message="retained"))
    old = spool.stream_id
    spool.acknowledge(1, legacy=True)
    assert spool.prepare_durable_stream() and spool.stream_id != old
    assert spool.batch()["records"][0]["sequence"] == 1
    response, _ = persist_log_batch(db, "node", spool.batch())
    assert response["type"] == "log_batch_ack"
    assert db.query(AgentTaskLog.message).scalar() == "retained"
    spool.close()


@pytest.mark.asyncio
async def test_missing_ack_gap_does_not_discard_retained_evidence(tmp_path):
    spool = LogSpool(tmp_path / "logs.sqlite")
    spool.append(payload("one"))
    spool.append(payload("two"))
    spool.acknowledge(1)
    delivery = LogDelivery(spool, SimpleNamespace(connected=False), logger)
    delivery.acknowledge(
        dict(
            type="log_batch_nack",
            stream_id=spool.stream_id,
            expected_sequence=1,
            reason="gap",
        )
    )
    assert delivery.blocked_reason == "gap" and spool.usage()["records"] == 1
    delivery.acknowledge(
        dict(type="log_batch_ack", stream_id=spool.stream_id, through_sequence=999)
    )
    assert spool.usage()["records"] == 1
    await delivery.close()


@pytest.mark.asyncio
async def test_task_output_preview_and_local_file_quota_stop_child(tmp_path):
    import sys
    from agent.task_executor import TaskExecutor

    executor = TaskExecutor(tmp_path, max_log_bytes=100000, total_log_bytes=150000)
    result = await executor.execute_task(
        dict(
            task_id="verbose",
            command=[sys.executable, "-c", "import sys;sys.stdout.write('x'*80000)"],
            timeout=5,
        )
    )
    assert result["status"] == "success" and len(result["output"]) < 66000
    assert "characters omitted" in result["output"]
    too_much = await executor.execute_task(
        dict(
            task_id="quota",
            command=[sys.executable, "-c", "import sys;sys.stdout.write('x'*3000000)"],
            timeout=5,
        )
    )
    assert too_much["status"] == "error" and "quota" in too_much["error"]
    assert (
        sum(p.stat().st_size for p in (tmp_path / "logs/tasks").glob("*.log")) <= 150000
    )
    assert not executor.tasks


@pytest.mark.asyncio
async def test_legacy_controller_compatibility_is_explicit_socket_only(tmp_path):
    spool = LogSpool(tmp_path / "legacy.sqlite")
    sent = []

    class Client:
        connected = True

        async def send_log_legacy(self, message):
            sent.append(message)
            return True

    delivery = LogDelivery(spool, Client(), logger, retry_seconds=0.01)
    await delivery.enqueue(payload("legacy"))
    delivery.negotiate({})
    for _ in range(50):
        if not spool.usage()["records"]:
            break
        await asyncio.sleep(0.01)
    assert (
        delivery.capable is False
        and len(sent) == 1
        and sent[0]["type"] == "test_suite_log"
    )
    assert spool.usage()["records"] == 0
    await delivery.close()


@pytest.mark.asyncio
async def test_new_messages_do_not_flood_unacknowledged_batch(tmp_path):
    spool = LogSpool(tmp_path / "one-flight.sqlite")
    sent = []

    class Client:
        connected = True

        async def send_message(self, message):
            sent.append(message)
            return True

    delivery = LogDelivery(spool, Client(), logger, retry_seconds=0.2)
    delivery.negotiate(dict(capabilities=["log_batch_v1"]))
    await delivery.enqueue(payload("first"))
    await asyncio.sleep(0.01)
    for i in range(20):
        await delivery.enqueue(payload(str(i)))
        await asyncio.sleep(0.001)
    assert len(sent) == 1 and spool.usage()["records"] == 21
    await delivery.close()


@pytest.mark.asyncio
async def test_control_char_escaping_stays_bounded_and_lossless(tmp_path):
    spool = LogSpool(tmp_path / "control.sqlite")
    delivery = LogDelivery(spool, SimpleNamespace(connected=False), logger)
    text = "\x00\x01\n\t" * 3000
    await delivery.enqueue(payload(text))
    recovered = []
    while spool.usage()["records"]:
        current = spool.batch()
        recovered.extend(r["payload"]["message"] for r in current["records"])
        spool.acknowledge(current["records"][-1]["sequence"])
    assert "".join(recovered) == text
    await delivery.close()


def test_invalid_batch_does_not_mutate_database(plan_lab):
    db, _ = plan_lab
    add_task(db)
    for malformed in [
        dict(stream_id="bad", records=[]),
        dict(
            stream_id="urn:uuid:" + str(uuid.uuid4()),
            records=[dict(sequence=1, payload=payload())],
        ),
        dict(
            stream_id=str(uuid.uuid4()),
            records=[dict(sequence=True, payload=payload())],
        ),
        dict(
            stream_id=str(uuid.uuid4()),
            records=[dict(sequence=1, payload=payload("x" * 20000))],
        ),
        dict(
            stream_id=str(uuid.uuid4()),
            records=[
                dict(sequence=1, payload=payload()),
                dict(sequence=3, payload=payload()),
            ],
        ),
    ]:
        response, deltas = persist_log_batch(db, "node", malformed)
        assert response["type"] == "log_batch_nack" and deltas == []
    assert db.query(SuiteLog).count() == 0 and db.query(AgentLogCursor).count() == 0


@pytest.mark.asyncio
async def test_full_spool_suite_cancel_completes_before_receiver_can_process_ack(
    tmp_path, sat_config, monkeypatch
):
    """Cancel callback runs on receiver; it cannot require a later receiver ACK."""
    import sys
    from agent.agent import Agent
    import agent.sat_runner as runner_module

    agent = Agent(sat_config)
    agent.work_dir = sat_config.work_dir
    events = []

    class Client:
        connected = True

        async def send_message(self, message):
            if message["type"] == "test_suite_log":
                return await agent.log_delivery.enqueue(message)
            events.append(message)
            return True

    agent.ws_client = Client()
    spool = LogSpool(tmp_path / "full-cancel.sqlite", max_bytes=16384, max_records=1)
    agent.log_delivery = LogDelivery(spool, agent.ws_client, logger, retry_seconds=0.01)
    agent.log_delivery.negotiate(dict(capabilities=["log_batch_v1"]))
    # The initial execution log fills the spool; subprocess output blocks on its
    # next enqueue while the receiver is occupied processing cancel.
    monkeypatch.setattr(
        runner_module,
        "build_invocation",
        lambda *_: (
            [
                sys.executable,
                "-c",
                "import time;print('blocked-output',flush=True);time.sleep(60)",
            ],
            __import__("os").environ.copy(),
        ),
    )
    message = dict(
        suite_id="suite-0",
        execution_id="cancel-full",
        case_ids=["case-0"],
        case_codes=["CODE"],
        execution_command="xat --mode offline",
    )
    agent.sat_runner.start(message)
    for _ in range(100):
        if (
            spool.usage()["records"] == 1
            and (
                agent.work_dir / "suites/suite-0/executions/cancel-full/output.log"
            ).exists()
        ):
            break
        await asyncio.sleep(0.01)
    assert spool.usage()["records"] == 1
    await asyncio.wait_for(
        agent.on_message(
            dict(
                type="cancel_test_suite", suite_id="suite-0", execution_id="cancel-full"
            )
        ),
        3,
    )
    terminal = [e for e in events if e["type"] == "test_suite_completed"]
    assert terminal and terminal[-1]["status"] == "cancelled"
    assert (
        spool.usage()["records"] == 1
    ), "control completion must not silently evict evidence"
    # Only now can the receiver handle the ACK. It must remain valid and drain.
    await agent.on_message(
        dict(type="log_batch_ack", stream_id=spool.stream_id, through_sequence=1)
    )
    assert spool.usage()["records"] == 0
    assert not agent.execution_admission.tickets and not agent.sat_runner.runs
    await agent.log_delivery.close()


@pytest.mark.asyncio
async def test_raw_stdout_fragments_preserve_every_character(plan_lab, tmp_path):
    db, _ = plan_lab
    add_task(db)
    spool = LogSpool(tmp_path / "raw.sqlite")
    delivery = LogDelivery(spool, SimpleNamespace(connected=False), logger)
    fragments = [
        "prefix no newline ",
        "😀\rprogress\r",
        "  whitespace\n\n",
        "x" * 9000,
        "tail",
    ]
    for text in fragments:
        await delivery.enqueue(payload(text, raw=True))
    while spool.usage()["records"]:
        current = spool.batch()
        response, _ = persist_log_batch(db, "node", current)
        assert response["type"] == "log_batch_ack"
        spool.acknowledge(response["through_sequence"])
    assert db.query(SuiteLog.message).scalar() == "".join(fragments)
    await delivery.close()


@pytest.mark.asyncio
async def test_sat_real_stdout_utf8_boundary_and_whitespace(sat_config, monkeypatch):
    import sys
    from agent.sat_runner import SATRunner
    import agent.sat_runner as runner_module

    events = []

    class Client:
        async def send_message(self, message):
            events.append(message)
            return True

    expected = " " * 4095 + "😀trail  \n\n"
    monkeypatch.setattr(
        runner_module,
        "build_invocation",
        lambda *_: (
            [
                sys.executable,
                "-c",
                "import os; os.write(1," + repr(expected.encode()) + ")",
            ],
            __import__("os").environ.copy(),
        ),
    )
    runner = SATRunner(
        SimpleNamespace(
            work_dir=sat_config.work_dir, config=sat_config, ws_client=Client()
        )
    )
    await runner.execute(
        dict(
            suite_id="suite-0",
            execution_id="utf8-real",
            case_ids=["case-0"],
            case_codes=["CODE"],
            execution_command="xat --mode offline",
        )
    )
    text = "".join(
        e["message"] for e in events if e["type"] == "test_suite_log" and e.get("raw")
    )
    assert text == expected and "�" not in text
    assert (
        sat_config.work_dir / "suites/suite-0/executions/utf8-real/output.log"
    ).read_text() == expected


def test_binary_nul_explicitly_nacks_instead_of_corrupting_text_offsets(plan_lab):
    db, _ = plan_lab
    add_task(db)
    response, _ = persist_log_batch(db, "node", batch("prefix\0tail"))
    assert response["reason"] == "unsupported_nul"
    assert db.query(SuiteLog).count() == 0 and db.query(AgentLogCursor).count() == 0


@pytest.mark.asyncio
async def test_nul_mixed_batch_retained_and_visible_diagnostic_is_not_spammed(
    plan_lab, tmp_path
):
    from models.notification import Notification

    db, _ = plan_lab
    add_task(db)
    spool = LogSpool(tmp_path / "rejected.sqlite")
    delivery = LogDelivery(spool, SimpleNamespace(connected=False), logger)
    await delivery.enqueue(payload("valid before invalid"))
    await delivery.enqueue(payload("😀before\0after", raw=True))
    current = spool.batch()
    for _ in range(2):
        response, _ = persist_log_batch(db, "node", current)
        delivery.acknowledge(response)
    assert response["reason"] == "unsupported_nul"
    assert db.query(SuiteLog).count() == db.query(AgentLogCursor).count() == 0
    assert (
        spool.usage()["records"] == 2 and delivery.blocked_reason == "unsupported_nul"
    )
    notification = db.query(Notification).one()
    assert notification.user_id == "owner" and "unsupported_nul" in notification.content
    await delivery.close()


@pytest.mark.asyncio
async def test_terminal_result_outbox_carries_log_backpressure_diagnostic(
    tmp_path, sat_config
):
    from agent.sat_runner import SATRunner

    events = []

    class Client:
        connected = False

        async def send_message(self, message):
            events.append(message)
            return False

    client = Client()
    spool = LogSpool(tmp_path / "terminal.sqlite", max_bytes=16384, max_records=1)
    delivery = LogDelivery(spool, client, logger)
    await delivery.enqueue(payload("retained"))
    blocked = asyncio.create_task(delivery.enqueue(payload("waiting")))
    await asyncio.sleep(0.02)
    agent = SimpleNamespace(
        work_dir=sat_config.work_dir,
        ws_client=client,
        config=sat_config,
        log_delivery=delivery,
    )
    runner = SATRunner(agent)
    await asyncio.wait_for(
        runner.deliver(
            dict(
                type="test_suite_completed",
                suite_id="suite-0",
                execution_id="exec",
                status="failed",
                message="timeout",
            )
        ),
        0.5,
    )
    saved = json.loads(next(runner.outbox.glob("*.json")).read_text())
    assert saved["log_delivery"]["backpressured"] is True
    assert "spool_quota_backpressure" in saved["message"]
    blocked.cancel()
    await asyncio.gather(blocked, return_exceptions=True)
    await delivery.close()


@pytest.mark.asyncio
async def test_large_enqueue_yields_to_control_loop(tmp_path):
    spool = LogSpool(tmp_path / "cooperative.sqlite")
    delivery = LogDelivery(spool, SimpleNamespace(connected=False), logger)
    control = []

    async def heartbeat():
        await asyncio.sleep(0)
        control.append(spool.usage()["records"])

    pulse = asyncio.create_task(heartbeat())
    await delivery.enqueue(payload("x" * 100000))
    await pulse
    assert 0 < control[0] < spool.usage()["records"]
    await delivery.close()


@pytest.mark.parametrize("status", ["completed", "cancelled", "failed"])
def test_delayed_logs_after_terminal_result_still_persist_and_ack(plan_lab, status):
    db, _ = plan_lab
    add_task(db)
    db.query(TaskQueue).filter_by(id="task").update(dict(status=status))
    db.commit()
    message = batch("delayed after terminal")
    first, _ = persist_log_batch(db, "node", message)
    replay, deltas = persist_log_batch(db, "node", message)
    assert first == replay and first["type"] == "log_batch_ack" and deltas == []
    assert db.query(SuiteLog.message).scalar() == "delayed after terminal"


def test_local_log_file_count_quota_bounds_tiny_file_growth(tmp_path):
    from agent.bounded_output import append_local_log, LocalLogQuotaExceeded

    append_local_log(tmp_path / "one.log", "x", max_files=1)
    with pytest.raises(LocalLogQuotaExceeded):
        append_local_log(tmp_path / "two.log", "x", max_files=1)
    assert [p.name for p in tmp_path.glob("*.log")] == ["one.log"]

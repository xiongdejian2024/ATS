"""One event-loop-local capacity gate for every Agent runner.

Admission precedes coroutine startup, so duplicate messages in the same receive
turn cannot start two workloads. Waiting/cancelled work never consumes a slot;
an admitted slot is released only after runner cleanup/finalization returns.
"""

import asyncio
import json
import os
import re
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Ticket:
    exclusive_key: str | None = None
    ready: asyncio.Event = field(default_factory=asyncio.Event)
    admitted: bool = False
    cancelled: bool = False


class ExecutionAdmission:
    def __init__(self, capacity, agent=None):
        self.agent = agent
        self.capacity = max(1, int(capacity or 1))
        self.tickets = {}
        self.seen = set()
        self.closed = False

    def _marker(self, execution_id):
        if not isinstance(execution_id, str) or not re.fullmatch(
            r"[a-zA-Z0-9_-]{1,128}", execution_id
        ):
            raise ValueError("执行ID无效")
        work_dir = getattr(self.agent, "work_dir", None)
        return (
            Path(work_dir) / "execution-admission" / (execution_id + ".json")
            if work_dir
            else None
        )

    def _persist(self, execution_id, state):
        marker = self._marker(execution_id)
        if marker is None:
            return True
        marker.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            return False
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            json.dump({"execution_id": execution_id, "state": state}, output)
            output.flush()
            os.fsync(output.fileno())
        return True

    def register(self, execution_id, *, exclusive_key=None):
        if not execution_id or execution_id in self.seen or self.closed:
            return False
        if not self._persist(execution_id, "accepted"):
            return False
        self.seen.add(execution_id)
        self.tickets[execution_id] = Ticket(exclusive_key)
        self._pump()
        return True

    def _pump(self):
        active = [ticket for ticket in self.tickets.values() if ticket.admitted]
        slots = self.capacity - len(active)
        exclusive = {ticket.exclusive_key for ticket in active if ticket.exclusive_key}
        for ticket in self.tickets.values():
            if slots <= 0 or self.closed:
                break
            if ticket.admitted or ticket.cancelled or ticket.exclusive_key in exclusive:
                continue
            ticket.admitted = True
            ticket.ready.set()
            slots -= 1
            if ticket.exclusive_key:
                exclusive.add(ticket.exclusive_key)

    async def wait(self, execution_id):
        ticket = self.tickets[execution_id]
        await ticket.ready.wait()
        return not ticket.cancelled

    def cancel_waiting(self, execution_id):
        ticket = self.tickets.get(execution_id)
        if ticket and not ticket.admitted:
            ticket.cancelled = True
            ticket.ready.set()

    def release(self, execution_id):
        self.tickets.pop(execution_id, None)
        # Disk markers remain the deduplication authority across reconnects and
        # restarts. Keep only active IDs in memory when that evidence is present;
        # embedders without a workspace still need the in-memory tombstone.
        try:
            marker = self._marker(execution_id)
            if marker is not None and marker.is_file():
                self.seen.discard(execution_id)
        except OSError:
            pass  # Uncertain disk evidence must not permit duplicate execution.
        self._pump()

    def cancel_unknown_suite(self, suite_id, execution_id):
        """Prove this work never started, then persist a no-execute tombstone.

        Old Agent workspaces predate admission markers: an existing execution
        directory or legacy selection file could belong to a surviving child.
        Ambiguous/unreadable evidence remains uncertain and is never ACKed.
        """
        if execution_id in self.seen or execution_id in self.tickets:
            return False
        if not isinstance(suite_id, str) or not re.fullmatch(
            r"[a-zA-Z0-9_-]{1,36}", suite_id
        ):
            return False
        marker = self._marker(execution_id)
        if marker is None:
            return False
        if marker.exists():
            try:
                return (
                    json.loads(marker.read_text())["state"] == "cancelled-before-start"
                )
            except (ValueError, KeyError, OSError):
                return False
        directory = Path(self.agent.work_dir) / "suites" / suite_id
        if (directory / "executions" / execution_id).exists():
            return False
        # Legacy runs share a workspace and can overwrite/omit the selection
        # file. Any legacy artifact is ambiguous, even if its ID differs.
        try:
            if directory.exists() and any(
                child.name != "executions" for child in directory.iterdir()
            ):
                return False
        except OSError:
            return False
        if not self._persist(execution_id, "cancelled-before-start"):
            return False
        # The marker must also block a delayed execute after restart/ACK removal.
        return True

    def close(self):
        self.closed = True
        for execution_id in list(self.tickets):
            self.cancel_waiting(execution_id)


def admission_for(agent):
    # Lightweight runner tests/embedders also share the same gate without
    # requiring a concrete Agent or silently bypassing the configured limit.
    if not hasattr(agent, "execution_admission"):
        agent.execution_admission = ExecutionAdmission(
            getattr(getattr(agent, "config", None), "max_concurrent_tasks", 1),
            agent=agent,
        )
    return agent.execution_admission

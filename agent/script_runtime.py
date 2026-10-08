"""Shared deadlines and nonblocking process I/O for trusted Agent scripts."""

import asyncio
import codecs
import math
import os
import subprocess


def positive_timeout(value):
    """Reject disabled/ambiguous deadlines before starting any subprocess."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("执行超时时间必须为有限正数（秒）")
    try:
        seconds = float(value)
    except (ValueError, OverflowError) as exc:
        raise ValueError("执行超时时间必须为有限正数（秒）") from exc
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("执行超时时间必须为有限正数（秒）")
    return seconds


async def text_chunks(stream):
    """Read bounded chunks without waiting for a newline; preserve split UTF-8."""
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    while chunk := await stream.read(4096):
        text = decoder.decode(chunk)
        if text:
            yield text
    tail = decoder.decode(b"", final=True)
    if tail:
        yield tail


async def stop_script_process(process):
    """Drain abandoned pipes while stopping; a full pipe must not block wait()."""
    try:
        from .sat_runner import terminate_process
    except ImportError:
        from sat_runner import terminate_process

    async def discard(stream):
        while await stream.read(4096):
            pass

    drainers = [asyncio.create_task(discard(stream)) for stream in (process.stdout, process.stderr) if stream]
    try:
        await terminate_process(process)
        try:
            async with asyncio.timeout(1.0):
                await asyncio.gather(*drainers, return_exceptions=True)
        except TimeoutError:
            # A trusted script can explicitly detach a process into another
            # session while it inherits stdout. Such an escaped descriptor must
            # not pin finalization forever. asyncio exposes no public close()
            # on its subprocess Process, so close the transport after the owned
            # process group has been stopped.
            transport = getattr(process, "_transport", None)
            if transport is not None:
                transport.close()
    finally:
        for task in drainers:
            if not task.done():
                task.cancel()
        await asyncio.gather(*drainers, return_exceptions=True)


async def bounded_tail(stream, limit=64 * 1024):
    """Keep a fixed byte tail while continuously draining preparation output."""
    tail = bytearray()
    total = 0
    while chunk := await stream.read(4096):
        total += len(chunk)
        tail.extend(chunk)
        if len(tail) > limit:
            del tail[:-limit]
    omitted = total - len(tail)
    prefix = f"[输出摘要已截断，省略 {omitted} 字节]\n" if omitted else ""
    return prefix + tail.decode("utf-8", "replace")


async def prepare_command(command, *, cwd=None, timeout):
    """Run legacy Git preparation without blocking cancellation or heartbeats."""
    process = None
    readers = []
    try:
        async with asyncio.timeout(positive_timeout(timeout)):
            process = await asyncio.create_subprocess_exec(
                *command, cwd=cwd, stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE, start_new_session=(os.name == "posix"),
            )
            readers = [asyncio.create_task(bounded_tail(stream)) for stream in (process.stdout, process.stderr)]
            stdout, stderr = await asyncio.gather(*readers)
            await process.wait()
            result = subprocess.CompletedProcess(
                command, process.returncode, stdout, stderr,
            )
            result.check_returncode()
            return result
    finally:
        for reader in readers:
            if not reader.done():
                reader.cancel()
        await asyncio.gather(*readers, return_exceptions=True)
        if process is not None:
            await stop_script_process(process)

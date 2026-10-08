"""Bounded result previews and explicitly capped secondary local log copies."""

from pathlib import Path


class OutputTail:
    def __init__(self, max_chars=65536):
        self.max_chars = max_chars
        self.text = ""
        self.total_chars = 0

    def append(self, text):
        self.total_chars += len(text)
        self.text = (self.text + text)[-self.max_chars :]

    def render(self):
        omitted = self.total_chars - len(self.text)
        return (
            f"[Output preview: {omitted} earlier characters omitted; use execution logs for retained evidence]\n"
            if omitted
            else ""
        ) + self.text


class LocalLogQuotaExceeded(OSError):
    pass


def append_local_log(
    path,
    text,
    max_bytes=16 * 1024 * 1024,
    total_bytes=64 * 1024 * 1024,
    quota_root=None,
    quota_pattern="*.log",
    max_files=1024,
):
    """Fail explicitly before writing; never silently rotate away raw evidence.

    Only this directory's *.log files count; caller selects a dedicated directory.
    Reaching quota stops the producer task, allowing an operator to archive files.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    current = path.stat().st_size if path.exists() else 0
    used_bytes = used_files = 0
    for existing in Path(quota_root or path.parent).glob(quota_pattern):
        used_files += 1
        used_bytes += existing.stat().st_size
    if (
        current + len(data) > max_bytes
        or used_bytes + len(data) > total_bytes
        or (not path.exists() and used_files >= max_files)
    ):
        raise LocalLogQuotaExceeded(
            "Local raw log quota reached; task stopped before discarding evidence. Archive retained logs or raise the configured quota."
        )
    with path.open("ab") as output:
        output.write(data)

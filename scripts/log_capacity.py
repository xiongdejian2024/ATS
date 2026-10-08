"""Report global durable log capacity; optionally COPY aged logs to gzip."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-expired", action="store_true", help="Copy aged records; never delete database evidence")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    from database import SessionLocal
    from services.log_archive import ArchivePolicy, capacity, archive_expired
    policy = ArchivePolicy.from_env()
    with SessionLocal() as db:
        report = capacity(db, policy)
        if args.archive_expired:
            report["archives"] = archive_expired(db, policy=policy, limit=args.limit)
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

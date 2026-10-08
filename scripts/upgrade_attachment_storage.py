"""Add database attachment storage without moving or deleting existing files."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    from database import engine
    from models import AttachmentBlob
    from sqlalchemy import inspect
    exists = inspect(engine).has_table(AttachmentBlob.__tablename__)
    print("attachment_blobs: " + ("exists" if exists else "create required"))
    if args.apply:
        AttachmentBlob.__table__.create(engine, checkfirst=True)
        print("Existing attachment paths and bytes preserved")


if __name__ == "__main__": main()

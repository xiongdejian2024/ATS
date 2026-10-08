"""Add the isolated suite dispatch audit table; never rewrite existing queues."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    from database import engine
    from models import SuiteDelivery
    from sqlalchemy import inspect
    exists = inspect(engine).has_table(SuiteDelivery.__tablename__)
    print("suite_deliveries: " + ("exists" if exists else "create required"))
    if args.apply:
        SuiteDelivery.__table__.create(engine, checkfirst=True)
        print("Existing queue, result and log data preserved")


if __name__ == "__main__": main()

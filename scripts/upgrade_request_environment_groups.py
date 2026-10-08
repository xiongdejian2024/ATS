"""Preview an additive environment-group upgrade on the configured ATS database."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    from database import engine
    from migrations.add_request_environment_groups import upgrade

    missing = upgrade(engine, apply=args.apply)
    print(
        ("Created: " if args.apply else "Would create: ")
        + (", ".join(missing) or "none")
    )
    print(
        "Existing tables and rows are preserved; no database or credentials are created"
    )


if __name__ == "__main__":
    main()

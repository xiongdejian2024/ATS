"""Preview independent resource-pool tables on the existing ATS database."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    from database import engine
    from migrations.add_global_resource_pools import upgrade

    missing = upgrade(engine, apply=args.apply)
    print(
        ("Created: " if args.apply else "Would create: ")
        + (", ".join(missing) or "none")
    )
    print("No databases, nodes, credentials, roles or permissions are created")


if __name__ == "__main__":
    main()

"""Preview additive defect workspace tables and four permission definitions."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    from database import engine
    from migrations.add_defect_workspace import upgrade

    planned = upgrade(engine, apply=args.apply)
    print(
        ("Created: " if args.apply else "Would create: ")
        + (", ".join(planned) or "none")
    )
    print("Existing users, role grants, defect identities and data are retained")


if __name__ == "__main__":
    main()

"""Inventory abandoned library/plan images, or explicitly copy archives. No deletion."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--archive-expired',action='store_true');parser.add_argument('--limit',type=int,default=100);args=parser.parse_args()
    from database import SessionLocal
    from services.evidence_archive import inventory,archive_expired
    with SessionLocal() as db:
        print(json.dumps(archive_expired(db,limit=args.limit) if args.archive_expired else inventory(db),ensure_ascii=False))
if __name__=='__main__':main()

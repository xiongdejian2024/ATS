"""Preview/create only shared-library tables. Does not move or remove any files."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    from database import engine
    from models import LibraryFolder,LibraryFile,LibraryReference
    from sqlalchemy import inspect
    for model in [LibraryFolder,LibraryFile,LibraryReference]:
        print(model.__tablename__+': '+('exists' if inspect(engine).has_table(model.__tablename__) else 'create required'))
        if args.apply:model.__table__.create(engine,checkfirst=True)
    print('Existing data/attachments/evidence preserved')
if __name__=='__main__':main()

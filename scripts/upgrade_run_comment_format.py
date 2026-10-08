"""Preview an additive comment format column. Existing text stays plaintext."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))


def upgrade(engine, *, apply=False):
    from sqlalchemy import inspect, text
    if not inspect(engine).has_table('plan_run_comments'):
        raise ValueError('Create/upgrade the existing plan workspace schema first')
    if any(c['name']=='content_format' for c in inspect(engine).get_columns('plan_run_comments')):
        return 'exists'
    if engine.dialect.name not in {'sqlite','mysql','postgresql'}:
        raise ValueError('Unsupported database dialect')
    if apply:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE plan_run_comments ADD COLUMN content_format VARCHAR(16) NOT NULL DEFAULT 'plain'"))
        return 'added'
    return 'add required'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    from database import engine
    print('plan_run_comments.content_format: '+upgrade(engine,apply=args.apply))
    print('Existing content is preserved; old comments remain plaintext')


if __name__=='__main__':main()

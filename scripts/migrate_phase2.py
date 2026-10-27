"""python -m scripts.migrate_phase2 --database NAME [--apply]."""
import argparse
import json
import re
from pymongo import MongoClient
from app.config import Settings
from app.migrations import migrate, SCHEMAS


def main():
    parser=argparse.ArgumentParser(description='Additive phase-two migration; default only prints plan without DB connection.')
    parser.add_argument('--database',required=True)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--allow-development',action='store_true',help='Explicitly permit a non-test target; never needed for tests.')
    args=parser.parse_args()
    if not args.apply:
        print(json.dumps({'database':args.database,'action':'plan-only, no connection',
                          'collections':list(SCHEMAS),'legacy_document_updates':0},ensure_ascii=False))
        return
    if not re.fullmatch(r'survey_system_test_[0-9a-f]{32}',args.database) and not args.allow_development:
        parser.error('Non-test database requires explicit --allow-development; no connection made.')
    with MongoClient(Settings().mongo_uri,serverSelectionTimeoutMS=3000) as connection:
        print(json.dumps(migrate(connection[args.database]),ensure_ascii=False))


if __name__=='__main__': main()

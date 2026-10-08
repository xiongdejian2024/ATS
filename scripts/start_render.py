"""Render single-process entrypoint. No credential generation or schema writes."""
import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
os.chdir(root / 'backend')
sys.path.insert(0, str(root / 'backend'))
os.environ['ENVIRONMENT'] = 'production'
os.environ['ATS_REQUIRE_ORIGIN_AUTH'] = 'true'
from config import settings
from core.origin_access import OriginAccessMiddleware

OriginAccessMiddleware(None, required=True, service_key=settings.ATS_ORIGIN_SERVICE_KEY)
if (len(settings.JWT_SECRET_KEY) < 32 or settings.JWT_SECRET_KEY.startswith(('your-', 'REPLACE_'))
        or settings.ATS_ORIGIN_SERVICE_KEY.startswith('REPLACE_')):
    raise SystemExit('Configure independent persistent JWT and origin secrets before starting')
if settings.JWT_SECRET_KEY == settings.ATS_ORIGIN_SERVICE_KEY:
    raise SystemExit('JWT and origin service secrets must be independent')
if not settings.DATABASE_URL.startswith(('postgresql', 'postgres:')) or not settings.DATABASE_SCHEMA:
    raise SystemExit('Render requires configured PostgreSQL and a dedicated ATS schema')
import uvicorn
uvicorn.run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT', '17400')),
            workers=1, access_log=False, log_level='warning')

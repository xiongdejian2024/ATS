import base64
import gzip
import hashlib
import json
from datetime import datetime,timezone,timedelta
import pytest
from models import LibraryFile,LibraryReference,AttachmentBlob
from services.evidence_archive import inventory,archive_expired,archive_binary
from services.log_archive import ArchivePolicy
from test_file_library import library,upload
from test_case_features import features
from test_case_governance import governance


def test_expired_inventory_retains_inactive_historical_refs_and_copies_atomically(library,tmp_path):
    g=library;orphan=upload(g);linked=upload(g)
    db=g['db'];old=datetime.now(timezone.utc)-timedelta(days=40)
    for item in db.query(LibraryFile):item.created_at=old
    db.add(LibraryReference(file_id=linked['id'],entity_kind='case',entity_id=g['cases'][0].id,created_by=g['users'][0].id,active=False));db.commit()
    policy=ArchivePolicy(enabled=True,directory=str(tmp_path))
    stats=inventory(db,policy);assert stats['expiredUnreferenced']['library']['records']==1 and not stats['automaticDeletion']
    result=archive_expired(db,policy);assert len(result['files'])==1 and result['sourceRowsPreserved']
    with gzip.open(result['files'][0],'rt') as source:lines=[json.loads(line) for line in source]
    raw=b''.join(base64.b64decode(line['base64']) for line in lines if line['type']=='chunk')
    assert raw==b'synthetic evidence' and lines[-1]['sha256']==hashlib.sha256(raw).hexdigest()
    assert db.query(LibraryFile).count()==2 and db.query(AttachmentBlob).count()==2 and db.query(LibraryReference).count()==1
    assert archive_expired(db,ArchivePolicy(enabled=True,directory=str(tmp_path),max_archive_bytes=1))['quotaReached']
    with pytest.raises(ValueError,match='disabled'):archive_expired(db,ArchivePolicy(directory=str(tmp_path)))


def test_archive_failure_preserves_previous_artifact(tmp_path,monkeypatch):
    path=archive_binary(tmp_path,'library','synthetic',{},b'original')
    before=open(path,'rb').read()
    def fail(*args):raise OSError('synthetic disk failure')
    monkeypatch.setattr('services.evidence_archive.os.replace',fail)
    with pytest.raises(OSError):archive_binary(tmp_path,'library','synthetic',{},b'retry')
    assert open(path,'rb').read()==before and not list(tmp_path.glob('.evidence-*'))


def test_old_plan_image_copy_is_bounded_and_preserves_source(library,tmp_path,monkeypatch):
    from models import TestPlan as Plan
    from models.plan_case_media import PlanCaseMedia
    from config import settings
    g=library;db=g['db'];db.add(Plan(id='synthetic-plan',project_id=g['project'].id,owner_id=g['users'][0].id,name='archive check',plan_number='ARCHIVE-001'));db.flush()
    row=PlanCaseMedia(id='synthetic-image',plan_id='synthetic-plan',uploaded_by=g['users'][0].id,file_name='old.png',file_size=4,mime_type='image/png',content=b'1234',created_at=datetime.now(timezone.utc)-timedelta(days=40));db.add(row);db.commit()
    policy=ArchivePolicy(enabled=True,directory=str(tmp_path))
    assert inventory(db,policy)['expiredUnreferenced']['plan-image']['records']==1
    assert len(archive_expired(db,policy)['files'])==1 and db.get(PlanCaseMedia,row.id).content==b'1234'
    monkeypatch.setattr(settings,'MAX_FILE_SIZE',3)
    with pytest.raises(ValueError,match='per-file'):archive_expired(db,policy)
    row.file_size=2;db.commit()
    with pytest.raises(ValueError,match='metadata'):archive_expired(db,policy)

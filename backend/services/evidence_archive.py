"""Bounded inventory and copy-only archive for abandoned evidence; never purge."""
import base64
import gzip
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from sqlalchemy import func
from models.file_library import LibraryFile, LibraryReference
from models.plan_case_media import PlanCaseMedia, PlanCaseMediaLink
from services.file_library import download, data
from services.log_archive import ArchivePolicy
from config import settings


def policy_from_env():
    flag=os.environ.get('ATS_EVIDENCE_ARCHIVE_ENABLED','false').lower()
    if flag not in {'true','false'}:raise ValueError('ATS_EVIDENCE_ARCHIVE_ENABLED must be true or false')
    return ArchivePolicy(enabled=flag=='true',retention_days=int(os.environ.get('ATS_EVIDENCE_RETENTION_DAYS','30')),max_archive_bytes=int(os.environ.get('ATS_EVIDENCE_ARCHIVE_MAX_BYTES',str(1024**3))),directory=os.environ.get('ATS_EVIDENCE_ARCHIVE_DIR',''))


def queries(db,cutoff):
    # Inactive case associations are historical references too, not orphans.
    library=db.query(LibraryFile).filter(LibraryFile.created_at<cutoff,~db.query(LibraryReference.id).filter(LibraryReference.file_id==LibraryFile.id).exists())
    images=db.query(PlanCaseMedia).filter(PlanCaseMedia.created_at<cutoff,~db.query(PlanCaseMediaLink.media_id).filter(PlanCaseMediaLink.media_id==PlanCaseMedia.id).exists())
    return [('library',LibraryFile,library),('plan-image',PlanCaseMedia,images)]


def inventory(db,policy=None,now=None):
    policy=policy or policy_from_env();cutoff=(now or datetime.now(timezone.utc))-timedelta(days=policy.retention_days)
    items={}
    for kind,model,query in queries(db,cutoff):
        count,size=query.with_entities(func.count(model.id),func.coalesce(func.sum(model.file_size),0)).one()
        items[kind]=dict(records=count,bytes=int(size))
    return dict(expiredUnreferenced=items,retentionDays=policy.retention_days,archiveEnabled=policy.enabled,automaticDeletion=False,sourceRowsPreserved=True,externalUntrackedObjects='not inventoried; no bucket listing or deletion')


def archive_binary(directory,kind,identifier,metadata,raw):
    target=directory/(kind+'-'+hashlib.sha256(identifier.encode()).hexdigest()+'.jsonl.gz')
    descriptor,temporary=tempfile.mkstemp(dir=directory,prefix='.evidence-')
    try:
        with os.fdopen(descriptor,'wb') as output:
            with gzip.GzipFile(fileobj=output,mode='wb',mtime=0) as zipped:
                zipped.write((json.dumps(dict(type='metadata',kind=kind,id=identifier,metadata=metadata),ensure_ascii=False,default=str)+'\n').encode())
                for offset in range(0,len(raw),65536):
                    zipped.write((json.dumps(dict(type='chunk',offset=offset,base64=base64.b64encode(raw[offset:offset+65536]).decode()))+'\n').encode())
                zipped.write((json.dumps(dict(type='footer',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))+'\n').encode())
            output.flush();os.fsync(output.fileno())
        os.replace(temporary,target)
        descriptor=os.open(directory,os.O_RDONLY)
        try:os.fsync(descriptor)
        finally:os.close(descriptor)
    except BaseException:
        Path(temporary).unlink(missing_ok=True);raise
    return str(target)


def archive_expired(db,policy=None,now=None,limit=100):
    policy=policy or policy_from_env()
    if not policy.enabled:raise ValueError('Evidence archival is disabled')
    if not policy.directory:raise ValueError('Evidence archive directory is required')
    if type(limit) is not int or not 1<=limit<=1000:raise ValueError('Evidence archive limit must be 1..1000')
    directory=Path(policy.directory).resolve();directory.mkdir(parents=True,exist_ok=True)
    cutoff=(now or datetime.now(timezone.utc))-timedelta(days=policy.retention_days)
    output=[];used=0
    for kind,model,query in queries(db,cutoff):
        # IDs and size only first; avoid materializing an unbounded blob selection.
        for identifier,size in query.with_entities(model.id,model.file_size).order_by(model.created_at,model.id).limit(limit-len(output)):
            if used+size>policy.max_archive_bytes:return dict(files=output,bytes=used,quotaReached=True,sourceRowsPreserved=True)
            if size>settings.MAX_FILE_SIZE:raise ValueError('Evidence exceeds current per-file bound')
            if kind=='library':
                row=db.get(model,identifier)
                if row is None:continue
                raw=download(db,row).body;metadata=dict(data(row),projectId=row.project_id)
            else:
                row=db.query(model.plan_id,model.uploaded_by,model.file_name,model.mime_type,model.created_at,func.substr(model.content,1,settings.MAX_FILE_SIZE+1)).filter(model.id==identifier).first()
                if row is None:continue
                raw=bytes(row[5]);metadata=dict(planId=row.plan_id,uploadedBy=row.uploaded_by,fileName=row.file_name,mimeType=row.mime_type,createdAt=row.created_at)
                if len(raw)!=size or len(raw)>settings.MAX_FILE_SIZE:raise ValueError('Evidence size disagrees with saved metadata')
            metadata['archivedAt']=datetime.now(timezone.utc).isoformat()
            output.append(archive_binary(directory,kind,identifier,metadata,raw));used+=len(raw)
            if len(output)>=limit:return dict(files=output,bytes=used,quotaReached=False,sourceRowsPreserved=True)
    return dict(files=output,bytes=used,quotaReached=False,sourceRowsPreserved=True)

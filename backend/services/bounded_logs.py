"""日志视窗只从数据库读取尾部；完整日志不被裁剪或加载到视窗查询中。"""
from datetime import date, datetime
from sqlalchemy import func
from models.test_suite import TestSuiteLog
from utils.serializer import serialize_model, to_camel_case

MAX_LOG_RECORDS = 20
MAX_LOG_CHARS = 32768


def log_window(query, skip, limit, tail_chars=None, latest=False):
    total = query.count()
    if tail_chars is not None:
        limit = min(limit, MAX_LOG_RECORDS)
    order = [TestSuiteLog.timestamp.desc(), TestSuiteLog.id.desc()] if latest else [TestSuiteLog.timestamp.asc(), TestSuiteLog.id.asc()]
    query = query.order_by(*order).offset(skip).limit(limit)
    if tail_chars is None:
        items = [serialize_model(row) for row in query.all()]
    else:
        # 避免ORM序列化触发完整message的惰性加载；SQLite/MySQL均支持substr和char_length。
        length = func.length(TestSuiteLog.message) if query.session.bind.dialect.name == 'sqlite' else func.char_length(TestSuiteLog.message)
        columns = [c for c in TestSuiteLog.__table__.columns if c.name != 'message']
        rows = query.with_entities(*columns, func.substr(TestSuiteLog.message, -tail_chars).label('message'), length.label('total_chars')).all()
        items = []
        for row in rows:
            item = {to_camel_case(key): value.isoformat() if isinstance(value, (date, datetime)) else value for key, value in row._mapping.items()}
            item['truncated'] = item['totalChars'] > len(item['message'])
            items.append(item)
    if latest:
        items.reverse()
    return dict(items=items, total=total, skip=skip, limit=limit)


def live_log_window(log_entry, message):
    """位置以Unicode字符计数；前端用它合并历史快照和实时消息。"""
    return dict(id=log_entry.id, message=message[-MAX_LOG_CHARS:], timestamp=log_entry.timestamp.isoformat(),
                execution_id=log_entry.execution_id, endOffset=len(log_entry.message), truncated=len(message) > MAX_LOG_CHARS)


def log_metadata_query(db):
    """History/status queries must not materialize the potentially huge body."""
    from sqlalchemy.orm import defer
    return db.query(TestSuiteLog).options(defer(TestSuiteLog.message, raiseload=True))

"""No controller connection, paths, extensions, writes or unbounded SQLite work."""
import asyncio
import json
import math
import sqlite3
import threading
import time
from .extractions import render_value

FUNCTIONS={'abs','length','lower','upper','coalesce','ifnull','nullif','trim','ltrim','rtrim','substr','substring','count','sum','avg','min','max','round','total','typeof','quote','json_extract','json_array_length'}


def query(processor, parameters, stop):
    connection=sqlite3.connect(':memory:')
    try:
        connection.setlimit(sqlite3.SQLITE_LIMIT_LENGTH,65536)
        connection.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH,8192)
        connection.setlimit(sqlite3.SQLITE_LIMIT_COLUMN,50)
        connection.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH,50)
        connection.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT,10)
        connection.setlimit(sqlite3.SQLITE_LIMIT_ATTACHED,0)
        for table in processor.tables:
            columns=','.join('"'+c.name+'" '+c.type for c in table.columns)
            connection.execute('CREATE TABLE "'+table.name+'" ('+columns+')')
            placeholders=','.join('?' for c in table.columns)
            connection.executemany('INSERT INTO "'+table.name+'" VALUES ('+placeholders+')',[[r[c.name] for c in table.columns] for r in table.rows])
        connection.commit()
        deadline=time.monotonic()+processor.timeoutMs/1000
        operations=0
        def progress():
            nonlocal operations
            operations+=1000
            return int(stop.is_set() or time.monotonic()>=deadline or operations>1000000)
        connection.set_progress_handler(progress,1000)
        def authorize(action,arg1,arg2,db_name,trigger):
            if action==sqlite3.SQLITE_FUNCTION:
                return sqlite3.SQLITE_OK if str(arg2).lower() in FUNCTIONS else sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK if action in {sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_RECURSIVE} else sqlite3.SQLITE_DENY
        connection.set_authorizer(authorize)
        cursor=connection.execute(processor.query,parameters)
        if not cursor.description:raise ValueError('SQL处理器只接受只读查询')
        columns=[c[0] for c in cursor.description]
        if len(columns)!=len(set(columns)) or any(len(c)>255 for c in columns):raise ValueError('SQL结果列重复或过长')
        rows, size = [], 2
        for values in cursor:
            if len(rows)>=processor.maxRows:raise ValueError('SQL结果超过行数限制')
            row = dict(zip(columns, values))
            size += len(json.dumps(row,ensure_ascii=False,allow_nan=False).encode()) + (1 if rows else 0)
            if size > 65536:raise ValueError('SQL结果超过64KiB')
            rows.append(row)
        return rows
    finally:connection.close()


async def execute(processor, variables, temporary):
    parameters=render_value(processor.parameters,variables)
    stop=threading.Event()
    task=asyncio.create_task(asyncio.to_thread(query,processor,parameters,stop))
    try:
        rows=await asyncio.wait_for(asyncio.shield(task),(processor.timeoutMs+200)/1000)
    except (asyncio.CancelledError,asyncio.TimeoutError):
        stop.set()
        try:await asyncio.shield(task)
        except Exception:pass
        raise
    updates={}
    for binding in processor.bindings:
        if binding.row>=len(rows) or binding.column not in rows[binding.row]:raise ValueError('SQL绑定结果不存在')
        value=rows[binding.row][binding.column]
        updates[binding.name]='' if value is None else str(value)
    combined={**variables,**updates}
    if len(combined)>10000 or sum(len(k.encode())+len(v.encode()) for k,v in combined.items())>8*1024*1024:
        raise ValueError('SQL变量超过执行容量')
    variables.update(updates);temporary.update(updates)
    return dict(rowCount=len(rows),bindings=[dict(name=k,value=v[:4096],truncated=len(v)>4096) for k,v in updates.items()])

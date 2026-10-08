"""Execute a bounded ordered list inside the already-owned parent run."""
import asyncio
import logging
import time
from .sql_runtime import execute as execute_sql

logger=logging.getLogger('XAT原生处理器')


async def evaluate(phase, processors, variables, temporary, *, hook_executor=None, skip_reason=None):
    rows=[]
    failed=False
    for processor in processors:
        row=dict(id=processor.id,name=processor.name,type=processor.type,phase=phase,result='skipped',durationMs=0,error=None,rowCount=None,bindings=[])
        if skip_reason or failed or not processor.enable:
            row['error']=skip_reason or ('前序处理器失败' if failed else '处理器已停用')
        else:
            started=time.monotonic()
            try:
                if processor.type == 'sql':
                    result=await execute_sql(processor,variables,temporary)
                else:
                    if hook_executor is None: raise ValueError('当前执行器未提供脚本钩子')
                    result=await hook_executor(processor)
                row.update(result,result='passed')
            except asyncio.CancelledError:raise
            except Exception as error:
                logger.exception('原生处理器失败：阶段=%s，处理器=%s',phase,processor.id)
                row.update(result='error',error='处理器执行失败：'+type(error).__name__)
                failed=True
            row['durationMs']=(time.monotonic()-started)*1000
        rows.append(row)
    return rows, not failed

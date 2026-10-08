"""A native script hook uses its parent's slot, process cleanup and durable log ID."""
import asyncio
import os
import sys
from pathlib import Path
try:
    from .script_job_runner import validate_config
    from .task_executor import TaskExecutor
except ImportError:
    from script_job_runner import validate_config
    from task_executor import TaskExecutor


async def execute(runner, message, hook, directory):
    mode,source,command,args,relative,timeout=validate_config(hook.config.model_dump())
    if hook.config.environmentId != runner.agent.environment_id:
        raise ValueError('脚本钩子不能转移到其他节点')
    root=Path(runner.agent.work_dir).resolve()
    directory=Path(directory).resolve()
    directory.relative_to(root)
    directory.mkdir(parents=True,exist_ok=True)
    cwd=(root/relative).resolve() if relative else directory
    cwd.relative_to(root)
    cwd.mkdir(parents=True,exist_ok=True)
    if mode!='command':
        filename=directory/('hook.py' if mode=='python' else 'hook.cmd' if os.name=='nt' else 'hook.sh')
        with open(filename,'w',encoding='utf-8',newline='',opener=lambda p,f:os.open(p,f,0o600)) as output:
            output.write(source)
        command=([sys.executable,'-u',str(filename)] if mode=='python' else [os.environ.get('COMSPEC','cmd.exe'),'/D','/C',str(filename)] if os.name=='nt' else ['/bin/sh',str(filename)])+args
    else: command=[command,*args]
    async def log(task_id,level,text): await runner.log(message,text,raw=True)
    executor=TaskExecutor(root,on_log=log,logger=runner.agent.logger,
        max_log_bytes=getattr(runner.agent.config,'task_log_max_bytes',16*1024*1024),
        total_log_bytes=getattr(runner.agent.config,'task_logs_total_bytes',64*1024*1024))
    # The parent log spool can wait for an ACK while disconnected. The hook
    # deadline includes that backpressure and cancellation still reaches the
    # executor's process-group cleanup before this context returns.
    async with asyncio.timeout(timeout):
        await runner.log(message,'原生脚本钩子开始：'+hook.id)
        result=await executor.execute_task(dict(task_id=message['execution_id'],command=command,work_dir=str(cwd),timeout=timeout))
        if result['status']=='cancelled': raise asyncio.CancelledError
        if result['status']!='success': raise ValueError('脚本钩子未成功：'+result['status'])
        await runner.log(message,'原生脚本钩子完成：'+hook.id)
    return {}

"""让业务接口按方法加载硬件与平台依赖，保留公共名称和函数实现。"""
import ast
import logging
from pathlib import Path

logger = logging.getLogger('xat.api')


def migrate(path):
    source=path.read_text();tree=ast.parse(source)
    delayed=[]
    for node in tree.body:
        if not isinstance(node,ast.ImportFrom) or not node.module:continue
        if node.module=='groot2' or (node.module.startswith('xat_ecu.legacy.') and '.common.' not in node.module):
            if all(alias.name!='*' for alias in node.names):delayed.append(node)
    names={alias.asname or alias.name:(node.module,alias.name) for node in delayed for alias in node.names}
    lines=source.splitlines(keepends=True); offsets=[0]
    for line in lines:offsets.append(offsets[-1]+len(line))
    edits=[(offsets[n.lineno-1],offsets[n.end_lineno],'') for n in delayed]
    # 同时处理方法内嵌函数；外层方法提供所需对象，内部重复导入不改变行为。
    for node in ast.walk(tree):
        if not isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
        used={n.id for statement in node.body for n in ast.walk(statement) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id in names}
        if not used:continue
        first=node.body[1] if isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str) and len(node.body)>1 else node.body[0]
        indent=' '*first.col_offset
        imports=''.join(indent+'from '+names[name][0]+' import '+names[name][1]+(' as '+name if names[name][1]!=name else '')+'\n' for name in sorted(used))
        edits.append((offsets[first.lineno-1],offsets[first.lineno-1],imports))
    for start,end,value in sorted(edits,reverse=True):source=source[:start]+value+source[end:]
    source='from __future__ import annotations\n'+source
    source+='\n# 保留显式模块属性访问；普通导入不初始化设备或私有服务。\n_DEFERRED_IMPORTS = '+repr(names)+'\n\ndef __getattr__(name):\n    if name not in _DEFERRED_IMPORTS:\n        raise AttributeError(name)\n    from importlib import import_module\n    module, attribute = _DEFERRED_IMPORTS[name]\n    value = getattr(import_module(module), attribute)\n    globals()[name] = value\n    return value\n'
    compile(source,str(path),'exec')
    path.write_text(source)
    logger.info('业务接口延迟导入完成：%s，依赖=%s',path,len(names))


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(message)s')
    root=Path(__file__).resolve().parents[1]/'xat/packages/ecu/src/xat_ecu/api'
    for path in [root/'interface.py',root/'interfaces/dp2/interface.py']:migrate(path)

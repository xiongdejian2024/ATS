"""为迁入的广义异常处理补充堆栈日志，不改变返回与重新抛出行为。"""
import ast
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
logger=logging.getLogger('xat.logging')


def main():
    changed,handlers=0,0
    for root in [ROOT/'xat/packages/ecu/src/xat_ecu',ROOT/'xat/framework/automotive',ROOT/'xat/tools']:
        for path in root.rglob('*.py'):
            if path.stat().st_size>512000 or path.name.endswith('_pb2.py'):continue
            source=path.read_text()
            try:tree=ast.parse(source)
            except SyntaxError:continue
            lines=source.splitlines(keepends=True);offsets=[0]
            for line in lines:offsets.append(offsets[-1]+len(line))
            edits=[]
            for node in ast.walk(tree):
                if not isinstance(node,ast.ExceptHandler):continue
                caught=ast.unparse(node.type) if node.type else ''
                if node.type is not None and 'Exception' not in caught:continue
                if any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and (n.func.attr=='exception' or any(k.arg=='exc_info' and isinstance(k.value,ast.Constant) and k.value.value for k in n.keywords)) for statement in node.body for n in ast.walk(statement)):
                    continue
                first=node.body[0];indent=' '*first.col_offset
                text=indent+'__import__("logging").getLogger(__name__).exception("XAT 捕获异常：'+str(path.relative_to(ROOT)).replace('"','')+'")\n'
                edits.append((offsets[first.lineno-1],text));handlers+=1
            for offset,text in sorted(edits,reverse=True):source=source[:offset]+text+source[offset:]
            if edits:path.write_text(source);changed+=1
    logger.info('广义异常堆栈日志补充完成：文件=%s，处理分支=%s',changed,handlers)


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(message)s')
    main()

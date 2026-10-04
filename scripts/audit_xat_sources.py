"""审计 XAT 迁入源码，结果只记录路径和错误，不执行设备代码。"""
import ast
import json
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger('xat.audit')


def main():
    failures, reverse_imports, missing_imports = [], [], []
    roots = [ROOT / 'xat/packages/ecu/src', ROOT / 'xat/framework/automotive', ROOT / 'xat/cases/src', ROOT / 'xat/tools']
    count = 0
    for root in roots:
        for path in root.rglob('*.py'):
            if '__pycache__' in path.parts:
                continue
            count += 1
            source = path.read_text(encoding='utf-8-sig')
            try:
                compile(source, str(path), 'exec')
            except Exception as exc:
                logger.exception('XAT 源码编译失败：%s', path.relative_to(ROOT))
                failures.append({'路径': str(path.relative_to(ROOT)), '错误': str(exc)})
                continue
            if root.name != 'src' or 'xat_ecu' not in path.parts:
                continue
            if len(source) > 512000:
                continue
            for node in ast.walk(ast.parse(source)):
                modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ''] if isinstance(node, ast.ImportFrom) and not node.level else []
                for module in modules:
                    if module.split('.')[0] in {'pytest', 'allure', 'framework', 'xat_cases', 'sat_framework', 'sdk_interface', 'ecu_simulator', 'automotive_sdk', 'test_case'}:
                        reverse_imports.append({'路径':str(path.relative_to(ROOT)), '模块':module, '行':node.lineno})
                    if module.startswith('xat_ecu.'):
                        local = root / module.replace('.', '/')
                        if not local.with_suffix('.py').is_file() and not local.is_dir():
                            missing_imports.append({'路径':str(path.relative_to(ROOT)), '模块':module, '行':node.lineno})
    report = {'Python文件数':count, '编译失败':failures, '库反向依赖':reverse_imports, '未找到的本地模块':missing_imports}
    (ROOT / 'docs/migration/编译与依赖审计.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    logger.info('审计完成：文件=%s，编译失败=%s，反向依赖=%s，本地缺失=%s', count,len(failures),len(reverse_imports),len(missing_imports))
    return 1 if failures or reverse_imports or missing_imports else 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    raise SystemExit(main())

"""验证安装包独立运行，并阻断旧仓库的导入与文件读取；不执行台架。"""
import argparse
import json
import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger('xat.installation')
ROOT = Path(__file__).resolve().parents[1]

PROGRAM = r'''
import importlib.abc, json, logging, os, sys
from pathlib import Path
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
forbidden = [Path(p).resolve() for p in json.loads(sys.argv[1])]
def audit(event, args):
    if event not in {'open', 'os.listdir', 'os.scandir'} or not args:
        return
    if not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    path = Path(os.fsdecode(args[0])).absolute()
    if any(path == root or root in path.parents for root in forbidden):
        raise AssertionError('读取了旧仓库：' + str(path))
sys.addaudithook(audit)
class BlockOld(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'sat_framework', 'sdk_interface', 'ecu_simulator', 'automotive_sdk', 'test_case', 'dp2'}:
            raise AssertionError('导入了旧模块：' + fullname)
sys.meta_path.insert(0, BlockOld())
import framework, xat_ecu, xat_cases
for module in (framework, xat_ecu, xat_cases):
    assert Path(sys.prefix) in Path(module.__file__).resolve().parents, module.__file__
    logging.info('安装包来源：%s = %s', module.__name__, module.__file__)
from xat_ecu.api import CommonBusComm, CommonSdTest
from xat_ecu.api.config_center.ConfigMasterV2T_pb2 import ConfSyncData
assert ConfSyncData.FromString(ConfSyncData(PbVer='软件验收').SerializeToString()).PbVer == '软件验收'
assert hasattr(CommonBusComm, '__init__') and hasattr(CommonSdTest, '__init__')
from framework.__main__ import main
directory = Path(sys.argv[2])
code = main(['--mode', 'offline', '--output-dir', str(directory)])
rows = json.loads((directory / 'results.json').read_text())
assert code == 0 and len(rows) == 4 and all(row['status'] == 'passed' for row in rows), rows
logging.info('旧仓库不可读验收通过：4 项软件用例，框架/库/用例均来自安装包')
'''


def main(python):
    directory = Path(tempfile.mkdtemp(prefix='xat-installed-'))
    forbidden = [str(ROOT.parent / name) for name in ('sat', 'ecu-simulator')]
    logger.info('验证独立安装环境：%s，输出：%s', python, directory)
    try:
        subprocess.run([str(python), '-I', '-c', PROGRAM, json.dumps(forbidden), str(directory)],
                       cwd=directory, check=True, timeout=60)
    except Exception:
        logger.exception('安装包独立运行验收失败')
        raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('--python', type=Path, required=True)
    # 不解析解释器符号链接：venv 解释器的路径决定虚拟环境归属。
    main(parser.parse_args().python.absolute())

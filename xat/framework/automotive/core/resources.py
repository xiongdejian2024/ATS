"""XAT 自有框架资源与部署命令，不导入或初始化台架设备。"""
import os
import shlex
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from urllib.parse import urlsplit

from framework.integrations.runtime import XAT_ROOT

AUTOMOTIVE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = XAT_ROOT.parent
LOCK_SCRIPT = AUTOMOTIVE_ROOT / 'scripts/resource_lock.sh'


def package_version(name):
    try:
        return version(name)
    except PackageNotFoundError:
        return '0.2.0'


def clone_command(workspace):
    url = os.environ.get('XAT_GIT_URL')
    if not url:
        raise ValueError('缺少 XAT_GIT_URL，请配置 ATS 仓库地址')
    parsed = urlsplit(url)
    if parsed.password:
        raise ValueError('仓库地址不能包含密码，请使用 Git 凭证管理或 SSH')
    return f'git clone --progress {shlex.quote(url)} {shlex.quote(str(Path(workspace) / "ATS"))}'


def install_command(repository):
    # 由使用方提供本机私有平台依赖；只安装 XAT 自有框架、库和用例。
    root = shlex.quote(str(repository))
    return (f'cd {root} && python3 -m venv venv && '
            'venv/bin/python -m pip install -e "./xat[automotive]" '
            '-e "./xat/packages/ecu[can,ssh,serial,security,network,protocols]" '
            '-e ./xat/cases')


def workspace_relative(path):
    return str(Path(path).resolve().relative_to(REPOSITORY_ROOT))

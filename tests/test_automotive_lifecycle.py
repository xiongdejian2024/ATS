"""迁入的 SAT pytest 生命周期在 XAT 中工作，不初始化设备或外部服务。"""
import json
from test_xat_integration import run_xat


def test_migrated_lifecycle_order_and_cleanup_failure(tmp_path):
    source = tmp_path / 'test_hooks.py'
    source.write_text('''
from pathlib import Path
steps = Path("生命周期.log")
def record(value):
    with steps.open("a") as stream: stream.write(value + "\\n")
def before_module(ecu): record("模块前置")
def after_module(ecu): record("模块后置")
class TestLifecycle:
    def before_class_setup(self, ecu): record("类前置")
    def after_class_teardown(self, ecu): record("类后置")
    def before_func_setup(self, ecu): record("函数前置")
    def after_func_teardown(self, ecu):
        record("函数后置")
        raise RuntimeError("迁入框架清理失败")
    def test_caseid_lifecycle(self, ecu):
        record("用例主体")
        assert ecu is not None
''')
    result, rows = run_xat(tmp_path,
        '-p', 'framework.hooks', '-p', 'framework.integrations.plugin',
        '-p', 'framework.automotive.core.framework_base', '--noconftest',
        str(source), native=True)
    assert result.returncode == 1, result.stdout + result.stderr
    assert (tmp_path/'生命周期.log').read_text().splitlines() == [
        '模块前置', '类前置', '函数前置', '用例主体', '函数后置', '类后置', '模块后置']
    assert rows[0]['status'] == 'error'
    assert '迁入框架清理失败' in rows[0]['error']


def test_migrated_pytest_options_parse_without_hardware(tmp_path):
    source = tmp_path / 'test_options.py'
    source.write_text('''def test_caseid_options(pytestconfig):
    assert pytestconfig.getoption("veh_type") == "软件车型"
    assert pytestconfig.getoption("bl_ver") == "软件版本"
''')
    result, rows = run_xat(tmp_path,
        '-p', 'framework.hooks', '-p', 'framework.integrations.plugin',
        '-p', 'framework.automotive.core.framework_base', '--noconftest',
        '--veh_type', '软件车型', '--bl_ver', '软件版本', str(source), native=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert rows[0]['status'] == 'passed'


def test_native_deployment_commands_and_packaged_resources(tmp_path, monkeypatch):
    """只验证生成的命令和包内资源，不运行 SSH、设备锁或安装命令。"""
    import pytest
    from framework.automotive.core.resources import (
        AUTOMOTIVE_ROOT, LOCK_SCRIPT, REPOSITORY_ROOT,
        clone_command, install_command, workspace_relative,
    )
    assert LOCK_SCRIPT.is_file()
    assert (AUTOMOTIVE_ROOT / 'scripts/record_top.sh').is_file()
    assert (AUTOMOTIVE_ROOT / 'scripts/record_vm_stat.sh').is_file()
    monkeypatch.delenv('XAT_GIT_URL', raising=False)
    with pytest.raises(ValueError, match='XAT_GIT_URL'):
        clone_command(tmp_path)
    monkeypatch.setenv('XAT_GIT_URL', 'https://example.invalid/ATS.git')
    command = clone_command(tmp_path / '软件 验收')
    assert 'ATS.git' in command and str(tmp_path / '软件 验收/ATS') in command
    command = install_command(tmp_path)
    assert './xat/packages/ecu[' in command and './xat/cases' in command
    assert 'setupenv.py' not in command and 'sat_framework' not in command
    assert workspace_relative(REPOSITORY_ROOT / 'xat/cases') == 'xat/cases'

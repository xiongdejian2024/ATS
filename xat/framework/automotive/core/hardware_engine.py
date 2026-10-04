#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :framework_base.py
@time         :2/7/24 17:49
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import pytest

from framework.automotive.fixture.fixture_class import Fixtures
from framework.automotive.hook.hook_master import HookMaster
from framework.automotive.hook.hook_non_dist import HookNonDist
from framework.automotive.hook.hook_slave import HookSlave


class FrameworkBase(HookMaster, HookSlave, HookNonDist, Fixtures):
    def __init__(self):
        super().__init__()


fb = None  # 实例由 XAT 会话在明确设备模式下创建。


# ***********************************hook***********************************
def pytest_addoption(parser):
    fb.pytest_addoption(parser)


def pytest_configure(config):
    fb.pytest_configure(config)


def pytest_collection_modifyitems(items):
    if fb.pytest_process.NonDist:
        fb.pytest_collection_modifyitems_for_non_dist(items)
    elif fb.pytest_process.Master:
        fb.pytest_collection_modifyitems_for_master(items)
    elif fb.pytest_process.Slave:
        fb.pytest_collection_modifyitems_for_slave(items)


def pytest_collection_finish(session):
    if fb.pytest_process.Master:
        fb.pytest_collection_finish_for_master(session)
    elif fb.pytest_process.NonDist:
        fb.pytest_collection_finish_for_non_dist(session)
    elif fb.pytest_process.Slave:
        fb.pytest_collection_finish_for_slave(session)


def pytest_runtestloop(session):
    if fb.pytest_process.Slave:
        return fb.pytest_runtestloop(session)


def pytest_unconfigure(config):
    if fb.pytest_process.NonDist:
        fb.pytest_unconfigure_for_non_dist(config)
    elif fb.pytest_process.Slave:
        fb.pytest_unconfigure_for_slave(config)
    elif fb.pytest_process.Master:
        fb.pytest_unconfigure_for_master(config)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if fb.pytest_process.NonDist:
        fb.pytest_terminal_summary_for_non_dist(terminalreporter, exitstatus, config)
    elif fb.pytest_process.Slave:
        fb.pytest_terminal_summary_for_slave(terminalreporter, exitstatus, config)


def pytest_sessionstart(session):
    if fb.pytest_process.NonDist:
        fb.pytest_sessionstart_for_non_dist(session)
    elif fb.pytest_process.Slave:
        fb.pytest_sessionstart_for_slave(session)
    elif fb.pytest_process.Master:
        fb.pytest_sessionstart_for_master(session)


def pytest_runtest_setup(item):
    if fb.pytest_process.NonDist:
        fb.pytest_runtest_setup_for_non_dist(item)
    elif fb.pytest_process.Slave:
        fb.pytest_runtest_setup_for_slave(item)


def pytest_runtest_teardown():
    if fb.pytest_process.NonDist:
        fb.pytest_runtest_teardown_for_non_dist()
    elif fb.pytest_process.Slave:
        fb.pytest_runtest_teardown_for_slave()


def pytest_sessionfinish(session, exitstatus):
    if fb.pytest_process.NonDist:
        fb.pytest_sessionfinish_for_non_dist(session, exitstatus)
    elif fb.pytest_process.Slave:
        fb.pytest_sessionfinish_for_slave(session, exitstatus)
    elif fb.pytest_process.Master:
        fb.pytest_sessionfinish_for_master(session, exitstatus)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    if fb.pytest_process.NonDist:
        out = yield
        report = out.get_result()
        fb.pytest_runtest_makereport_for_non_dist(report, item, call)
    elif fb.pytest_process.Slave:
        out = yield
        report = out.get_result()
        fb.pytest_runtest_makereport_for_slave(report, item, call)


# ***********************************fixture***********************************

@pytest.fixture(scope="session")
def ecu(request):
    return fb.ecu(request)


@pytest.fixture(scope='module', autouse=True)
def case_module_hook(request, ecu):
    if fb.pytest_process.Slave or fb.pytest_process.NonDist:
        fb.case_module_hook(request, ecu)


@pytest.fixture(scope='class', autouse=True)
def case_class_hook(request, ecu):
    if fb.pytest_process.Slave or fb.pytest_process.NonDist:
        fb.case_class_hook(request, ecu)


@pytest.fixture(scope='function', autouse=True)
def case_function_hook(request, ecu):
    if fb.pytest_process.Slave or fb.pytest_process.NonDist:
        fb.case_function_hook(request, ecu)

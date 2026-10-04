#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :message.py
@Time         :2024/10/28 16:31
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
from flask_socketio import emit

from xat_ecu.legacy.common.logger import logger
from framework.automotive.utils.data_type import CaseStatus, SlaveTaskStatus, TaskTarget, PytestSlaveStatus

# 处理消息
"""
task_group_list = [
    {
        'domain': 'two_domain',
        'vehicle': 'Venus',
        'case_dict': {
              "test_case/bgm/VehicleControl/InteriorLight/test_alm.py::TestLightServiceTurnLamp": {
                  "class_case_list": [item],
                  "class_total_time": 1
                  "case_status": 0  # 0-not_start 1-running 2-finished
                  "slave_ip": "xxxx"
              }
        },
        'case_total_time': 1,
        'running_env': 'HIL',
    },
    {
        'domain': 'two_domain',
        'vehicle': 'Venus800v',
        'case_dict': {
              "test_case/bgm/VehicleControl/ChargeLid/test_chrglid_ctrl_abc.py::TestChrglidCtrlAbc": {
                  "class_case_list": [item],
                  "class_total_time": 1
                  "case_status": 0  # 0-not_start 1-running 2-finished
                  "slave_ip": "xxxx"
              }
        },
        'case_total_time': 1,
        'running_env': 'HIL',
    },
]

"""


def check_task_is_done(self, message):
    sid = message.get('sid')
    client_ip = message.get('client_ip')
    domain = message.get('domain')
    running_env = message.get('running_env')
    for task in self.task_group_list:
        case_dict = task.get('case_dict')
        for node_id, case_info in case_dict.items():
            # 如果有case状态是not_start, 则说明case需要被分配
            if all([
                domain == task.get('domain'),
                running_env == task.get('running_env'),
                case_info.get('case_status') == CaseStatus.not_start.value
            ]):
                return
    else:
        logger.info(f"当前{domain} {running_env}的所有任务都已经分配完成, 信息发送给{client_ip}")
        msg = dict(slave_task_status=SlaveTaskStatus.finish.value)
        emit('message', msg, to=sid, json=True)


def apply_case_to_slave(self, message, sid, client_ip):
    for task in self.task_group_list:
        domain = task.get('domain')
        case_dict = task.get('case_dict')
        vehicle = task.get('vehicle')
        running_env = task.get('running_env')
        # 申请用例时,domain,running_env
        if all([
            domain == message.get('domain'),
            running_env == message.get('running_env')
        ]):
            for node_id, case_info in case_dict.items():
                # 未开始状态的case发送给slave
                if case_info.get('case_status') == CaseStatus.not_start.value:
                    msg = dict(
                        class_name=node_id,
                        class_case_list=case_info.get('class_case_list'),
                        vehicle=vehicle,
                    )
                    emit('message', msg, to=sid, json=True)
                    case_info['case_status'] = CaseStatus.running.value  # 更新case状态
                    case_info['slave_ip'] = client_ip  # 记录任务分配的台架ip
                    return


def update_case_status(self, message, client_ip):
    for task in self.task_group_list:
        domain = task.get('domain')
        case_dict = task.get('case_dict')
        vehicle = task.get('vehicle')
        running_env = task.get('running_env')
        if all([
            domain == message.get('domain'),
            running_env == message.get('running_env'),
            vehicle == message.get('vehicle_model'),
        ]):
            class_name = message.get('class_name')
            if case_dict.get(class_name):
                case_dict[class_name].update({
                    'case_status': message.get('task_status'),
                    'slave_ip': client_ip,
                })
            else:
                logger.warning(f'收集的用例中不存在{class_name}')
            return


def handle_pytest_runtestloop(self, message):
    sid = message.get('sid')
    client_ip = message.get('client_ip')
    with self.master_lock:
        self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_runtestloop.value
        if message.get('data') == TaskTarget.apply_case.value:
            check_task_is_done(self, message)
            return apply_case_to_slave(self, message, sid, client_ip)
        elif message.get('data') == TaskTarget.update_case_status.value:
            return update_case_status(self, message, client_ip)
        else:
            logger.warning(f'data:{message.get("data")} is not supported')


def handle_slave_offline(self, message):
    """
    如果slave离线了，需要将对应的case_status置为finished，防止任务重复执行
    离线有两种情况：
    1.进程结束，则缺少这部分的用例执行
    2.网络断开，slave进程没有退出，这种情况重连上来之后可能case已经执行完成，防止用例重复执行
    """
    client_ip = message.get('client_ip')
    with self.master_lock:
        for task in self.task_group_list:
            case_dict = task.get('case_dict')
            for node_id, case_info in case_dict.items():
                # 如果slave断开时，用例未完成，则需要将case_status置为未开始
                if case_info.get('slave_ip') == client_ip and case_info.get('case_status') == CaseStatus.running.value:
                    case_info['case_status'] = CaseStatus.finished.value
                    case_info['slave_ip'] = None
                    break


def handle_pytest_collection_modifyitems(self, message):
    client_ip = message.get('client_ip')
    msg = message.get('msg')
    with self.master_lock:
        logger.info(f'{client_ip} {msg}')
        # self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_collection_modifyitems.value


def handle_pytest_collection_finish(self, message):
    client_ip = message.get('client_ip')
    msg = message.get('msg')
    with self.master_lock:
        logger.info(f'{client_ip} {msg}')
        # self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_collection_finish.value


def handle_pytest_terminal_summary(self, message):
    client_ip = message.get('client_ip')
    msg = message.get('msg')
    with self.master_lock:
        logger.info(f'{client_ip} {msg}')
        self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_terminal_summary.value


def handle_pytest_sessionstart(self, message):
    client_ip = message.get('client_ip')
    msg = message.get('msg')
    with self.master_lock:
        logger.info(f'{client_ip} {msg}')
        self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_sessionstart.value


def handle_pytest_sessionfinish(self, message):
    client_ip = message.get('client_ip')
    msg = message.get('msg')
    exit_code = message.get('exitcode')
    with self.master_lock:
        logger.info(f'{client_ip} {msg}, 返回码: {exit_code}')
        self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_sessionfinish.value


def handle_pytest_runtest_makereport(self, message):
    client_ip = message.get('client_ip')
    data = message.get('data')
    with self.master_lock:
        logger.info(f'{client_ip} {data}')
        self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_runtest_makereport.value


def handle_pytest_unconfigure(self, message):
    client_ip = message.get('client_ip')
    msg = message.get('msg')
    with self.master_lock:
        logger.info(f'{client_ip} {msg}')
        self.pytest_slave_status_dict[client_ip] = PytestSlaveStatus.pytest_unconfigure.value


def handle_start_task(self, message):
    client_ip = message.get('client_ip')
    req = message.get('req')
    domain = req.get('domain')
    running_env = req.get('running_env')
    with self.master_lock:
        if domain and running_env:
            self.add_new_task.append({
                "domain": domain,
                "running_env": running_env,
            })
            logger.info(f'{client_ip}申请了新任务，环境配置为{domain} {running_env}')


def handle_stop_task(self, message):
    sid = message.get('sid')
    socket_io = message.get('socket_io')
    with self.master_lock:
        socket_io.emit('message', 'stop', to=sid)


def list_all_tasks(self, message):
    logger.debug(f"task_group_list:{self.task_group_list}")
    return self.task_group_list


def list_all_slave_status(self, message):
    logger.info(f"pytest_slave_status_dict:{self.pytest_slave_status_dict}")
    return self.pytest_slave_status_dict


message_protocol_dict = {
    PytestSlaveStatus.pytest_runtestloop.value: handle_pytest_runtestloop,
    PytestSlaveStatus.pytest_collection_finish.value: handle_pytest_collection_finish,
    PytestSlaveStatus.pytest_terminal_summary.value: handle_pytest_terminal_summary,
    PytestSlaveStatus.pytest_sessionfinish.value: handle_pytest_sessionfinish,
    PytestSlaveStatus.pytest_sessionstart.value: handle_pytest_sessionstart,
    PytestSlaveStatus.pytest_collection_modifyitems.value: handle_pytest_collection_modifyitems,
    PytestSlaveStatus.pytest_runtest_makereport.value: handle_pytest_runtest_makereport,
    PytestSlaveStatus.pytest_unconfigure.value: handle_pytest_unconfigure,
    PytestSlaveStatus.slave_offline.value: handle_slave_offline,
    PytestSlaveStatus.handle_stop_task.value: handle_stop_task,
    PytestSlaveStatus.handle_start_task.value: handle_start_task,
    PytestSlaveStatus.list_all_tasks.value: list_all_tasks,
    PytestSlaveStatus.list_all_slave_status.value: list_all_slave_status,
}

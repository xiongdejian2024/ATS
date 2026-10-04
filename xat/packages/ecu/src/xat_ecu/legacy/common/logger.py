# -*- coding: utf-8 -*-
"""
@File        : logger.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/2/19 14:49
@Description : 
@Examples    :
"""

import logging
import sys
import os
import datetime


class Logger(object):
    __instance = None

    def __init__(self, log_path='./logs', log_level='INFO', file_log_level='INFO', log_num=10):
        self.log_path = log_path
        self.origin_log_level = log_level
        self.log_num = log_num
        self.log_level = self._get_log_level(self.origin_log_level)
        self.file_log_level = self._get_log_level(file_log_level)
        self._purge_log_file(self.log_num)

    def __new__(cls, log_path='./logs', log_level='INFO', file_log_level='INFO', log_num=10):
        """
        Single instance.
        :param log_path:
        :param log_level:
        :return:
        """
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def get_logger(self, name=''):
        """
        Create a logger instance.
        :param name:
        :return:
        """
        log = logging.getLogger(name)
        log.setLevel(self.file_log_level)
        date_time = datetime.datetime.now()
        log_name = self.log_path + '/test_log_' + \
                   date_time.strftime("%Y_%m_%d_%H_%M_%S_%f") + '.log'

        fh = logging.FileHandler(log_name)
        fh.setLevel(self.file_log_level)

        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        formatter = logging.Formatter(
            '%(asctime)s (%(filename)s:%(lineno)d)' + ' (%(threadName)s:%(process)d)' +
            ' %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        log.addHandler(fh)
        log.addHandler(ch)
        os.environ["LOGGER"] = "logger"    # Avoid repeated printing with the logger in the ecu simulator
        return log

    def _get_log_level(self, log_level):
        if log_level.upper() == 'DEBUG':
            return 'DEBUG'
        elif log_level.upper() == 'INFO':
            return 'INFO'
        elif log_level.upper() == 'WARNING':
            return 'WARNING'
        elif log_level.upper() == 'ERROR':
            return 'ERROR'
        elif log_level.upper() == 'CRITICAL':
            return 'CRITICAL'
        else:
            print('ERROR: Input log_level parameter error: %s' % self.origin_log_level)
            sys.exit(-1)

    def _purge_log_file(self, exp_log_num=10):
        """Keep latest log files according exp_log_num value"""
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        else:
            try:
                log_list = os.listdir(self.log_path)
                log_list = sorted(log_list, key=lambda x:
                            os.path.getmtime(os.path.join(self.log_path, x)))
                log_list.reverse()
                num = 0
                for f in log_list:
                    num += 1
                    if num >= exp_log_num:
                        log_file = self.log_path + '/' + f
                        if os.path.isfile(log_file):
                            os.remove(log_file)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/logger.py")
                print("ERROR: Delete log files failed!!!")
                print(e)


# logger be initialized in conftest.py
logger = logging.getLogger('test')


if __name__ == '__main__':
    pass

# -*- coding: utf-8 -*-
"""
@File        : fixture_base.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/7/11 10:19
@Description : 
@Examples    :
"""

import threading
import time
from pytest import FixtureRequest
import logging
logger = logging.getLogger(__name__)


class FixtureBase(object):
    @staticmethod
    def case_module_hook(request: FixtureRequest, fixture_name: str):
        """
        automatically call `before_module(fixture_name)` and
        `after_module(fixture_name)`
        once call for each module
        """
        if request.module is None:
            return

        ns = '%s.py' % request.module.__name__

        FixtureBase.log_print(1, 'STARTING %s' % ns)
        FixtureBase.fn_call(
            request.module, 'before_module', 'SETUPING', ns, fixture_name
        )

        def module_teardown():
            FixtureBase.fn_call(
                request.module, 'after_module', 'CLEANUPING', ns, fixture_name
            )
            FixtureBase.log_print(1, 'COMPLETED %s' % ns)

        request.addfinalizer(module_teardown)

    @staticmethod
    def case_class_hook(request: FixtureRequest, fixture_name):
        """
        automatically call `before_class(self, fixture_name)` and
        `after_class(self, fixture_name)`
        once call for each class
        """
        if request.cls is None:
            return

        ns = '%s.py::%s' % (request.module.__name__, request.cls.__name__)

        FixtureBase.log_print(1, 'STARTING %s' % ns)

        def cls_teardown():
            try:
                FixtureBase.fn_call(
                    request.cls, 'after_class_teardown', 'CLEANUPING', ns, fixture_name, request.cls
                )
            except Exception as e:
                logger.exception(f"======后置class处理运行失败，请去检查！！！======== 运行失败报错： {e}")
                raise e
            FixtureBase.log_print(1, 'COMPLETED %s' % ns)

        try:
            FixtureBase.fn_call(
                request.cls, 'before_class_setup', 'SETUPING', ns, fixture_name, request.cls
            )
        except Exception as e:
            logger.exception(f"======前置class处理运行失败，请去检查！！！======== 运行失败报错： {e}")
            raise e
        finally:
            thread_list = [thread.name for thread in threading.enumerate()]
            logger.debug(
                "Before class {}, thread list is {}".format(request.cls, thread_list)
            )
            request.addfinalizer(cls_teardown)

    @staticmethod
    def case_function_hook(request: FixtureRequest, fixture_name):
        """
        automatically call `before_each_func(self,fixture_name)` and
        `after_each_func(self,fixture_name)`
        once call for each function
        """
        global fn_name_case
        ns = request.module.__name__ + '.py'

        if request.cls is not None:
            ns = ns + '::' + request.cls.__name__

        fn_name_case = request.function.__name__
        print('\n')
        FixtureBase.log_print(1, 'STARTING %s::%s' % (ns, fn_name_case))
        fn_parent_obj = request.cls
        if request.cls is None:
            fn_parent_obj = request.module

        def func_teardown():
            print('\t')
            try:
                FixtureBase.fn_call(
                    fn_parent_obj,
                    'after_func_teardown',
                    'CLEANUPING',
                    ns,
                    fixture_name,
                    request.instance,
                )
                FixtureBase.log_print(1, 'COMPLETED %s::%s' % (ns, fn_name_case))
            except Exception as e:
                logger.exception(f"======后置func处理运行失败，请去检查！！！======== 运行失败报错： {e}")
                raise e

        try:
            FixtureBase.fn_call(
                fn_parent_obj,
                'before_func_setup',
                'SETUPING',
                ns,
                fixture_name,
                request.instance,
            )
        except Exception as e:
            logger.exception(f"======前置func处理运行失败，请去检查！！！======== 运行失败报错： {e}")
            raise e
        finally:
            request.addfinalizer(func_teardown)

    @staticmethod
    def fn_call(fn_parent_obj, fn_name, action, ns, fixture_name, instance=None):
        fn = getattr(fn_parent_obj, fn_name, None)
        if fn is None:
            return

        FixtureBase.log_print(2, '%s %s::%s' % (action, ns, fn_name))
        if instance is None:
            fn(fixture_name)  # 没有类的情况
        else:
            fn(instance, fixture_name)

    @staticmethod
    def log_print(level, message):
        dim = '=' if level == 1 else '-'
        dim = dim * 60

        logger.info(dim)
        logger.info('    ' + message)
        logger.info(dim)

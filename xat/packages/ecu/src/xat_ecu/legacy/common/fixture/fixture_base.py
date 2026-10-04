# -*- coding: utf-8 -*-
"""
@File        : fixture_base.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/7/11 10:19
@Description : 
@Examples    :
"""


from xat_ecu.legacy.common.logger import logger
import threading
import time


class FixtureBase(object):
    @staticmethod
    def case_module_hook(request, fixture_name):
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
    def case_class_hook(request, fixture_name):
        """
        automatically call `before_class(self, fixture_name)` and
        `after_class(self, fixture_name)`
        once call for each class
        """
        if request.cls is None:
            return

        ns = '%s.py::%s' % (request.module.__name__, request.cls.__name__)

        FixtureBase.log_print(1, 'STARTING %s' % ns)
        FixtureBase.fn_call(
            request.cls, 'before_class_setup', 'SETUPING', ns, fixture_name, request.cls
        )
        thread_list = [thread.name for thread in threading.enumerate()]
        logger.debug(
            "Before class {}, thread list is {}".format(request.cls, thread_list)
        )

        def cls_teardown():
            # CloseableObserver.close_all()
            FixtureBase.fn_call(
                request.cls, 'after_class_teardown', 'CLEANUPING', ns, fixture_name, request.cls
            )
            time.sleep(3)
            thread_list2 = [thread.name for thread in threading.enumerate()]
            logger.info(
                "After class {}, thread list is {}".format(request.cls, thread_list2)
            )
            FixtureBase.log_print(1, 'COMPLETED %s' % ns)

        request.addfinalizer(cls_teardown)

    @staticmethod
    def case_function_hook(request, fixture_name):
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
        # 创建log文件
        # Logmagment().mkdir_file(method=fn_name_case)  # 名字过长会报错
        fn_parent_obj = request.cls
        if request.cls is None:
            fn_parent_obj = request.module
        FixtureBase.fn_call(
            fn_parent_obj,
            'before_func_setup',
            'SETUPING',
            ns,
            fixture_name,
            request.instance,
        )

        def func_teardown():
            print('\t')
            FixtureBase.fn_call(
                fn_parent_obj,
                'after_func_teardown',
                'CLEANUPING',
                ns,
                fixture_name,
                request.instance,
            )
            FixtureBase.log_print(1, 'COMPLETED %s::%s' % (ns, fn_name_case))

        request.addfinalizer(func_teardown)

    @staticmethod
    def fn_call(fn_parent_obj, fn_name, action, ns, fixture_name, instance=None):
        fn = getattr(fn_parent_obj, fn_name, None)
        if fn is None:
            return

        FixtureBase.log_print(2, '%s %s::%s' % (action, ns, fn_name))
        try:
            if instance is None:
                fn(fixture_name)   # 没有类的情况
            else:
                fn(instance, fixture_name)
        except Exception as e:
            # CloseableObserver.close_all()
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/common/fixture/fixture_base.py")
            if "before" in fn_name:
                logger.error("======case前置处理运行失败，请去检查！！！========")
                logger.error(f"运行失败报错： {e}")

                # 强行运行后置处理
                fn_name_after = fn_name.replace('before', 'after').replace('setup', 'teardown')
                FixtureBase.fn_call(
                    fn_parent_obj,
                    fn_name_after,
                    'CLEANUPING',
                    ns,
                    fixture_name,
                    instance,
                )

            raise e

    @staticmethod
    def log_print(level, message):
        dim = '=' if level == 1 else '-'
        dim = dim * 60

        logger.info(dim)
        logger.info('    ' + message)
        logger.info(dim)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :thread_helper.py
@time         :4/11/24 10:32
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import ctypes
import inspect
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import Future
from typing import Dict


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        pass
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class ThreadPoolManager:
    def __init__(self, max_workers=50):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, Future] = {}

    def add_task(self, task_name, function, *args, **kwargs):
        if task_name in self.tasks:
            return
            # raise ValueError(f"Task with name '{task_name}' already exists.")
        future: Future = self.executor.submit(function, *args, **kwargs)
        self.tasks[task_name] = future
        return future

    def remove_task(self, task_name):
        if task_name in self.tasks:
            self.tasks[task_name].cancel()
            del self.tasks[task_name]

    def get_task(self, task_name) -> Future:
        return self.tasks.get(task_name)

    def get_result(self, task_name):
        future = self.tasks.get(task_name)
        if future is None:
            raise ValueError(f"No task with name '{task_name}'.")
        try:
            return future.result()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/thread_helper.py")
            return f"An error occurred: {e}"

    def shutdown(self, wait=True):
        self.executor.shutdown(wait=wait)

    def all_tasks_done(self) -> bool:
        """
        检查所有任务是否都已完成。

        返回:
            如果所有任务都已完成，则返回True；否则返回False。
        """
        for future in self.tasks.values():
            if not future.done():
                return False
        return True

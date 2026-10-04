# -*- coding: utf-8 -*-
"""
@File        : singleton.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2023/7/24 上午10:44
@Description : 线程安全的单利模式
@Examples    :
```
class function(metaclass=SingletonMeta):
    ...
```
"""
import threading


class SingletonMeta(type):
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

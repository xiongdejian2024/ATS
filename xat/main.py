"""保留原 main.py 启动方式，使用 XAT 统一执行入口。"""

from framework.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())

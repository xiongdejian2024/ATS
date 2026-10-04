import os
import sys


ecu_simulator_path = os.path.join(os.path.realpath(__file__).split("ecu_simulator")[0], 'ecu_simulator')

def create_init_py_under_modules(ignore_targets: list = []):
    """补齐模块 __init__.py

    可以自动给包含 python 文件并且缺失 __init__.py 文件的目录下创建 __init__.py 文件

    Args:
        ignore_targets (list, optional): 忽略路径特征. Defaults to [].
    """
    ROOT = ecu_simulator_path

    for dirpath, _, filenames in os.walk(ROOT):
        ignore = False
        for target in ignore_targets:
            if target in dirpath:
                ignore = True
        if ignore:
            continue
        if dirpath == ROOT:
            continue
        init_py_path = os.path.join(dirpath, "__init__.py")
        if not os.path.exists(init_py_path):
            need_to_create = False
            for filename in filenames:
                if filename.endswith(".py"):
                    need_to_create = True
            if need_to_create:
                print(f"need to create: {init_py_path}")
                with open(init_py_path, "w") as f:
                    f.write("")


if __name__ == "__main__":
    # work dir: ecu-simulator
    # cmd: python3 ecu_simulator/tools/pypi_jfrog/add_init.py

    create_init_py_under_modules(
        ignore_targets=[
            "/venv/",
            "pytest_cache",
            "/dist",
            ".git",
            "xat_ecu.legacy.egg-info",
            "logs",
            "__pycache__",
        ]
    )

# -*- coding: utf-8 -*-

"""
@Time    : 2022/5/24 11:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
@Description : 
@Examples    :
"""
import subprocess
import shutil
import os


def delWithCmd(path):
    """
    强制删除文件
    """
    try:
        if os.path.isfile(path):
            cmd = 'del "' + path + '" /F'
            print(cmd)
            os.system(cmd)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/git_clone_demo.py")
        print(e)


def is_directory_empty(path):
    """
    判断目录是否是空的目录
    """
    return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]) == 0


def delete_directory(path):
    """
    递归删除指定的目录
    """
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                try:
                    print(f"删除文件：{file}")
                    os.remove(os.path.join(root, file))
                except PermissionError as e:
                    delWithCmd(os.path.join(root, file))
            for sub_dir in dirs:
                if is_directory_empty(os.path.join(root, sub_dir)):
                    try:
                        os.rmdir(os.path.join(root, sub_dir))
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/git_clone_demo.py")
                        pass
                else:
                    delete_directory(sub_dir)
        else:
            try:
                os.rmdir(path)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/utils/window_canoe/git_clone_demo.py")
                pass

def git_clone(repo_url, target_dir):
    """
    clone最新的工程代码到指定目录，如果target_dir存在，则先递归删除目录，再执行git clone
    """
    # 检查目录是否存在
    # if os.path.exists(target_dir):
    #     # 使用shutil.rmtree删除目录及其所有内容
    #     # shutil.rmtree(target_dir)
    #     delete_directory(target_dir)
    #     print(f"Directory {target_dir} has been removed.")

    try:
        subprocess.run(['git', 'clone', '-b', 'anlei', repo_url, target_dir], check=True)
        return True, f"Repository cloned to {target_dir}"
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e}"


if __name__ == '__main__':
    print(git_clone('https://jidudev.com/soa/soa_test/soa_vector_proj.git', r'D:\test'))

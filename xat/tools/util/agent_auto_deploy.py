
from xat_ecu.legacy.driver.ssh_client import *
from xat_ecu.legacy.common.logger import logger, Logger

global version_name


def type_commands(hostname, commands, password):
    conn = SSHClient(hostname=hostname, username='root', password=password)
    outmsg, errmsg = conn.exec_cmd(commands)
    conn.close()
    if errmsg:
        logger.info(f"{hostname} 上命令 '{commands}' 命令执行失败，失败信息=》{errmsg}")
    else:
        # if len(outmsg) > 0:
        #     logger.info(f'{hostname} 上命令 "{commands}" 执行成功，返回结果=》{outmsg}')
        # else:
        logger.info(f'{hostname} 上命令 "{commands}" 执行成功。')
    return outmsg, errmsg


def sftp_upload_file(host, server_path, local_path, password, timeout=30):
    """
    上传文件，注意：不支持文件夹
    :param host: 主机名
    :param password: 密码
    :param server_path: 远程路径，比如：/home/sdn/tmp.txt
    :param local_path: 本地路径，比如：D:/text.txt
    :param timeout: 超时时间(默认)，必须是int类型
    :return: bool
    """
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username="root", password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
        return True
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/util/agent_auto_deploy.py")
        logger.info(f"向{host}上传文件的异常信息：{e}")
        return False


def putFile_unzip_startAgent(hostname, filename, password, dir_name):
    """
    删除目录->拷贝文件->解压缩->启动进程
    """
    outmsg, errmsg = type_commands(hostname, f"rm -rf {dir_name}*", password)
    if errmsg:
        logger.info(f"{hostname} 上清空目录{dir_name}失败：{errmsg}")
        return False, f"{hostname} 上清空目录{dir_name}失败：{errmsg}"
    result = sftp_upload_file(hostname, dir_name + os.path.splitext(filename)[0]+".zip",
                              "C:\\project\\DaXiang\\soa_mock_app\\" + os.path.splitext(filename)[0]+".zip", password)
    logger.info(f"向{hostname}文件上传结果：{result}")
    if result:  # 文件上传成功，则解压缩并启动进程
        outmsg1, errmsg1 = type_commands(hostname, f"cd {dir_name} && unzip " + os.path.splitext(filename)[0]+".zip", password)
        if errmsg1:
            logger.info(f"{hostname}上解压缩失败!!!")
            return False, f"{hostname}上解压缩失败!!!"
        else:
            # 解压缩成功，则启动agent
            cmd = f"cd {dir_name} && rm -rf " + os.path.splitext(filename)[0]+".zip"
            _, rm_errmsg = type_commands(hostname, cmd, password)
            if rm_errmsg:
                logger.info(f"{hostname} 上原始文件 " + os.path.splitext(filename)[0]+".zip 删除失败")
            else:
                logger.info(f"{hostname} 上原始文件 " + os.path.splitext(filename)[0] + ".zip 删除成功")
            cmd1 = f"cd {dir_name} && echo 'nohup java -jar {version_name} --ip={hostname} &' > run.sh"
            a, b = type_commands(hostname, cmd1, password)
            cmd2 = f"cd {dir_name} && bash run.sh </dev/null >> nohup.out 2>&1"
            _, errmsg2 = type_commands(hostname, cmd2, password)
            if errmsg2:
                logger.info(f"{hostname} agent进程启动 fail！！！")
                return False, f"{hostname} agent进程启动 fail！！！"
            else:
                logger.info(f"{hostname} agent进程启动 success！！！")
                return True, f"{hostname} agent进程启动 success！！！"
    else:
        return False, f"{hostname}上文件上传失败!!!"


def auto_deploy(hostname, password, dir_name):
    global version_name
    outmsg, errmsg = type_commands(hostname, "ps -ef | grep 'java -jar agent' |grep -v grep| awk '{print $2,$10}'", password)
    if errmsg:
        logger.info(f"{hostname} 命令执行失败，失败信息：{errmsg}")
    else:
        if len(outmsg) > 0:  # 进程已启动，则 杀进程-> 拷贝文件-> 解压缩-> 启动进程
            version = outmsg.split(" ")[1]
            pid = outmsg.split(" ")[0]
            logger.info(f"当前进程版本：{version}，进程ID: {pid}")
            if version != version_name:  # 如果版本不是最新的，则kill进程
                logger.info(f"{hostname} 上当前版本{version}，开始停止运行，上传最新版本 {version_name} 并启动")
                outmsg2, errmsg2 = type_commands(hostname, f"kill -9 {pid}", password)
                if errmsg2:
                    logger.info(f"{hostname} 上kill process {pid} fail")
                else:
                    putFile_unzip_startAgent(hostname, version_name, password, dir_name)
            else:
                logger.info(f"{hostname} 上正在运行版本：{version} 为最新版本，无需更新。")
        else:  # 进程未启动，则 拷贝文件-> 解压缩-> 启动进程
            logger.info(f"{hostname} agent进程没有启动")
            outmsg2, errmsg2 = type_commands(hostname, f"cd {dir_name} && ls agent*jar", password)
            if len(outmsg2) == 0:
                logger.info(f"{hostname} 上 {dir_name} 没有程序包, 开始上传最新版本{version_name}并启动.... ")
                putFile_unzip_startAgent(hostname, version_name, password, dir_name)
            else:
                if outmsg2 == version_name:  # 进程未启动，但是版本匹配
                    logger.info(f"{hostname} 上程序为最新版本，但程序未运行，开始运行....")
                    cmd1 = f"cd {dir_name} && echo 'nohup java -jar {version_name} --ip={hostname} &' > run.sh"
                    a, b = type_commands(hostname, cmd1, password)
                    cmd2 = f"cd {dir_name} && bash run.sh </dev/null >> nohup.out 2>&1"
                    _, errmsg2 = type_commands(hostname, cmd2, password)
                    if errmsg2:
                        logger.info(f"{hostname} agent进程启动 fail！！！")
                    else:
                        logger.info(f"{hostname} agent进程启动 success！！！")
                else:  # 进程未启动，且版本不匹配
                    logger.info(f"{hostname} 上的agent版本为{outmsg2}, 开始上传最新版本{version_name}并启动....")
                    putFile_unzip_startAgent(hostname, version_name, password, dir_name)


def dir_exist(hostname, password, dir_name):
    outmsg, errmsg = type_commands(hostname, 'ls '+dir_name, password)

    if errmsg:
        logger.info(f"{hostname}上不存在目录{dir_name}")
        outmsg, errmsg = type_commands(hostname, 'mkdir -p ' + dir_name, password)
        if errmsg:
            logger.info(f"{hostname}上创建目录{dir_name} fail")
        else:
            logger.info(f"{hostname}上创建目录{dir_name} success")
    else:
        logger.info(f"{hostname}上已存在目录{dir_name}")
    return outmsg


class machine:
    def __init__(self, hostname, password=__import__("os").environ.get('XAT_CREDENTIAL____UTIL_AGENT_AUTO_DEPLOY_PY_PASSWORD', ""), dir_name='/root/monitor/agent/'):
        self.hostname = hostname
        self.password = password
        self.dir_name = dir_name


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    global version_name
    version_name = "agent-1.0.11.jar"
    machine_list = []
    machine_list.append(machine("172.18.128.5"))
    # machine_list.append(machine("172.18.128.6", 'jidu1234'))
    machine_list.append(machine("172.18.128.7"))
    machine_list.append(machine("172.18.128.70"))
    machine_list.append(machine("172.18.128.71"))
    # machine_list.append(machine("172.18.128.72"))
    machine_list.append(machine("172.18.128.73"))
    machine_list.append(machine("172.18.128.75"))
    machine_list.append(machine("172.18.128.76"))
    machine_list.append(machine("172.18.128.77"))
    machine_list.append(machine("172.18.128.78"))
    machine_list.append(machine("172.18.128.79"))
    machine_list.append(machine("172.18.128.80"))
    # machine_list.append(machine("172.18.128.113"))

    for m in machine_list:
        logger.info(f"================{m.hostname}  start   ==============")
        dir_exist(m.hostname, m.password, m.dir_name)  # 检测目录 /root/monitor/agent 是否存在，如果不存在则创建
        auto_deploy(m.hostname, m.password, m.dir_name)
        logger.info(f"================{m.hostname}  end   ==============")

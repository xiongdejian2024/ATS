import re
import csv
import tarfile
import pathlib
import fnmatch
import zstandard as zstd

from xat_ecu.legacy.common.logger import *


class LogHandler:
    def __init__(self, **kwargs):
        self.filesystem_list = None
        self.tcam_mem_list = None
        self.tcam_thread_list = None
        self.tcam_cpu_list = None
        self.bgm_cpu_list = None
        self.bgm_mem_list = None
        self.bgm_thread_list = None
        self.logger = kwargs.get('logger', None)
        self.lines = None
        if not self.logger:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            self.logger = logging.getLogger(self.__class__.__name__)

    def read_log(self, path):
        """
        读取log
        return ：self.lines
        """
        self.logger.info("read log from path: {}".format(path))
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            self.lines = f.read()
        # print(self.lines)
        return self.lines

    def extract_tar_gz(self, file_path, destination):
        """
        解压.tar.gz
        file_path:解压文件所在
        destination:解压存放路径
        """
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(path=destination)
            self.logger.info("解压gz完成，存放》》》{}".format(destination))

    def decompress_zst_file(self, input_file, output_file):
        """
        解压zst日志
        file_path:解压路径
        output_file:解压完成存放路径
        """
        try:
            self.logger.info(f"解码zst日志{input_file}")
            if not os.path.exists(os.path.dirname(output_file)):
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

            dctx = zstd.ZstdDecompressor()
            with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
                dctx.copy_stream(fin, fout)
            self.logger.info("解码zst完成，文件存放》》》{}".format(output_file))
        except Exception as err:
            self.logger.error(f"解析zst日志错误，请检查日志，错误信息：{err}")

    def find_files(self, directory, pattern):
        """
        遍历文件键，取出指定文件名的文件
        directory：文件路径
        pattern：文件名所包含的内容
        示例 :     # 搜索包含'message'的文件
        for file_path in find_files(directory, '*message*'):
            print(file_path)
        """
        message_path = []
        self.logger.info("开始遍历文件，文件名包含{}".format(pattern))
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                message_path.append(os.path.join(root, filename))
        self.logger.info("包含{}的有：{}".format(pattern, message_path))
        return message_path

    def is_file_zst(self, zst_file_path):
        self.logger.info("判断文件后缀是.zst")
        if zst_file_path.endswith('.zst'):
            return True
        else:
            return False

    def analysis_bgm_mcu_log(self, file):
        self.read_log(file)
        mcu_pattern = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?McuModuleId 225 LCId 128 ApiId 0 ErrorId 0 NumOfOccur 0 McuModuleReserve2 (\d+) McuModuleReserve3 (\d+) McuModuleReserve4"
        mcu_result = re.findall(mcu_pattern, self.lines)
        self.mcu_cpu_list = []
        self.mcu_cpu1_list = []
        self.mcu_cpu2_list = []
        self.mcu_cpu3_list = []
        for mcu in mcu_result:
            # print(mcu)
            mcu_sixteen = hex(int(mcu[1]))
            mcu1 = int(mcu_sixteen[2:4], 16)
            mcu1_max = int(mcu_sixteen[4:6], 16)
            mcu2 = int(mcu_sixteen[6:8], 16)
            mcu2_max = int(mcu_sixteen[8:10], 16)
            core3 = int(mcu[2]).to_bytes(4, 'big')
            self.mcu_cpu1_list.append({"time": mcu[0], "内核1": mcu1})
            self.mcu_cpu1_list.append({"time": mcu[0], "内核2": mcu2})
            self.mcu_cpu3_list.append({"time": mcu[0], "内核3": core3})
            self.mcu_cpu_list.append(
                {"time": mcu[0], "MCU1": mcu1, "MCU1_MAX": mcu1_max, "MCU2": mcu2, "MCU2_MAX": mcu2_max,
                 "MCU3": core3[0]})

    def analysis_bgm_log(self):
        # cpu_pattern = "CPU : (.+?)% User (.+?)% Sys (.+?)% Nic (.+?)% Idie (.+?)% IO (.+?)% IRQ"
        cpu_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: .*: CPU : (.+?)% User (.+?)% Sys (.+?)% Nic ("
                       ".+?)% Idle (.+?)% IO (.+?)% IRQ")
        cpu_result = re.findall(cpu_pattern, self.lines)
        if len(cpu_result) < 10:
            cpu_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: .*: CPU : (.+?)% User (.+?)% Sys (.+?)% "
                           r"Nic (.+?)% Idle (.+?)% IO (.+?)% IRQ")
            cpu_result = re.findall(cpu_pattern, self.lines)
        self.bgm_cpu_list = []
        for cpu in cpu_result:
            cpu_dick = {"time": cpu[0], "User": cpu[1], "Sys": cpu[2], "Nic": cpu[3], "Idie": cpu[4],
                        "IO": cpu[5], "IRQ": cpu[6]}
            self.bgm_cpu_list.append(cpu_dick)
        mem_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: .*: Mem : (\d+)K total, (\d+)K free, "
                       r"(\d+)K used, (\d+)K buff, (\d+)K cached")
        mem_result = re.findall(mem_pattern, self.lines)
        self.bgm_mem_list = []
        for mem in mem_result:
            percent = int(mem[2]) + int(mem[4]) + int(mem[5])
            mem_dick = {"time": mem[0], "total": mem[1], "free": mem[2], "used": mem[3], "buff": mem[4],
                        "cached": mem[5], "剩余百分比": percent / int(mem[1])}
            self.bgm_mem_list.append(mem_dick)
        self.bgm_thread_list = []
        thread_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: (\d+): *(\d+) .*(\d+)K *(\d+)K *("
                          r"\d+\.\d+)% *(\d+\.\d+)% *(.*)")
        thread_result = re.findall(thread_pattern, self.lines)
        for thread in thread_result:
            # VSS     RSS  %CPU  %MEM Name
            self.bgm_thread_list.append(
                {"time": thread[0], "PID": thread[2], "VSS": thread[3], "RSS": thread[4], "CPU": thread[5],
                 "MEM": thread[6],
                 "Name": thread[7]})
        self.filesystem_list = []
        filesystem_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: (\d+): (.+?) *(\d+) *(\d+) *(\d+) *("
                              r"\d+)% /data")
        filesystem_result = re.findall(filesystem_pattern, self.lines)
        # print(filesystem_result)
        for filesystem in filesystem_result:
            self.filesystem_list.append({"filesystem": filesystem[0], "1k-blocks": filesystem[2], "Used": filesystem[3],
                                         "Available": filesystem[4], "Use%": filesystem[5], "Mounted": filesystem[6]})
        # print(self.filesystem_list)

    def analysis_coredump(self, coredump_file):
        """
        解析coredump
        :param coredump_file:
        """
        self.logger.info("解析coredum》》》{}".format(coredump_file))
        cmd = 'gzip -d {}'.format(coredump_file)
        os.system(cmd)
        result = os.popen('file {}'.format(coredump_file.replace('.gz', '')))
        res = result.read()
        thread_name = re.findall("", res)
        self.logger.info("解析原文为：{}".format(res))
        return res, thread_name

    def analysis_tcam_log(self):
        """
        Mem: 721988K used, 47444K free, 2676K shrd, 81728K buff, 301428K cached
        CPU: 10.7% usr 39.1% sys  0.0% nic 47.4% idle  0.0% io  0.0% irq  2.6% sirq
        Load average: 4.91 5.22 5.41 1/1378 7610
          PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
        23473     2 root     DW<      0  0.0   0  3.6 [kworker/u3:0]
        """
        # (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: .*
        # pattern = r'CPU : (\d+)% User (\d+)% Sys (\d+)% Nic (\d+)% Idie (\d+)% IO (\d+)% IRQ'
        pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I monitor_s: .*: CPU : (\d+)% User (\d+)% Sys (\d+)% Nic "
                   r"(\d+)% Idie (\d+)% IO (\d+)% IRQ")
        cpu_result = re.findall(pattern, self.lines)
        # print(cpu_result)
        self.tcam_cpu_list = []
        for cpu in cpu_result:
            self.tcam_cpu_list.append(
                {"time": cpu[0], "User": cpu[1], "Sys": cpu[2], "Nic": cpu[3], "Idie": cpu[4], "IO": cpu[5],
                 "PID": cpu[6]})
        # PID  STAT    PR   NI      VSS     RSS  %CPU  %MEM Name
        thread_pattern = (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I monitor_s: .*:  *(\d+) .*(\d+)K *(\d+)K *('
                          r'\d+\.\d+)% *(\d+\.\d+)% *(.*)')
        cpu_thread = re.findall(thread_pattern, self.lines)
        # print(cpu_thread)
        self.tcam_thread_list = []
        for thread in cpu_thread:
            self.tcam_thread_list.append(
                {"time": thread[0], "PID": thread[1], "CPU": thread[4], "MEM": thread[5], "name": thread[6]})
        # print(self.tcam_thread_list)
        mem_pattern = (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I monitor_s: .*: Mem : (\d+)K total, (\d+)K free, '
                       r'(\d+)K used, (\d+)K buff, (\d+)K cached')
        MEM = re.findall(mem_pattern, self.lines)
        # print(MEM)
        self.tcam_mem_list = []
        for mem in MEM:
            percent = int(mem[2]) + int(mem[4]) + int(mem[5])
            self.tcam_mem_list.append(
                {"time": mem[0], "total": mem[1], "free": mem[2], "used": mem[3], "buff": mem[4], "cached": mem[5],
                 "剩余百分比": percent / int(mem[1])})
        # print(self.tcam_mem_list)

    def teardown_unzip_log(self, log_path, device_name):
        # 解压tar_gz
        self.logger.info("解压{}".format(log_path))
        output_file = os.path.join(os.path.dirname(log_path), device_name)
        if not os.path.exists(output_file):
            os.makedirs(output_file)
        # 解压tar.gz
        self.extract_tar_gz(log_path, output_file)
        i = 0
        # 匹配*message*文件
        for file_path in self.find_files(output_file, '*message*'):
            print(file_path)
            # 判断文件是否zst结尾
            if self.is_file_zst(file_path):
                # 解压zst
                self.logger.info("解压{}".format(file_path))
                self.decompress_zst_file(file_path, "{}/{}{}_log.txt".format(output_file, device_name, i))
                i += 1
        return output_file

    def write_to_csv(self, filename, data):
        """
       数据写入csv
       :param filename:文件名字
       :param data:数据data，格式list[]嵌套字典，每个字典key必须一致
        """
        if len(data) <= 0:
            self.logger.warning(f"{filename}数据data为空,请检测日志文件是否正确")
        # header = ['time', 'User', 'Sys', 'Nic', 'Idie', 'IO', 'IRQ']
        else:
            header = list(data[0].keys())
            # data = data
            with open(filename, 'a') as file:
                # Create a CSV dictionary writer and add the student header as field names
                writer = csv.DictWriter(file, fieldnames=header)
                # Use writerows() not writerow()
                writer.writeheader()
                writer.writerows(data)

    def teardown_analysis_log(self, log_path, mcu=True):
        self.logger.info("处理日志，写入CSV文件")
        if os.path.exists(log_path) and log_path.endswith("bgm"):
            self.logger.info("正在处理bgm日志")
            for file in os.listdir(log_path):
                if file.endswith(".txt"):
                    file = os.path.join(log_path, file)
                    self.read_log(file)
                    if mcu:
                        self.analysis_bgm_mcu_log()
                        self.write_to_csv(os.path.join(log_path, "bgm_mcu_list.csv"), self.mcu_cpu_list)
                    self.analysis_bgm_log()
                    self.write_to_csv(os.path.join(log_path, "bgm_thread_list.csv"), self.bgm_thread_list)
                    self.write_to_csv(os.path.join(log_path, "bgm_cpu_list.csv"), self.bgm_cpu_list)
                    self.write_to_csv(os.path.join(log_path, "bgm_mem_list.csv"), self.bgm_mem_list)
        elif os.path.exists(log_path) and log_path.endswith("tcam"):
            self.logger.info(f"正在处理tcam日志{log_path}")
            print(os.listdir(log_path))
            for file in os.listdir(log_path):
                if file.endswith(".txt"):
                    file = os.path.join(log_path, file)
                    self.read_log(file)
                    self.analysis_tcam_log()
                    self.write_to_csv(os.path.join(log_path, "tcam_cpu_list.csv"), self.tcam_cpu_list)
                    self.write_to_csv(os.path.join(log_path, "tcam_mem_list.csv"), self.tcam_mem_list)
                    self.write_to_csv(os.path.join(log_path, "tcam_thread_list.csv"), self.tcam_thread_list)
        else:
            self.logger.info("请检查文件路径是否正确")

    def handle_bgm_logs(self, bgm_log_path, mcu=True):
        try:
            self.logger.info("处理bgm日志，写入CSV文件")
            for file in os.listdir(bgm_log_path):
                if file.startswith('jetlog_messages') and file.endswith('.zst'):
                    print('current_file:', file)
                    file_path = os.path.join(bgm_log_path, file)


            for root, dirs, files in os.walk(bgm_log_path):
                for file in files:
                    if file.startswith('jetlog_messages') and file.endswith('.zst'):
                        print('current_file:', file)
                        file_path = os.path.join(root, file)
                        replace_file = os.path.join(root, 'ana_bgm', file.replace("zst", "txt"))
                        self.decompress_zst_file(file_path, replace_file)
                        if os.path.exists(replace_file):
                            self.read_log(replace_file)
                            if mcu:
                                self.analysis_bgm_mcu_log()
                                self.write_to_csv(os.path.join(bgm_log_path, "bgm_mcu_list.csv"), self.mcu_cpu_list)

                            self.analysis_bgm_log()
                            self.write_to_csv(os.path.join(bgm_log_path, "bgm_thread_list.csv"), self.bgm_thread_list)
                            self.write_to_csv(os.path.join(bgm_log_path, "bgm_cpu_list.csv"), self.bgm_cpu_list)
                            self.write_to_csv(os.path.join(bgm_log_path, "bgm_mem_list.csv"), self.bgm_mem_list)

        except Exception as e:
            self.logger.error('处理bgm日志error:{}'.format(e))

    def handle_tcam_logs(self, tcam_log_path):
        # try:
        self.logger.info(f"处理tcam日志，写入CSV文件")
        for root, dirs, files in os.walk(tcam_log_path):
            for file in files:
                if file.startswith('jetlog_messages') and file.endswith('.zst'):
                    print('current_file:', file)
                    file_path = os.path.join(root, file)
                    replace_file = os.path.join(root, 'ana_tcam', file.replace("zst", "txt"))

                    self.decompress_zst_file(file_path, replace_file)
                    if os.path.exists(replace_file):
                        self.read_log(replace_file)
                        self.analysis_tcam_log()
                        self.write_to_csv(os.path.join(tcam_log_path, "tcam_cpu_list.csv"), self.tcam_cpu_list)
                        self.write_to_csv(os.path.join(tcam_log_path, "tcam_mem_list.csv"), self.tcam_mem_list)
                        self.write_to_csv(os.path.join(tcam_log_path, "tcam_thread_list.csv"),
                                          self.tcam_thread_list)
    # except Exception as e:
    # self.logger.error('处理tcam日志error:{}'.format(e))


def log_analysis():
    log_handle = LogHandler()
    monitor = Monitor()
    coredump_path = monitor.get_tcam_coredump()
    if coredump_path:
        out_file = log_handle.teardown_unzip_log(coredump_path, "tcam_coredump")
        log_handle.teardown_analysis_log(out_file)
    monitor.client_tcam_tar_log()
    tcam_log_path = monitor.get_tcam_log()
    if tcam_log_path is not None:
        out_file = log_handle.teardown_unzip_log(tcam_log_path, "tcam")
        log_handle.teardown_analysis_log(out_file)
    bgm_log_path = monitor.get_bgm_log()
    if bgm_log_path is not None:
        out_file = log_handle.teardown_unzip_log(bgm_log_path, 'bgm')
        log_handle.teardown_analysis_log(out_file)
    for coredump in monitor.get_bgm_coredump():
        log_handle.analysis_coredump(coredump)
    monitor.clear_all_log()


if __name__ == '__main__':
    loghandler = LogHandler()
    # loghandler.teardown_unzip_log("/root/zhenhua/log/bgm_log_2023-12-07_13:37:39.tar.gz", "bgm")
    # loghandler.teardown_unzip_log("/root/zhenhua/log/bgm_log_2023-12-06_15:15:05.tar.gz","bgm")
    loghandler.handle_bgm_logs('/sat/log/bgm_log')

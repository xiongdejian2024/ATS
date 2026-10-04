import os.path
import re
import csv
import shutil
import tarfile
import pathlib
import fnmatch
import zstandard as zstd
import logging
import pandas as pd


class LogParser:
    def __init__(self, **kwargs):
        self.logger = kwargs['logger'] if kwargs.get("logger") else logging
        self.bgm_log_path = kwargs["bgm_log_path"] if kwargs.get("bgm_log_path") else '.'
        self.tcam_log_path = kwargs["tcam_log_path"] if kwargs.get("tcam_log_path") else '.'

    def get_txt_log_files(self, log_path):
        """
        txt log files are parsed from zst files
        """
        return [os.path.join(log_path, file) for file in os.listdir(log_path) if
                file.startswith("jetlog_messages") and file.endswith("txt")]

    def read_log_file(self, file):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as fr:
                lines = fr.read()
        except Exception as e:
            lines = ''
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))
        return lines

    def decompress_zst_file(self, log_path):
        try:
            zst_files = [file for file in os.listdir(log_path) if file.startswith("jetlog_message") and file.endswith(".zst")]
            for file in zst_files:
                self.logger.info("开始解析{}...".format(os.path.join(log_path, file)))
                new_file = file.replace("zst", "txt")
                dctx = zstd.ZstdDecompressor()
                with open(os.path.join(log_path, file), 'rb') as fin, open(os.path.join(log_path, new_file), 'wb') as fout:
                    dctx.copy_stream(fin, fout)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def handle_bgm_logs(self):
        self.logger.info("开始解析bgm jetlog为txt格式")
        self.decompress_zst_file(self.bgm_log_path)

        try:
            self.logger.info("开始解析jetlog txt数据")
            self.analysis_bgm_log()

        except Exception as e:
            self.logger.error('处理bgm日志error:{}'.format(e))

    def analysis_bgm_log(self):
        txt_log_files = self.get_txt_log_files(log_path=self.bgm_log_path)
        if not txt_log_files:
            self.logger.warning(f"Not any bgm txt log files to analysis")
            return

        self.logger.info(f"开始解析bgm mcu log")
        self.analysis_bgm_mcu_log(log_files=txt_log_files)

        self.logger.info(f"开始解析bgm cpu log")
        self.analysis_bgm_cpu_log(log_files=txt_log_files)

        self.logger.info(f"开始解析bgm mem log")
        self.analysis_bgm_mem_log(log_files=txt_log_files)

        self.logger.info(f"开始解析bgm thread log")
        self.analysis_bgm_process_log(log_files=txt_log_files)

        self.logger.info(f"开始解析bgm filesystem log")
        self.analysis_bgm_filesystem_log(log_files=txt_log_files)

    def analysis_bgm_mcu_log(self, log_files):
        mcu_pattern = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?McuModuleId 225 LCId 128 ApiId 0 ErrorId 0 NumOfOccur 0 McuModuleReserve2 (\d+) McuModuleReserve3 (\d+) McuModuleReserve4"

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的mcu log...")
                mcu_cpu_list = []

                lines = self.read_log_file(file)
                mcu_result = re.findall(pattern=mcu_pattern, string=lines)
                for mcu in mcu_result:
                    mcu1_current, mcu1_max, mcu2_current, mcu2_max = int(mcu[1]).to_bytes(4, 'big')
                    mcu3_current, mcu3_max, _, _ = int(mcu[2]).to_bytes(4, 'big')
                    test_result = "PASS" if (mcu1_current < 85 or mcu1_max < 85 or mcu2_current < 85 or mcu2_max < 85
                                             or mcu3_current < 85 or mcu3_max < 85) else "FAIL"

                    mcu_cpu_list.append(
                        {
                            "FileName": file,
                            "Time": mcu[0],
                            "MCU1_Current": mcu1_current,
                            "MCU1_Max": mcu1_max,
                            "MCU2_Current": mcu2_current,
                            "MCU2_Max": mcu2_max,
                            "MCU3_Current": mcu3_current,
                            "MCU3_Max": mcu3_max,
                            "Test_Result": test_result
                        }
                    )

                self.write_to_csv(os.path.join(self.bgm_log_path, "bgm_mcu_list.csv"), mcu_cpu_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def analysis_bgm_cpu_log(self, log_files):
        cpu_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: .*: CPU : (.+?)% User (.+?)% Sys (.+?)% Nic ("
                       ".+?)% Idle (.+?)% IO (.+?)% IRQ")

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的bgm cpu log...")
                bgm_cpu_list = []
                lines = self.read_log_file(file)

                cpu_result = re.findall(cpu_pattern, lines)
                for cpu in cpu_result:
                    test_result = "PASS" if float(cpu[4]) > 5 else 'FALSE'
                    bgm_cpu_list.append(
                        {
                            "FileName": file,
                            "Time": cpu[0],
                            "User": cpu[1],
                            "Sys": cpu[2],
                            "Nic": cpu[3],
                            "Idie": cpu[4],
                            "IO": cpu[5],
                            "IRQ": cpu[6],
                            "Test_Result": test_result
                         }
                    )
                self.write_to_csv(os.path.join(self.bgm_log_path, "bgm_cpu_list.csv"), bgm_cpu_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def analysis_bgm_mem_log(self, log_files):
        mem_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: .*: Mem : (\d+)K total, (\d+)K free, "
                       r"(\d+)K used, (\d+)K buff, (\d+)K cached")

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的bgm mem log...")
                bgm_mem_list = []
                lines = self.read_log_file(file)

                mem_result = re.findall(mem_pattern, lines)
                for mem in mem_result:
                    percent = int(mem[2]) + int(mem[4]) + int(mem[5])
                    remaining_percentage = percent / int(mem[1])
                    test_result = "FAIL" if remaining_percentage < 0.3 else "PASS"
                    bgm_mem_list.append(
                        {
                            "FileName": file,
                            "Time": mem[0],
                            "Total": mem[1],
                            "Free": mem[2],
                            "Used": mem[3],
                            "Buff": mem[4],
                            "Cached": mem[5],
                            "Remaining_Percentage": remaining_percentage,
                            "Test_Result": test_result
                        }
                    )
                self.write_to_csv(os.path.join(self.bgm_log_path, "bgm_mem_list.csv"), bgm_mem_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def analysis_bgm_process_log(self, log_files):
        process_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: (\d+): *(\d+) .*(\d+)K *(\d+)K *("
                          r"\d+\.\d+)% *(\d+\.\d+)% *(.*)")

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的bgm thread log...")
                bgm_process_list = []
                lines = self.read_log_file(file)

                thread_result = re.findall(process_pattern, lines)
                for thread in thread_result:
                    bgm_process_list.append(
                        {
                            "FileName": file,
                            "time": thread[0],
                            "PID": thread[2],
                            "VSS": thread[3],
                            "RSS": thread[4],
                            "CPU": thread[5],
                            "MEM": thread[6],
                            "Name": thread[7]
                        }
                    )
                self.write_to_csv(os.path.join(self.bgm_log_path, "bgm_process_list.csv"), bgm_process_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def analysis_bgm_filesystem_log(self, log_files):
        filesystem_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I SYSM: (\d+): (.+?) *(\d+) *(\d+) *(\d+) *("
                           r"\d+)% /data")

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的bgm filesystem log...")
                bgm_filesystem_list = []
                lines = self.read_log_file(file)

                filesystem_result = re.findall(filesystem_pattern, lines)
                for filesystem in filesystem_result:
                    bgm_filesystem_list.append(
                        {
                            "FileName": file,
                            "filesystem": filesystem[1],
                            "1k-blocks": filesystem[2],
                            "Used": filesystem[3],
                            "Available": filesystem[4],
                            "Use%": filesystem[5],
                            "Mounted": filesystem[6]
                        }
                    )
                self.write_to_csv(os.path.join(self.bgm_log_path, "bgm_filesystem_list.csv"), bgm_filesystem_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

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

    def handle_tcam_logs(self):
        self.logger.info("开始解析tcam jetlog为txt格式")
        self.decompress_zst_file(self.tcam_log_path)

        try:
            self.logger.info("开始解析jetlog txt数据")
            self.analysis_tcam_log()

        except Exception as e:
            self.logger.error('处理tcam日志error:{}'.format(e))

    def analysis_tcam_log(self):
        txt_log_files = self.get_txt_log_files(log_path=self.tcam_log_path)
        if not txt_log_files:
            self.logger.warning(f"Not any tcam txt log files to analysis")
            return

        self.logger.info(f"开始解析tcam cpu log")
        self.analysis_tcam_cpu_log(log_files=txt_log_files)

        self.logger.info(f"开始解析tcam mem log")
        self.analysis_tcam_mem_log(log_files=txt_log_files)

        self.logger.info(f"开始解析tcam thread log")
        self.analysis_tcam_process_log(log_files=txt_log_files)

    def analysis_tcam_cpu_log(self, log_files):
        cpu_pattern = (r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I monitor_s: .*: CPU : (\d+)% User (\d+)% Sys (\d+)% "
                       r"Nic (\d+)% Idie (\d+)% IO (\d+)% IRQ")

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的tcam cpu log...")
                tcam_cpu_list = []
                lines = self.read_log_file(file)

                cpu_result = re.findall(cpu_pattern, lines)
                for cpu in cpu_result:
                    test_result = "PASS" if float(cpu[4]) > 5 else 'FALSE'
                    tcam_cpu_list.append(
                        {
                            "FileName": file,
                            "Time": cpu[0],
                            "User": cpu[1],
                            "Sys": cpu[2],
                            "Nic": cpu[3],
                            "Idie": cpu[4],
                            "IO": cpu[5],
                            "PID": cpu[6],
                            "Test_Result": test_result
                         }
                    )
                self.write_to_csv(os.path.join(self.tcam_log_path, "tcam_cpu_list.csv"), tcam_cpu_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def analysis_tcam_mem_log(self, log_files):
        mem_pattern = (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I monitor_s: .*: Mem : (\d+)K total, (\d+)K free, '
                       r'(\d+)K used, (\d+)K buff, (\d+)K cached')

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的tcam mem log...")
                tcam_mem_list = []
                lines = self.read_log_file(file)

                mem_result = re.findall(mem_pattern, lines)
                for mem in mem_result:
                    percent = int(mem[2]) + int(mem[4]) + int(mem[5])
                    remaining_percentage = percent / int(mem[1])
                    test_result = "FAIL" if remaining_percentage < 0.3 else "PASS"
                    tcam_mem_list.append(
                        {
                            "FileName": file,
                            "Time": mem[0],
                            "Total": mem[1],
                            "Free": mem[2],
                            "Used": mem[3],
                            "Buff": mem[4],
                            "Cached": mem[5],
                            "Remaining_Percentage": remaining_percentage,
                            "Test_Result": test_result
                        }
                    )
                self.write_to_csv(os.path.join(self.tcam_log_path, "tcam_mem_list.csv"), tcam_mem_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def analysis_tcam_process_log(self, log_files):
        process_pattern = (r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).* I monitor_s: .*:  *(\d+) .*(\d+)K *(\d+)K *('
                           r'\d+\.\d+)% *(\d+\.\d+)% *(.*)')

        try:
            for file in log_files:
                self.logger.info(f"开始解析{file}的tcam thread log...")
                tcam_process_list = []
                lines = self.read_log_file(file)

                thread_result = re.findall(process_pattern, lines)
                for thread in thread_result:
                    tcam_process_list.append(
                        {
                            "FileName": file,
                            "time": thread[0],
                            "PID": thread[1],
                            "CPU": thread[4],
                            "MEM": thread[5],
                            "Name": thread[6]
                        }
                    )
                self.write_to_csv(os.path.join(self.tcam_log_path, "tcam_process_list.csv"), tcam_process_list)
        except Exception as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))

    def write_to_csv(self, filename, data):
        """
       数据写入csv
       :param filename:文件名字
       :param data:数据data，格式list[]嵌套字典，每个字典key必须一致
        """
        if len(data) <= 0:
            print(f"{filename}数据data为空,请检测日志文件是否正确")
            return

        header = list(data[0].keys())
        with open(filename, 'a') as file:
            # Create a CSV dictionary writer and add the student header as field names
            writer = csv.DictWriter(file, fieldnames=header)
            # Use writerows() not writerow()
            writer.writeheader()
            writer.writerows(data)

    def read_csv(self, filename):
        try:
            df = pd.read_csv(filename, sep=',')
            test_result = df["Test_Result"]
        except FileNotFoundError as e:
            self.logger.error("Error {} happened in line {}".format(e, e.__traceback__.tb_lineno))
            return -1
        else:
            return test_result[test_result == "FAIL"].count()

    def parser_test_result(self, domain: str):
        test_result = {}

        csv_files = ["bgm_mcu_list.csv", "bgm_cpu_list.csv", "bgm_mem_list.csv",
                     "tcam_cpu_list.csv", "tcam_mem_list.csv"]
        log_path = self.bgm_log_path if domain == "bgm" else self.tcam_log_path
        for csv in csv_files:
            if domain in csv:
                test_result[csv.split("_")[1]] = self.read_csv(os.path.join(log_path, csv))

        return test_result


if __name__ == '__main__':
    loghandler = LogParser(bgm_log_path="/root/cyb/soa_perstab_log/bgm_log/")
    loghandler.handle_bgm_logs()
    loghandler.handle_tcam_logs()
    # loghandler.parser_test_result()

import json
import os.path
import pathlib
import sys
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_ecu.legacy.common.logger import Logger


class statistics_summary_result:
    def __init__(self, files_count=0, total_rows=0, total_cases=0, details=[]):
        """
        files_count: 测试用例文件数
        total_rows：测试用例总行数
        total_cases：测试用例总数
        """
        self.files_count = files_count
        self.total_rows = total_rows
        self.total_cases = total_cases
        self.average_rows_per_case = 0
        # details 为列表，每个元素为字典，字典的键为目录名，字典的值为列表，列表包含目录下每个文件的统计信息字典：文件名：
        self.details = details

    def print_dict_form(self, flag=False):
        if self.total_cases > 0:
            self.average_rows_per_case = self.total_rows // self.total_cases
        dict_form = {"files_count": self.files_count, "total_rows": self.total_rows,
                     "total_cases": self.total_cases, "average_rows_per_case": self.average_rows_per_case}
        if flag:
            dict_form["details"] = self.details
        logger.info(json.dumps(dict_form, ensure_ascii=False, indent=4))
        return dict_form


class detail_result:
    def __init__(self, file_dir, file_name, total_case_num=0, total_row_num=0, detail=[]):
        """
        file_dir: 文件所在目录
        file_name：文件名
        total_case_num：总用例数
        total_row_num：总行数
        """
        self.file_dir = file_dir
        self.file_name = file_name
        self.total_case_num = total_case_num
        self.total_row_num = total_row_num
        self.details = detail

    def print_dict_form(self, flag=False):
        dict_form = {"file_name": os.path.join(self.file_dir, self.file_name), "total_case_num": self.total_case_num,
                     "total_row_num": self.total_row_num, "average_case_row_num": 0 if self.total_case_num == 0 else
                        self.total_row_num//self.total_case_num}
        # if flag:
        #     dict_form["details"] = self.details
        # logger.info(json.dumps(dict_form, ensure_ascii=False, indent=4))
        return dict_form


def get_filenames_by_dir(dir_name=r"C:\project\2023-Q3-Target\sat\test_case\soa\test_function"):
    path = pathlib.Path(dir_name)
    if path.exists():
        logger.info("路径存在")
        if path.is_dir():
            logger.info("是目录")
        elif path.is_file():
            logger.info("是文件")


def getALLDirAndFile(dir_path, exclude_dir=[]):
    # 判断目录是否存在,不存在直接结束函数
    file_list = []
    # logger.info(dir_path)
    if not os.path.exists(dir_path):
        logger.info(f"文件不存在")
        return
        # 把文件夹下的内容放入列表,便于下一步分析
    listName = os.listdir(dir_path)
    for fileDirName in listName:
        # 拼接成绝对路径
        abspath = os.path.join(dir_path, fileDirName)

        # 判断该路径是否是目录,如果是目录,就用递归的方式继续遍历,不是的话就会退出
        if os.path.isdir(abspath):
            # logger.info(f"{abspath} 是目录")
            # 递归遍历目录
            path = pathlib.Path(abspath)
            # logger.info(f"最底层目录名：{path.parts[-1]}, 类型是{type(path.parts[-1])},exclude_dir is {exclude_dir}")
            if path.parts[-1] not in exclude_dir:
                file_list.extend(getALLDirAndFile(abspath, exclude_dir))
        # 判断是否是文件
        if os.path.isfile(abspath):
            # logger.info(f"{abspath} 是文件")
            path = pathlib.Path(abspath)
            if path.suffix == '.py' and path.name.startswith("test_"):
                file_list.append(abspath)
    return file_list


def statistics_case_row_num_dir(dir_name, exclude_dir=None, flag=True):
    """
    dir_name: 测试用例所在的目录
    exclude_dir：不统计的目录
    flag: 是否仅统计抽象接口的用例，默认是True
    """
    summary_result = statistics_summary_result()
    if exclude_dir is None:  # 不包含的文件夹
        exclude_dir = ['data_drive', 'kdt']
    files_in_dir = getALLDirAndFile(dir_name, exclude_dir)
    for file_name in files_in_dir:
        result = []
        case_start_flag = False
        first_flag = True  # 是否是第一条用例
        current_row = 0  # 当前的用例行数
        total_rows = 0
        total_test_case = 0
        test_function_name = ""
        counter_right = 0
        counter_left = 0
        skip_flag = False
        with open(file_name, encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if flag:
                    if line.startswith("class"):
                        if "TestABCBase" not in line:
                            skip_flag = True
                            break
                if len(line) > 0:  # 去除空行
                    if line.startswith("def test_"):
                        total_test_case = total_test_case + 1
                        if len(test_function_name) > 0:
                            result.append({test_function_name: current_row})
                        test_function_name = line.split(" ")[1].split("(")[0]
                        # logger.info(f"测试函数名称：{test_function_name}")
                        case_start_flag = True
                        current_row = 0
                        counter_right = 0
                        counter_left = 0
                        continue  # 每条测试用例的 def 语句不算在用例行数统计内
                    if line.replace(" ", "").startswith("#"):  # 去除注释行
                        continue
                    if line.replace(" ", "").startswith("@"):  # 去除注释行
                        continue
                    if "__name__" in line:
                        break
                    # if any(include_str in line for include_str in include_list):
                    if case_start_flag:
                        counter_right += line.count('(')
                        counter_left += line.count(')')
                        if counter_left == counter_right:
                            current_row = current_row + 1
                            total_rows = total_rows + 1
            else:
                if len(test_function_name) > 0:
                    result.append({test_function_name: current_row})
        if total_test_case == 0:
            continue
        signal_file_result = detail_result(os.path.dirname(file_name), os.path.basename(file_name),
                                           total_test_case, total_rows, result).print_dict_form(True)
        summary_result.total_rows = summary_result.total_rows + total_rows
        summary_result.total_cases = summary_result.total_cases + total_test_case
        summary_result.files_count = summary_result.files_count + 1
        if not skip_flag:
            summary_result.details.append(signal_file_result)

    summary_result.print_dict_form(True)
    return summary_result


if __name__ == "__main__":
    logger = Logger().get_logger("test")
    statistics_case_row_num_dir(r"/root/huizhao/sat/xat_cases/legacy/", flag=True)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :utils.py
@Time         :2023/09/24 17:30:31
@Author       :jiabin.zhu@jiduauto.com
@Description  : 放杂七杂八的函数
"""
import os
import xlrd2
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.driver.tosun.tosunbus import current_path
from xat_ecu.legacy.driver.ssh_interface import file_download, command_send


def ck_pdu_period_time(pdu_data_info, pdu_id, period, deviation=0.1):
    """
    校验pdu的周期
    @param pdu_data_info: pcap解析出的信号数据
    @param pdu_id: 以太网数据pdu的id
    @param period: 期望周期, 单位s
    @param deviation: 默认±10%为可接受偏差
    """
    last_time = None
    for key in pdu_data_info:
        if key[0] == pdu_id:
            for data in pdu_data_info[key]:
                if last_time is None:
                    last_time = data[2]
                else:
                    assert abs(data[2] - last_time - period) / period < deviation, \
                        f"{data[2]}与前一帧数据偏差大于{deviation * 100}%"
                    last_time = data[2]
            return True


def ck_pdu_sporadic(pdu_data_info, pdu_id, times=1):
    """
    校验pdu为事件帧
    @param pdu_data_info: pcap解析出的信号数据
    @param pdu_id: 以太网数据pdu的id
    @param times: pdu次数
    """
    for key in pdu_data_info:
        if key[0] == pdu_id:
            assert len(pdu_data_info[key]) == times, f"pdu{pdu_id}次数应该是{times}"


def ck_pdu_ordered_array(tcp_datas: list, ck_array: list):
    """
    校验周期下行pdu中信号为有序数组
    从获取到ck_array第一个信号开始校验，因为抓tcpdump开始的数据可能还没有下发服务请求，不是期望值
    @param tcp_datas: 抓取的下行pdu数据[(index, value, timestamp)]
    @param ck_array:  信号数组
    """
    curr_ck_value = ck_array.pop(0)
    start_ck = False
    for data in tcp_datas:
        if not start_ck and data[1] == curr_ck_value:
            start_ck = True  # 拿到第一个期望数据，开始校验有序数组
            last_ck_value = curr_ck_value
            if ck_array:
                curr_ck_value = ck_array.pop(0)
            continue
        
        if start_ck:
            if data[1] == last_ck_value:
                continue
            elif data[1] == curr_ck_value:
                last_ck_value = curr_ck_value
                if ck_array:
                    curr_ck_value = ck_array.pop(0)
            else:
                assert False, f"{data}不该出现在该时刻"
    if ck_array:
        assert False, f"未校验完成，剩余{ck_array}"


def check_bgm_error_log_init(bgmcli):
    # 先移除旧的日志
    bgmcli.type_commands("mkdir /log/log_backup;mv /log/jetlog* /log/log_backup/")

def check_bgm_error_log(bgmcli, log_num=2):
    """
    检查bgm里S2S的Error日志和socket绑定失败的Error日志
    需配合check_bgm_error_log_init使用
    @param bgmcli：即self.bgmcli
    @param log_num：检查最近几份的日志，默认2份
    """
    log_list = get_lastest_log(num=log_num)
    data = ''
    try:
        for log in log_list:
            data += bgmcli.type_commands(f"/app/bin/zstdcat /log/{log}|grep -Ein '( E s2s| E handy:|RT throttling activated)'", timeout=600)
        if ' E s2s' in data:
            return False,f"检测到s2s有error日志{data}"
        elif ' E handy' in data:
            return False,f"检测到socket绑定服务端的地址和端口有error日志{data}"
        elif 'RT throttling activated' in data:
            return False,f"检测到s2s线程卡死的日志{data}"
        else:
            return True,"没有Error日志"
    except Exception as e:
        logger.error(e)
    
def recover_bgm_log(bgmcli):
    # 恢复旧的日志
    bgmcli.type_commands("mv /log/log_backup/*.zst /log/;rm -rf /log/log_backup")


tobus_path = os.path.join(current_path, "tosunbus.py")
input = [            
    '        ################\n',
    '        time.sleep(0.03)\n',
    '        file = os.path.join(os.getcwd(), "tosun_asc_product_time")\n',
    '        with open(file, "a") as fds:\n',
    '            __timestap = time.time()\n',
    '            fds.write(str(__timestap)+"\\n")\n',
    '            logger.info(__timestap)\n',
    '        logger.info("tosun_asc_product_time success")\n'
    ]
index = []
tosun_data = []


def update_tosun():
    with open(tobus_path, "r") as fd:
        tosun_data = fd.readlines()
        logger.info(tosun_data)
        index = [i for i, element in enumerate(tosun_data) if element == '        self.p = Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True, preexec_fn=os.setsid, text=True)\n']
        logger.info(index[0])
    os.system(f"rm {tobus_path}")
    with open(tobus_path, "a") as fd:
        for i in (tosun_data[:(index[0]+2)]+ input + tosun_data[(index[0]+2):]):
            fd.write(i)


def recover_tosun():
    with open(tobus_path, "r") as fd:
        tosun_data = fd.readlines()
        logger.info(tosun_data)
        index = [i for i, element in enumerate(tosun_data) if element == '        self.p = Popen(cmd, shell=True, stdout=subprocess.PIPE, close_fds=True, preexec_fn=os.setsid, text=True)\n']
    os.system(f"rm {tobus_path}")
    with open(tobus_path, "a") as fd:
        for i in (tosun_data[:(index[0]+2)] + tosun_data[(index[0]+10):]):
            fd.write(i)


def get_ETH_signal_from_SDB(file, sheet_name, folder):
    """
    从SDB表中筛选出需要信号路由的信号
    file: SDB表文件名
    sheet_name: SDB表文件sheet页
    folder: 需要更新脚本的目标文件夹
    """
    excel_path = os.path.dirname(os.path.realpath(__file__)).split("sat")[0] + file
    wb1 = xlrd2.open_workbook(excel_path, encoding_override="utf-8")
    sheet = wb1.sheet_by_name(sheet_name)
    testcases_list = [] # 需要路由信号的列表
    num_rows = sheet.nrows
    for i in range(1, num_rows):
        if "底层软件需配置信号路由" in sheet.cell_value(i, 20):
            testcases_list.append(sheet.cell_value(i, 7))
    # print(f"底层软件需配置信号路由的信号：{testcases_list}")
    
    files_list = [] # 获取所有接口py文件
    for home, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)).split("sat")[0], "sat/xat_cases/legacy/soa", folder)):
        for filename in files:
            if "pyc" not in filename:
                files_list.append(os.path.join(home, filename))
    # print(f"所有文件：{files_list}")

    # 开始更新
    no_check_sig = [] #没有self.ipdu.check的信号
    col = 0
    for sig in testcases_list:
        # if sig == "PosnFromSatltTiForMsec":
            sig_flag = False
            for file in files_list:
                # if "xat_cases.legacy.py" in file:
                    with open (file, "r") as f:
                        lines = f.readlines()
                    with open(file, "w", encoding="utf-8") as fd:
                        new_line = 0
                        for line, data in enumerate(lines):
                             # 下次写入的行数需要
                            if f"self.ipdu.check(self.ipdu" in data and sig in data:
                                sig_flag = True
                                all_data = [] 
                                # 对于以#开头的已注释的脚本不做修改
                                if not data.strip().startswith('#'):
                                    print(data)
                                    if data.replace("\n", "").split('#')[0].strip()[-1] == ")":
                                        new_line = line + 1
                                        all_data.append(data)
                                    elif lines[line+1].replace("\n", "").split('#')[0].strip()[-1] == ")":
                                        new_line = line + 2
                                        all_data.append(data)
                                        all_data.append(lines[line+1])
                                    elif lines[line+2].replace("\n", "").split('#')[0].strip()[-1] == ")":
                                        new_line = line + 3
                                        all_data.append(data)
                                        all_data.append(lines[line+1])
                                        all_data.append(lines[line+2])
                                    else:
                                        print(f"{data}有误，请线下check")

                                for i in range(len(all_data)):
                                    if "timeout" not in "".join(all_data):
                                        if all_data[-1].replace("\n", "").strip() == ")":
                                            if i < len(all_data) - 2:
                                                fd.write(all_data[i])
                                            elif i == len(all_data) - 2:
                                                if '#' not in all_data[i]:
                                                    fd.write(all_data[i].replace("\n", "").rstrip()[:-1] + ", timeout=0.5)" + "\n")
                                                else:
                                                    fd.write(all_data[i].replace("\n", "").split('#')[0].rstrip()[:-1] + ", timeout=0.5)" + ' #' + all_data[i].replace("\n", "").split('#')[-1] + "\n")
                                        else:
                                            if i != len(all_data) - 1:
                                                fd.write(all_data[i])
                                            else:
                                                if "\n" in all_data[i]:
                                                    if '#' not in all_data[i]:
                                                        fd.write(all_data[i].replace("\n", "").rstrip()[:-1] + ", timeout=0.5)" + "\n")
                                                    else:
                                                        fd.write(all_data[i].replace("\n", "").split('#')[0].rstrip()[:-1] + ", timeout=0.5)" + ' #' + all_data[i].replace("\n", "").split('#')[-1] + "\n")
                                                else:
                                                    if '#' not in all_data[i]:
                                                        fd.write(all_data[i].rstrip()[:-1] + ", timeout=0.5)")
                                                    else:
                                                        fd.write(all_data[i].split('#')[0].rstrip()[:-1] + ", timeout=0.5)" + ' #' + all_data[i].replace("\n", "").split('#')[-1])
                                    else:
                                        # 高压和后视镜的timeout不动
                                        # if file.split('/')[-1] not in ['test_HighVoltageAppService.py', 'test_HighVoltageService.py', 'test_OuterRearViewService.py']:
                                        #     if all_data[-1].replace("\n", "").strip() == ")":
                                        #         if i < len(all_data) - 2:
                                        #             fd.write(all_data[i])
                                        #         elif i == len(all_data) - 2:
                                        #             if '#' not in all_data[i]:
                                        #                 fd.write(all_data[i].split("timeout")[0] + "timeout=0.5)" + "\n")
                                        #             else:
                                        #                 fd.write(all_data[i].split("timeout")[0] + "timeout=0.5)" + ' #' + all_data[i].replace("\n", "").split('#')[-1] + "\n")
                                        #     else:
                                        #         if "timeout" in all_data[i]:
                                        #             if "\n" in all_data[i]:
                                        #                 if '#' not in all_data[i]:
                                        #                     fd.write(all_data[i].split("timeout")[0] + "timeout=0.5)" + "\n")
                                        #                 else:
                                        #                     fd.write(all_data[i].split("timeout")[0] + "timeout=0.5)" + ' #' + all_data[i].replace("\n", "").split('#')[-1] + "\n")
                                        #             else:
                                        #                 if '#' not in all_data[i]:
                                        #                     fd.write(all_data[i].split("timeout")[0] + "timeout=0.5)")
                                        #                 else:
                                        #                     fd.write(all_data[i].split("timeout")[0] + "timeout=0.5)" + ' #' + all_data[i].replace("\n", "").split('#')[-1])
                                        #         else:
                                        #             fd.write(all_data[i])
                                        fd.write(all_data[i])
                            if new_line <= line:
                                        fd.write(lines[line])

            if not sig_flag:
                no_check_sig.append(sig)
                import pandas as pd
                ms_excel_path = os.path.join(os.path.dirname(os.path.realpath(__file__))).split("sat")[0] + f"MARS1_V2.0.5_BGM_Internal_ETH_Signal.xlsx"
                
                if not os.path.exists(ms_excel_path):
                    os.mknod(f"{ms_excel_path}")

                data = pd.read_excel(ms_excel_path, keep_default_na=True, engine='openpyxl')
                # 只需要关注Mars1 sheet页
                if sig:
                    print(f"开始插入数据信号：{sig}")
                    data.loc[col+1 , "ETH Signal Name"] = sig
                    col += 1
                data.to_excel(ms_excel_path, index=False)
                    

    print(f"没有校验总线的信号有：{no_check_sig}")
    

def get_lastest_log(log_types="messages", num=2, local_path="/root/", device_name='BGM',  connect_type="vlan", is_download=False):    
    """
    从域控获取最近几份的log日志
    device_name: 默认bgm域控
    connect_type: 默认vlan方式连接
    log_type: 需要下载的日志类型，比如messages，bts，s2s，默认messages
    num: 需要下载的日志数量，默认下载最近2份
    local_path: 本地下载的日志地址，默认/root/
    """   
    log_list = [] 
    log_name_type = []
    if isinstance(log_types, str):
        log_name_type.append(log_types)
    elif isinstance(log_types, list):
        log_name_type = log_types
    for log_type in log_name_type:
        data = command_send(device_name=device_name, connect_type=connect_type, cmd=f"cd /log;ls -lh|grep 'jetlog_{log_type} ->'|" + "awk '{print $11}'")
        if data[-1]:
            num_now = data[-1].split(f"jetlog_{log_type}")[-1].split("_")[0]
            if int(num_now) >= num:
                for i in range(num):
                    log_name = command_send(device_name=device_name, connect_type=connect_type, cmd=f"cd /log;ls jetlog_{log_type}" + str(int(num_now) - i) + "*")
                    log_list.append(log_name[-1])
            else:
                logger.info(f"{device_name}日志中只有{num_now}个日志，全部下载")
                for i in range(1, int(num_now)+1):
                    log_name = command_send(device_name=device_name, connect_type=connect_type, cmd=f"cd /log;ls jetlog_{log_type}{i}*")
                    log_list.append(log_name[-1])
        else:
            logger.info(f"没有查询到{device_name}日志，请线下check")
    if is_download:
        for j in log_list:
            file_download(device_name=device_name, local_path=local_path, remote_path=f"/log/{j}", connect_type=connect_type)
    
    return log_list

if __name__ == "__main__":
    get_ETH_signal_from_SDB("MARS1_V2.0.5_BGM_Internal_ETH_Communicaiton_Release_20240515.xlsx", "BGM ETH Internal Communication", "interface")

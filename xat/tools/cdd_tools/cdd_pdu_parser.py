# -*- coding: utf-8 -*-
"""
@File        : cdd_pdu_parser.py.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/4/26 20:01
@Description : 
@Examples    :
"""


def get_raw_data(f_path):
    start_append = False
    data = []
    with open(f_path, 'r') as cdd:
        for line in cdd:
            print(line)
            if line.split("   ")[0] == "0030":
                start_append = True
            if start_append:
                data += line.split("   ")[1].split(" ")
    return data


def get_data(r_data, dl):
    data = r_data[:dl]
    raw_data = r_data[dl:]
    return data, raw_data


def gen_comment(err_str):
    if err_str != "":
        return "  # {}".format(err_str)
    else:
        return ""


def bus_id_check(data):  # 1byte, raw_data
    error_str = ""
    data = "".join(data)
    if int(data, 16) not in range(1, 13) and \
            int(data, 16) not in range(41, 48):
        error_str = "bus_id非法"
    return error_str


def not_zero_check(data):  # 1~4byte raw_data
    error_str = ""
    frame_id = 0
    try:
        frame_id = int("".join(data), 16)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/cdd_pdu_parser.py")
        error_str = "值类型非法"
    if frame_id == 0:
        error_str = "值非法"
    return error_str


def easy_print(p_str, o_file=None):
    print(p_str)
    if o_file:
        o_file.write(p_str)
        o_file.write("\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CDD data parser from tcpdump raw data")
    parser.add_argument('-f', type=str, help='f: log file path')
    parser.add_argument('-o', type=str, default=None, help="o: parser output file path")
    args = parser.parse_args()
    cdd_log_path = args.f
    out_file = None
    if args.o:
        out_file = open(args.o, 'w')
    raw_data = get_raw_data(cdd_log_path)
    print(raw_data)
    print(f'raw_data length: {len(raw_data)}')
    time_stampe, raw_data = get_data(raw_data, 6)
    easy_print(f'全局时钟: {time_stampe}', out_file)
    try:
        while len(raw_data) > 0:
            # print("=" * 40)
            easy_print("=" * 40, out_file)
            bus_id_raw, raw_data = get_data(raw_data, 1)  # bus id是1byte
            bus_id = bus_id_raw[0]
            if int(bus_id, 16) in range(41, 48):  # lin, 报文id为1byte
                f_id, raw_data = get_data(raw_data, 1)
            elif int(bus_id, 16) in range(2, 13):  # CAN/CANFD, 报文ID为2byte
                f_id, raw_data = get_data(raw_data, 2)
            elif int(bus_id, 16) == 1:  # FR, 报文id为4byte
                f_id, raw_data = get_data(raw_data, 4)
                easy_print("**" * 40, out_file)
                easy_print("FR 报文", out_file)
                easy_print("**" * 40, out_file)
            elif int(bus_id, 16) == 254 and len(raw_data) == 0:  # 结束符
                exit()
            else:
                print(f"bus_id error {bus_id}!!!")
                exit()
            check_str = gen_comment(bus_id_check(bus_id_raw))
            easy_print(f'总线编号:{bus_id_raw} {check_str}', out_file)
            check_str = gen_comment(not_zero_check(f_id))
            easy_print(f'报文ID:{f_id}  {check_str}', out_file)
            ms_ts, raw_data = get_data(raw_data, 2)  # ms时间戳 2 byte
            easy_print(f'毫秒时间戳: {ms_ts}', out_file)
            f_len, raw_data = get_data(raw_data, 1)  # 报文长度 1 byte
            check_str = gen_comment(not_zero_check(f_len))
            easy_print(f'报文长度: {f_len} {check_str}', out_file)
            f_len = int(f_len[0], 16)
            f_data, raw_data = get_data(raw_data, f_len)
            easy_print(f'报文内容:{f_data}', out_file)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/cdd_tools/cdd_pdu_parser.py")
        print(str(e))
    finally:
        if out_file:
            out_file.close()

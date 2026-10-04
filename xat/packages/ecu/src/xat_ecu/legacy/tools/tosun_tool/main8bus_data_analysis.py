# -*- coding: utf-8 -*-
"""
@File        : main
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/9/4 10:53
@Description :

"""
import copy
import csv
import time


def read_asc_file(file_name, start=5):
    can_dic = {}
    canfd_dic = {}
    error_Lis = []
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()[start:]

        for line_index, line in enumerate(lines):
            if "Statistic" in line or "error" in line or "End" in line or "Start" in line:
                continue
            if len(line.strip()) < len("396.207222 1  00A       Tx  d"):
                continue
            if "Rx" in line:
                continue
            if "53F" in line:
                continue
            if "CANFD" in line:
                data = [i for i in line.split(' ') if i.strip()]
                # print(data)
                can_time = round(float(data[0]) * 1000, 3)
                can_channel = data[2]
                canid = data[4]
                can_rt = data[3]
                # if int(canid, 16) != int(can_id, 16):
                #     continue

                if can_channel in canfd_dic:
                    #
                    if int(canid, 16) in canfd_dic[can_channel]:
                        lis = canfd_dic[can_channel][int(canid, 16)]
                        tmp = round(can_time - lis[-1][1], 3)
                        # if abs(tmp - 10) > 0.5:
                        #     error_Lis.append(tmp)
                        error_Lis.append(tmp)
                        lis.append((line_index + start + 1, can_time, can_rt, tmp, canid, can_channel))
                    else:
                        # error_Lis.append(0)
                        canfd_dic[can_channel][int(canid, 16)] = [
                            (line_index + start + 1, can_time, can_rt, 0.0, canid, can_channel)]
                else:
                    # error_Lis.append(0)
                    canfd_dic[can_channel] = {
                        int(canid, 16): [(line_index + start + 1, can_time, can_rt, 0.0, canid, can_channel)]
                    }
                # break
            else:
                if not line.strip():
                    continue
                data = [i for i in line.split(' ') if i.strip()]
                # print(data)
                can_time = round(float(data[0]) * 1000, 3)
                can_channel = data[1]
                canid = data[2]
                can_rt = data[3]
                if can_channel in can_dic:
                    #
                    if int(canid, 16) in can_dic[can_channel]:
                        lis = can_dic[can_channel][int(canid, 16)]
                        tmp = round(can_time - lis[-1][1], 3)
                        lis.append((line_index + start + 1, can_time, can_rt, tmp, canid, can_channel))
                    else:
                        can_dic[can_channel][int(canid, 16)] = [
                            (line_index + start + 1, can_time, can_rt, 0.0, canid, can_channel)]
                else:
                    can_dic[can_channel] = {
                        int(canid, 16): [(line_index + start + 1, can_time, can_rt, 0.0, canid, can_channel)]
                    }

                # break
    # pprint.pprint(canfd_dic)
    # print(can_id, len(error_Lis), error_Lis)
    return can_dic, canfd_dic


def count_per(data_list, cycl):
    '''
    统计 百分比
    :param data_list: 数据
    :param cycl: 周期
    :return:
    '''

    data_list1 = data_list[1:]
    time_list = [item[3] for item in data_list1]
    # print('该报文相邻两帧报文时间差', time_list)
    per_lis = ["5", '10', "20", "30", "40", "50", "60", "70", "80"]
    dic = dict(zip(per_lis, [0] * len(per_lis)))
    for index, item in enumerate(time_list):
        v = abs(item - cycl)
        if 0 <= v < 0.05 * cycl:
            dic["5"] = dic["5"] + 1
        elif 0.05 * cycl <= v < 0.1 * cycl:
            dic["10"] = dic["10"] + 1
        elif 0.1 * cycl <= v < 0.2 * cycl:
            name = "20"
            dic[name] = dic[name] + 1
        elif 0.2 * cycl <= v < 0.3 * cycl:
            name = "30"
            dic[name] = dic[name] + 1
        elif 0.3 * cycl <= v < 0.4 * cycl:
            name = "40"
            dic[name] = dic[name] + 1
        elif 0.4 * cycl <= v < 0.5 * cycl:
            name = "50"
            dic[name] = dic[name] + 1
        elif 0.5 * cycl <= v < 0.6 * cycl:
            name = "60"
            dic[name] = dic[name] + 1
        elif 0.6 * cycl <= v < 0.7 * cycl:
            name = "70"
            dic[name] = dic[name] + 1
        else:
            print(f"误差超过80%的数据帧 所在过滤该报文后索引位置{index+2}  比周期多{v}  源文件当前所在==》》{data_list1[index]}")
            name = "80"
            dic[name] = dic[name] + 1

    all_counts = sum(list(dic.values()))
    print("该报文总条数", all_counts)
    new_dic = {}
    for key, value in dic.items():
        new_dic[key] = str(float(round(value / all_counts, 4) * 100)) + "%"
    print("该报文在每个误差区间个数", dic)
    print("该报文在每个误差区间百分比", new_dic)
    return all_counts, dic, new_dic


def get_canid_time_cycle2(file_name):
    canid_lis = []
    cycle_lis = []
    type_lis = []
    channel_lis = []
    can_dic = {}
    canfd_dic = {}

    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if not line.strip():
                continue
            if not line.strip().startswith("[01"):
                continue
            channe_index = str(int(line[3:4], 16) + 1)

            new_lins = copy.deepcopy(lines[index + 1:])
            print(line)
            for lin in new_lins:
                if not lin.strip():
                    continue
                if lin.strip().startswith("CANID"):
                    canid = lin.replace(" ", '').strip().split("=")[-1]
                    canid = int(canid)
                    canid_lis.append(canid)
                    continue
                if lin.strip().startswith("ISCANFD"):
                    msg_type = lin.replace(" ", '').strip().split("=")[-1].strip()

                    type_lis.append(msg_type)
                    continue
                if lin.strip().startswith("CyclcTime"):
                    cycle = lin.replace(" ", '').strip().split("=")[-1]
                    if cycle == "None":
                        cycle = None
                    else:
                        cycle = int(1000 * float(cycle))
                    cycle_lis.append(cycle)
                    continue
                if lin.strip().startswith("[01"):
                    if msg_type == "1":
                        if channe_index in canfd_dic:
                            canfd_dic[channe_index][canid] = cycle
                        else:
                            canfd_dic[channe_index] = {canid: cycle}
                    else:
                        if channe_index in can_dic:
                            can_dic[channe_index][canid] = cycle
                        else:
                            can_dic[channe_index] = {canid: cycle}
                    break

    print("can_cycle_dic=", can_dic)
    print("canfd_cycle_dic=", canfd_dic)

    return can_dic, canfd_dic


def save_data2csv(save_file_name, data_file_name, can_cycle_dic, canfd_cycle_dic):
    otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
    with open(f'.\{save_file_name}_{otherStyleTime}.csv', 'w+', newline="") as file:
        writer = csv.writer(file)
        header = ["通道", "canid", "canid", "周期", "总数", "can类型", "百分比", "5以下", '10', "20", "30", "40", "50",
                  "60",
                  "70",
                  "80以上"]
        writer.writerow(header)
        can_dic, canfd_dic = read_asc_file(data_file_name, start=5)
        for channel, canid_info in can_dic.items():
            for can_id, data_list in canid_info.items():
                try:
                    cycl = can_cycle_dic[channel][can_id]
                except Exception:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/tosun_tool/main8bus_data_analysis.py")
                    cycl = None
                    print(f"\n=======通道==》》{channel} canid >> {can_id} {hex(can_id)},周期》》{cycl}=========")
                print(f"\n=======通道==》》{channel} canid >> {can_id} {hex(can_id)},周期》》{cycl}=========")
                all_count, num_dic, per_dic = count_per(data_list, cycl)

                count_lis = list(num_dic.values())
                data_string = [channel, hex(can_id), can_id, cycl, all_count, "can", "0"] + count_lis
                writer.writerow(data_string)

                per_lis = list(per_dic.values())
                data_string = [channel, hex(can_id), can_id, cycl, all_count, "can", "1"] + per_lis
                writer.writerow(data_string)

        print('*****************************************')
        for channel, canid_info in canfd_dic.items():
            for can_id, data_list in canid_info.items():
                cycl = canfd_cycle_dic[channel][can_id]
                print(f"\n========通道==》》{channel} canid >> {can_id} {hex(can_id)},周期》》{cycl}========")
                all_count, num_dic, per_dic = count_per(data_list, cycl)

                count_lis = list(num_dic.values())
                data_string = [channel, hex(can_id), can_id, cycl, all_count, "canfd", "0"] + count_lis
                writer.writerow(data_string)

                per_lis = list(per_dic.values())
                data_string = [channel, hex(can_id), can_id, cycl, all_count, "canfd", "1"] + per_lis
                writer.writerow(data_string)


# 获取TC1018 小程序发送的 can 报文的id 对应的周期
# file_path = r"C:\LTG\002code\test02\同星can报文检测\11\11.txt"
# can_cycle_dic, canfd_cycle_dic = get_canid_time_cycle2(file_path)


can_cycle_dic = {
    '1': {1435: 1250, 177: 20, 37: 20, 512: 90, 289: 30, 1029: 150, 1033: 250, 1034: 150, 933: 400, 1037: 150,
          1040: 150, 1049: 150, 1145: 1000, 1168: 60, 1184: 150, 1025: 500, 295: 100, 831: 200, 851: 1000, 856: 1000,
          860: 1000, 865: 1000, 868: 1000, 596: 900, 600: 900, 604: 300, 607: 900, 1152: 1000, 1153: 1000, 1154: 1000,
          1155: 1000, 1156: 1000, 1157: 1000, 1158: 1000, 1159: 1000, 1160: 1000, 1161: 1000, 1162: 1000, 1163: 1000,
          805: 135, 579: 100, 768: 100, 769: 100, 770: 100, 771: 100, 772: 100, 773: 100, 774: 100, 48: 70, 480: 400,
          291: 100, 5: 25, 192: 20, 535: 20, 53: 20, 581: 100, 800: 200, 536: 20, 54: 20, 16: 20, 293: 100, 416: 300,
          149: 45, 578: 100, 546: 20, 55: 20, 112: 30, 515: 50, 554: 20, 56: 20, 117: 20, 516: 50, 105: 20, 665: 95,
          272: 70, 304: 35, 275: 70, 1063: 150, 616: 50, 617: 50, 625: 50},
    '4': {258: 40, 367: 10, 1245: 1000, 150: 10, 278: 20, 136: 20, 128: 10, 37: 10, 53: 10, 256: 25, 272: 25, 304: 25,
          288: 50, 352: 100, 512: 100, 528: 30, 544: 30, 704: 80, 640: 70, 800: 200, 560: 40, 880: 700, 848: 400,
          752: 80, 944: 1000, 547: 30, 570: 40, 101: 10, 156: 15, 563: 130, 529: 150, 597: 150, 785: 230, 819: 270,
          1136: 1000, 1137: 1000, 1138: 1000, 1139: 1000, 1140: 1000, 1141: 1000, 1142: 1000, 1143: 1000, 1144: 1000,
          36: 10, 69: 20, 1170: 1000, 1173: 1000, 1174: 1000, 1175: 1000, 1177: 1000, 1162: 1000, 1163: 1000,
          1164: 1000, 1165: 1000, 1178: 1000, 1114: 500, 1091: 400, 325: 30, 531: 130, 431: 10, 687: 30, 447: 10,
          98: 10, 112: 15, 160: 15, 208: 15, 224: 20, 240: 25, 320: 25, 928: 60, 384: 20, 480: 30, 448: 30, 336: 25,
          432: 30, 496: 30, 576: 60, 736: 80, 720: 80, 513: 30, 784: 400, 864: 500, 896: 700, 624: 70, 688: 50,
          768: 300, 832: 120, 464: 30, 549: 40, 562: 40, 774: 170, 568: 40, 1024: 1000, 776: 130, 501: 40, 26: 10,
          103: 40, 17: 10, 548: 80, 579: 150, 856: 300, 857: 320, 769: 300, 664: 300, 647: 200, 1179: 1000},
    '3': {298: 20, 147: 20, 51: 10, 554: 100, 1111: 50, 708: 130, 859: 170, 871: 200, 979: 260, 1039: 300, 563: 100,
          991: 270, 304: 25, 1135: 30, 576: 800, 455: 30, 587: 100, 543: 40, 609: 100, 632: 100, 642: 100, 131: 10,
          752: 80, 1157: 1000, 1158: 1000, 820: 260, 832: 260, 837: 260, 822: 260, 246: 10, 70: 15, 444: 25, 955: 400,
          78: 10, 64: 10, 362: 50, 363: 50, 81: 10, 160: 15, 400: 20, 224: 20, 928: 320, 433: 30, 1087: 350, 432: 30,
          736: 70, 1123: 170, 784: 170, 137: 20, 823: 165, 686: 120, 1243: 170, 1255: 170, 1267: 170, 1099: 170,
          26: 100, 1159: 700, 864: 80, 896: 700, 17: 10, 496: 30, 439: 30},
    '2': {321: 20, 373: 100, 376: 70, 659: 400, 661: 600, 662: 600, 834: 1000, 789: 800, 817: 1000, 769: 600, 664: 600,
          646: 140, 323: 20, 833: 1000, 837: 1000, 838: 1000, 839: 1000, 325: 100, 648: 100, 83: 100, 322: 30, 656: 100,
          1177: 1000, 1180: 1000, 1161: 900, 1144: 1000, 261: 20, 1025: 300, 1026: 300, 331: 50, 329: 50, 1109: 800,
          341: 25, 259: 20, 74: 10, 80: 10, 102: 15, 305: 20, 132: 25, 816: 260, 369: 50, 406: 70, 647: 300, 1160: 800,
          392: 70, 75: 10, 634: 100, 401: 70, 278: 20, 1168: 1000, 649: 100, 328: 25, 309: 20, 310: 20, 76: 10, 96: 20,
          1111: 800, 1125: 800, 773: 600, 613: 80, 626: 100, 643: 150, 99: 20, 1126: 800, 393: 40, 544: 80, 272: 20,
          629: 160, 314: 20, 512: 80, 342: 20, 149: 10, 627: 100, 1178: 800, 1179: 800, 640: 120, 148: 20, 384: 40,
          550: 80, 53: 200, 302: 20, 98: 15, 118: 15, 113: 15, 65: 10, 312: 25, 313: 25, 353: 25, 358: 50, 609: 80,
          597: 80, 354: 50, 86: 15, 645: 200, 296: 25, 667: 200, 49: 15, 1051: 500, 1042: 500, 304: 15, 1143: 120,
          819: 1000, 282: 20}, '5': {339: 55, 137: 60, 18: 20, 19: 20, 33: 10}}
canfd_cycle_dic = {
    '10': {375: 80, 16: 10, 20: 10, 24: 45, 408: 100, 580: 100, 581: 100, 928: 200, 496: 50, 497: 50, 498: 50, 499: 50,
           500: 50, 501: 50, 240: 20, 502: 50, 503: 50, 504: 50, 505: 50, 507: 50, 508: 50, 241: 20, 509: 50, 510: 50,
           511: 50, 513: 50, 514: 50, 515: 50, 242: 20, 516: 50, 517: 50, 518: 50, 519: 50, 520: 50, 521: 50, 243: 20,
           401: 85, 357: 60, 330: 40, 356: 40, 360: 40, 31: 2000, 769: 85},
    '8': {593: 50, 124: 50, 256: 30, 594: 50, 127: 50, 272: 30, 592: 50, 596: 50, 608: 50},
    '7': {768: 60, 256: 60, 784: 200, 1104: 320, 192: 20},
    '9': {304: 20, 389: 70, 305: 450, 288: 50, 289: 45, 1040: 320}}

data_file_name = f"can.asc"
save_data2csv(data_file_name.split('.')[0], data_file_name, can_cycle_dic, canfd_cycle_dic)

# data_file_name = f"CANoe 8个通道接收数据.asc"
# save_data2csv(data_file_name.split('.')[0], data_file_name, can_cycle_dic, canfd_cycle_dic)

import base64
import csv
import json
import os
import random
import requests
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import folium
from folium.plugins import MousePosition

from jal_cloud_communication import Client

timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
user = 'cHVibGljX3NvYV9iZ21fdGNhbQ=='
password = __import__("os").environ.get('XAT_CREDENTIAL____JFS_ROUTE_MAP_ROUTE_MAP_RECOVERY_PY_PASSWORD', "")


def upload_files_to_youzhi(local_file_path, remote_dir_path='/SOA/JFS_route_map/'):
    """
    将本地文件上传到指定的远程目录，并生成一个无需密码的分享链接。

    Args:
        local_file_path (str): 要上传的本地文件路径。
        remote_dir_path (str, optional): 远程目录路径，默认为'/SOA/JFS_route_map/'。

    Returns:
        str: 生成的无密码分享链接。
    """
    nc = Client(host='http://youzi.jidudev.com')
    nc.login(user=base64.b64decode(user).decode(), password=base64.b64decode(password).decode())
    remote_dir_path = remote_dir_path + os.path.basename(local_file_path)
    nc.put_file(remote_file_path=remote_dir_path, local_file_path=local_file_path)
    link = nc.simply_share_no_passwd(remote_path=remote_dir_path)
    return link


def send_request_with_retry(data_url, method, data=None, params=None, headers=None, timeout=600, retry_count=3):
    current_retry = 0
    while current_retry < retry_count:
        try:
            if method == 'post':
                response = requests.post(data_url, data=json.dumps(data), headers=headers, timeout=timeout)
            elif method == 'get':
                response = requests.get(data_url, params=params)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code == 200 and response.ok:
                return response
            else:
                print(f"请求失败，正在尝试重新连接... 失败原因：{response.text}")
                current_retry += 1
                time.sleep(2 * current_retry)  # 逐渐增加等待时间
        except requests.exceptions.RequestException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/JFS_route_map/route_map_recovery.py")
            print(f"请求过程中发生异常：{e}")
            current_retry += 1
            time.sleep(2 * current_retry)  # 逐渐增加等待时间
    raise Exception("请求失败，已达到最大重试次数。")


def get_network_status_csv(data_url, envs="prod", timeout=600, retry_count=3):
    """
    从指定URL获取网络状态信息，并将其保存为CSV文件。

    Args:
        data_url (str): 包含查询参数的URL，用于指定网络状态查询的参数。
        envs (str, optional): 环境标识，默认为"prod"。用于指定查询哪个环境的网络状态。
        timeout (int, optional): 请求超时时间（秒），默认为600秒。
        retry_count (int, optional): 请求重试次数，默认为3次。

    Returns:
        str: 保存CSV文件的名称。

    Raises:
        ValueError: 如果响应内容不是有效的bytes数据，则引发此异常。
    """
    base_url = "https://soa-log-parser.jidustaging.com"
    parsed_url = urlparse(data_url)
    query_params = parse_qs(parsed_url.query)
    csv_name = f"{query_params['vin'][0]}_output_{timestamp}.csv"
    url_board = f"{base_url}/api/diag/network/board"
    url_status = f"{base_url}/api/diag/network/status"
    headers = {'Content-Type': 'application/json'}
    data_status = {
        "start_time": query_params['start_time'][0],
        "end_time": query_params['end_time'][0],
        "vin": query_params['vin'][0],
        "envs": envs
    }
    response_board = send_request_with_retry(url_board, 'post', data=data_status, headers=headers, timeout=timeout,
                                             retry_count=retry_count)
    response_status = send_request_with_retry(url_status, 'post', data=data_status, headers=headers, timeout=timeout,
                                              retry_count=retry_count)

    url_download = f"{base_url}/api/diag/network/download"
    params_download = {'vin': query_params['vin'][0]}
    response_download = send_request_with_retry(url_download, 'get', params=params_download, timeout=timeout,
                                                retry_count=retry_count)

    content = response_download.content
    if not isinstance(content, bytes):
        raise ValueError("content不是有效的bytes数据")
    with open(csv_name, 'wb') as f:
        f.write(content)
    upload_files_to_youzhi(local_file_path=csv_name)
    return csv_name


####################read csv file####################
def read_csv(file):
    apn1, apn4 = [], []
    with open(file, encoding='gbk') as f:
        reader = csv.reader(f)
        first_line_list = next(reader)
        for row in reader:
            if row[4] == "无日志" or row[4] == "0.0":
                continue
            if row[2] == '1':
                apn1.append(row)
            else:
                apn4.append(row)
        return first_line_list, apn1, apn4


##############str to float####################################
def float_data(str_data, para_ind) -> list:  # para_ind  表示数据表中的列，如 11 表示RsrpVector
    return list(map(float, [line[para_ind] for line in str_data]))


#################data for map line return lon and lat############################
def map_line_data(data_str_list: list) -> list:
    lon_data = float_data(data_str_list, 4)  # col3 --->lon
    lat_data = float_data(data_str_list, 5)  # col4 --->lat
    return list(zip(lat_data, lon_data))


############################################make data slices###################################################
def deal_data_by_ind(data1, ind):
    """
    :param data1:
    :param ind:
    :return:
    返回数据格式[[(value, slice), (value, slice), ...], [(value, slice), (value, slice), ...], ...]
    """
    data_change_pos = []
    data1_length = len(data1)
    if data1_length < 2:
        return data1
    for i in range(0, data1_length - 1):
        if data1[i][ind] != data1[i + 1][ind]:
            data_change_pos.append(i)
    data_change_pos.append(data1_length)
    fina_data = []
    data_new = []
    fina_data.append(data1[0:data_change_pos[0] + 1])

    for j in range(1, len(data_change_pos)):
        fina_data.append(data1[data_change_pos[j - 1]: data_change_pos[j] + 1])

    # if ind >= 39 and ind != 47:
    #     if fina_data[0][0][ind] == 'False':  # 暂时不改  以后会有bug
    #         fina_data = fina_data[::2]
    #         # return fina_data, data_change_pos
    #     else:
    #         fina_data = fina_data[1::2]
    #         # return fina_data, data_change_pos
    for i in fina_data:
        value = i[-1][ind]
        data_new.append((value, i))
    if data_change_pos:
        return data_new, data_change_pos
    else:
        return data_new


##############################random color###########################

color_map = {}  # 用于存储参数和颜色代码的映射


def generate_color(param):
    if param in color_map:
        return color_map[param]

    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color_code = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    color_map[param] = color_code  # 将参数和生成的颜色代码存储在字典中
    return color_code


#################draw line and point########################
def drawLineOnMap(data_rat, data_pci, data_ping_fail, data_ping_fail_pos, data_weak_signal, data_high_latency, tiles,
                  show_now=True):
    m = folium.Map(location=data_rat[0][1][0], tiles=tiles, attr='default', width='100%', height='100%', zoom_start=12)
    Rat_group = folium.FeatureGroup(name="RAT", control=True)
    Pci_group = folium.FeatureGroup(name="PCI", control=True)
    Pingfail_group = folium.FeatureGroup(name="PingFail&HighLatency", control=True)
    high_latency_group = folium.FeatureGroup(name="HighLatency", control=True)
    pingfail_pos_group = folium.FeatureGroup(name="PingFailPosition", control=True)
    weak_signal_group = folium.FeatureGroup(name="WeakSignal", control=True)
    folium.CircleMarker(
        location=data_rat[0][1][0], radius=5, color="yellow", fill=True,
        fill_color="red", fill_opacity=0.6,
        popup="start"
    ).add_to(m)  # 画起点

    for data_slices_rat in data_rat:
        if data_slices_rat[0] in ('7', '7.0'):
            folium.PolyLine(data_slices_rat[1], color='green', tooltip='5G').add_to(Rat_group)
        elif data_slices_rat[0] in ('3', '3.0'):
            folium.PolyLine(data_slices_rat[1], color='blue', tooltip='4G').add_to(Rat_group)
    for data_slices_pci in data_pci:
        folium.PolyLine(data_slices_pci[1], color=generate_color(data_slices_pci[0]), tooltip=data_slices_pci[0]).add_to(Pci_group)

    for data_slices_ping_fail in data_ping_fail:
        if data_slices_ping_fail[0] in ('True', 'true'):
            folium.PolyLine(data_slices_ping_fail[1], color='red', tooltip='ping fail').add_to(Pingfail_group)
        elif data_slices_ping_fail[0] in ('False', 'false'):
            folium.PolyLine(data_slices_ping_fail[1], color='green', tooltip='ping ok').add_to(Pingfail_group)

    for pingfail_pos in data_ping_fail_pos:
        folium.Marker(location=pingfail_pos, popup=pingfail_pos).add_to(pingfail_pos_group)

    for data_slices_weak_signal in data_weak_signal:
        if data_slices_weak_signal[0] in ('false', 'False'):
            folium.PolyLine(data_slices_weak_signal[1], color='green', tooltip='网络无问题').add_to(weak_signal_group)
        elif data_slices_weak_signal[0] in ('true', 'True'):
            folium.PolyLine(data_slices_weak_signal[1], color='red', tooltip='弱信号').add_to(weak_signal_group)
    for data_slices_high_latency in data_high_latency:
        if data_slices_high_latency[0] > 500:
            folium.PolyLine(data_slices_high_latency[1], color='blue',
                            tooltip=f'高延时:{data_slices_high_latency[0]}').add_to(high_latency_group)
    Pingfail_group.add_child(high_latency_group)
    m.add_child(Rat_group)
    m.add_child(Pci_group)
    m.add_child(Pingfail_group)
    m.add_child(pingfail_pos_group)
    m.add_child(weak_signal_group)
    folium.LayerControl(collapsed=False).add_to(m)
    MousePosition().add_to(m)
    html_file = f"route_map_{timestamp}.html"
    m.save(html_file)
    if show_now:
        m.show_in_browser()
    return html_file



###########################################################################
def map_wrapper(excel_list, apn_data, title, show_now=False):  # 按照10列RAT进行区分,按照19列cid区分,39列pingfail
    rat_ind = excel_list.index("RatVector")
    cid_ind = excel_list.index("CID")
    ping_fail_ind = excel_list.index("pingfail")
    weak_signal_ind = excel_list.index("signal_low")
    high_latency_ind = excel_list.index("PingTimeVector")

    data_slices_list_rat = deal_data_by_ind(apn_data, rat_ind)[0]
    # print(data_slices_list_rat[0][0][rat_ind]) #debug   ,这里可以提前判断第一个值是4、5G
    # rat_flag = 3
    # if data_slices_list_rat[0][0][rat_ind] == 7:
    #     rat = 7
    data_all_rat = []
    for data_rat in data_slices_list_rat:
        # 这里的data_rat是[[],[]]结构
        data_all_rat.append((data_rat[0], map_line_data(data_rat[1])))

    data_all_pci = []
    data_slices_list_pci = deal_data_by_ind(apn_data, cid_ind)[0]
    for data_pci in data_slices_list_pci:
        data_all_pci.append((data_pci[0], map_line_data(data_pci[1])))

    data_all_pingfail = []
    data_slices_list_pingfail, pingfail_pos = deal_data_by_ind(apn_data, ping_fail_ind)  # 如果有问题去48行看看

    for data_pingfail in data_slices_list_pingfail:
        data_all_pingfail.append((data_pingfail[0], map_line_data(data_pingfail[1])))

    pingfail_list = []
    if len(pingfail_pos) % 2 == 0:  # DEBUG
        for pos in pingfail_pos[:-1]:  # 暂时这么写，要修改
            pingfail_list.append(apn_data[pos])
        pingfail_list.append(apn_data[pingfail_pos[-1] - 1])
        pingfail_lat_lon = map_line_data(pingfail_list)
    else:
        for pos in pingfail_pos[:-1]:
            pingfail_list.append(apn_data[pos])
        pingfail_lat_lon = map_line_data(pingfail_list)
    weak_signal_list = []
    for data_weak_signal in deal_data_by_ind(apn_data, weak_signal_ind)[0]:
        weak_signal_list.append((data_weak_signal[0], map_line_data(data_weak_signal[1])))
    high_latency_list = []
    for data_high_latency in deal_data_by_ind(apn_data, high_latency_ind)[0]:
        high_latency_list.append((float(data_high_latency[0]), map_line_data(data_high_latency[1])))
    html_file = drawLineOnMap(data_all_rat, data_all_pci, data_all_pingfail, pingfail_lat_lon, weak_signal_list, high_latency_list,
                  tiles=title, show_now=show_now)
    return html_file


def jfs_route_map_create(data_url, apn_type=4, csv_file=None, show_now=False):
    """
    根据提供的数据URL创建JFS路线映射，并返回一个链接用于访问生成的HTML文件。

    Args:
        data_url (str): 数据URL，用于获取网络状态数据。
        apn_type (int, optional): APN类型，默认为4。可以是1或4。
        csv_file (str, optional): CSV文件路径，默认为None。如果未提供，则通过data_url获取网络状态数据并生成CSV文件。
        show_now (bool, optional): 是否立即显示地图，默认为False。

    Returns:
        str: 生成的HTML文件的下载链接。

    Raises:
        Exception: 如果apn_type不是1或4，则引发异常。

    该函数首先检查是否提供了csv_file。如果没有提供，它会通过data_url获取网络状态数据并生成CSV文件。
    然后，它读取CSV文件中的数据，并根据apn_type选择相应的APN数据。
    接着，它使用map_wrapper函数根据提供的数据和tiles模板生成HTML文件，并可选择是否立即显示地图。
    最后，它将生成的HTML文件上传到某个服务器，并返回该文件的访问链接。
    如果在执行过程中发生任何异常，该函数将捕获异常并打印错误信息。
    """
    tiles = r'http://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7'
    try:
        if not csv_file:
            csv_file = get_network_status_csv(data_url=data_url)
        excel_list, apn1, apn4 = read_csv(csv_file)
        if apn_type == 1:
            apn = apn1
        elif apn_type == 4:
            apn = apn4
        else:
            raise Exception('apn_type must be 1 or 4')
        html_file = map_wrapper(excel_list, apn, tiles, show_now=show_now)
        link = upload_files_to_youzhi(local_file_path=html_file)
        return link
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/JFS_route_map/route_map_recovery.py")
        print(f'Error occurred while creating JFS route map: {str(e)}')


#######################################################################################################
if __name__ == "__main__":
    url = 'https://platform-vehicle.jiduprod.com/network/index?vin=L6T79P2N3RP185558&start_time=2024-11-03+17%3A47%3A04&end_time=2024-11-03+17%3A57%3A04'

    f = jfs_route_map_create(url, apn_type=4)
    print(f)

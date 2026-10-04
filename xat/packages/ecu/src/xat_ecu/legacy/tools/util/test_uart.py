# server 192.168.225.1 port 9090 protocol tcp ；  client 192.168.225.121 port 19090 protocol tcp ；  

import socket
from time import sleep


# 客户端代码
def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.225.1', 9090))
    while True:
        data = generate_nmea_data()
        s.sendall(data)
        print("send data:{}".format(data.decode()))
        sleep(1)
    s.close()

def generate_nmea_data(time_param:str ="061106.00", date_param:str ="221024", checksum=None):
    """
    生成NMEA0183协议格式的数据。
    
    Args:
        time_param (str, optional): 时间参数，默认为"061106.00"。用于构造NMEA0183数据的时间部分。  格式：hhmmss.ss  到10ms
        date_param (str, optional): 日期参数，默认为"221024"。用于构造NMEA0183数据的其他部分。     格式：ddmmyy
    
    Returns:
        str: 构造完成的NMEA0183协议格式的数据，编码为ASCII。
    
    """
    
    data_str = "$GPRMC,{},,,,,,,,{},,,,*".format(time_param, date_param)
    if checksum is None:
        checksum = calculate_nmea_checksum(data_str) # 计算校验和
    nmea_data = "{}{}{}".format(data_str, checksum, "\r\n")
    return nmea_data.encode(encoding="ascii")  # 使用ascii编码


def calculate_nmea_checksum(sentence):
    # 计算NMEA0183协议格式语句的校验和
    checksum = 0
    for char in sentence:
        if char!= '$' and char!= '*':
            checksum ^= ord(char)
        if char == "*":
            break
    return hex(checksum)[2:].upper()


if __name__ == '__main__':
    # # sentence = "$GPRMC,061106.00,,,,,,,,221024,,,,*"
    # sentence = "$GNRMC,061106.00,A,3121.553428,N,12113.350508,E,0.0,,180724,6.6,W,A,V*62"
    # checksum = calculate_nmea_checksum(sentence)
    # print("NMEA0183协议格式语句的校验和为：", checksum)
    client()


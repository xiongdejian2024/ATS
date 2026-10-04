import typing
from pathlib import Path


class TestTousnFrameLost:

    def __init__(self, asc_path: typing.Union[str, Path]) -> None:
        """
        功能说明：传入asc文件路径初始化
        """
        self.asc_path = asc_path

    def check_can(self, check_list: typing.List[typing.List[typing.Union[str, int]]]) -> None:
        """
        功能说明：检查can是否存在丢帧
        参数说明：
            param: check_list [[通道名称, 16进制帧名称, 发送Tx或接收Rx, 校验的位置], ... ]
            校验位置说明，如01 23 45 67 89 AB CD EF，若E是需要校验的则E是第14位
        """
        result = {}
        for item in check_list:
            _channel, _frame, _action, _ = item
            if _channel not in result:
                result[_channel] = {}
            if _frame not in result[_channel]:
                result[_channel][_frame] = {}
            result[_channel][_frame].update({
                _action: {
                    "last_data": "",
                    "crc": 0,
                    "total": 0,
                    "error": 0
                    }
                })
        with open(self.asc_path) as f1, open("can_restlt.txt", mode="w") as f2:
            [f1.__next__() for _ in range(5)]
            for line in f1:
                data = [data for data in line.split(" ") if data != ""]
                if len(data) < 9:
                    continue
                timestamp = data[0]
                action = data[3]
                if data[1] == "CANFD":
                    channel = data[2]
                    frame = data[4]
                    lenth = int(data[8])
                    signal = "".join(data[9:9 + lenth]) if lenth + 9 <= len(data) else None
                else:
                    channel = data[1]
                    frame = data[2]
                    lenth = int(data[5])
                    signal = "".join(data[6:6 + lenth]) if lenth + 6 <= len(data) else None
                if signal:
                    for item in check_list:
                        if item[0] == channel and item[1] == frame and item[2] == action:
                            result[channel][frame][action]["total"] += 1
                            crc = int(signal[item[3]: item[3]+1], 16)
                            current_data = f"can {channel}通道 {timestamp} {frame} {action} {signal} 校验第{item[3]}位：{crc}"
                            if result[channel][frame][action]["last_data"]:
                                if result[channel][frame][action]["crc"] + 1 != crc:
                                    result[channel][frame][action]["error"] += 1
                                    last_data = result[channel][frame][action]["last_data"]
                                    info = f"上一帧数据：{last_data}\n异常帧数据：{current_data}\n\n"
                                    print(info)
                                    f2.write(info)
                            result[channel][frame][action]["crc"] = -1 if crc == 14 else crc
                            result[channel][frame][action]["last_data"] = current_data
                            continue
            for channel, frams in result.items():
                for fram, actions in frams.items():
                    for action, data in actions.items():
                        total = data.get("total")
                        error = data.get("error")
                        percent = round(error / total * 100, 2) if total else 0
                        f2.write(f"can {channel}通道 {fram} {action} 总次数：{total} 异常次数：{error} 异常帧出现概率{percent}%\n")

    def check_fr(self, check_list: typing.List[typing.List[typing.Union[str, int]]]) -> None:
        """
        功能说明：检查fr是否存在丢帧
        参数说明：
            param: check_list [[solt_id, 发送Tx或接收Rx], ... ]
        """
        result = {}
        for item in check_list:
            solt_id, action = item
            if solt_id not in result:
                result[solt_id] = {}
            result[solt_id].update({
                action: {
                    "last_data": "",
                    "crc": 0,
                    "total": 0,
                    "error": 0
                    }
                })
        with open(self.asc_path) as f1, open("fr_result.txt", mode="w") as f2:
            [f1.__next__() for _ in range(5)]
            for line in f1:
                data = [data for data in line.split(" ") if data != ""]
                if len(data) < 10:
                    continue
                timestamp = data[0]
                action = data[9]
                frame = int(data[7], 16)
                crc = int(data[8], 16)
                lenth = int(data[17], 16)
                signal = "".join(data[18:18 + lenth]) if lenth + 18 <= len(data) else None
                if signal:
                    for item in check_list:
                        if item[0] == frame:
                            result[frame][action]["total"] += 1
                            current_data = f"fr {timestamp} {frame} {action} {signal} 校验：{crc}"
                            if result[frame][action]["last_data"]:
                                if result[frame][action]["crc"] + 1 != crc:
                                    result[frame][action]["error"] += 1
                                    last_data = result[frame][action]["last_data"]
                                    info = f"上一帧数据：{last_data}\n异常帧数据：{current_data}\n\n"
                                    print(info)
                                    f2.write(info)
                            result[frame][action]["crc"] = -1 if crc == 63 else crc
                            result[frame][action]["last_data"] = current_data
                            continue
            for solit, actions in result.items():
                for action, data in actions.items():
                    total = data.get("total")
                    error = data.get("error")
                    percent = round(error / total * 100, 2) if total else 0
                    f2.write(f"solit {solit} {action} 总次数：{total} 异常次数：{error} 异常帧出现概率{percent}%\n")
                

if __name__ == "__main__":
    tousn_can = TestTousnFrameLost(r"Can.asc") #替换为真实can.asc路径, 需要新增在大列表中继续添加小列表即可
    tousn_can.check_can([
        ["1", "0C0", "Tx", 1],    #0.02
        ["1", "260", "Rx", 3],    #0.02
        ["2", "050", "Tx", 10],   #0.01
        ["3", "083", "Tx", 2],    #0.01
        ["3", "125", "Rx", 3],    #0.015
        ["4", "16F", "Tx", 8],    #0.01
        ["5", "012", "Tx", 2],    #0.02
        ["5", "054", "Rx", 1],    #0.01
        ["7", "0C0", "Tx", 15],   #0.02
        ["7", "050", "Rx", 3],    #0.01
        ["8", "092", "Rx", 9],    #0.01
        ["9", "310", "Rx", 3],    #0.01
        ["10", "0F3", "Tx", 13],  #0.02
        ["10", "15A", "Rx", 13],  #0.02
    ])

    tousn_fr = TestTousnFrameLost(r"FlexRay.asc")  #替换为真实flexray.asc路径, 需要新增在大列表中继续添加小列表即可
    tousn_fr.check_fr([
        [20, "Tx"],
        [31, "Tx"],
        [46, "Tx"],
        [1, "Rx"]
        ])

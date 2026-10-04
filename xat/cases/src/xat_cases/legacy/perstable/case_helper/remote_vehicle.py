import time
import subprocess
import requests
import random

from xat_cases.legacy.tcam.tcam_back.rvcremote.remotectrl import RemoteCtrl


def get_vid():
    devices = subprocess.getstatusoutput("adb get-state")
    if "device" in devices:
        cmd = "adb shell getprop |grep vid"
        vid = subprocess.getstatusoutput(cmd)
        return vid[1].rpartition(":")[2].replace("[", "").replace("]", "")
    else:
        return False


class RemoteVehicle:
    def __init__(self, tel=15201537076):
        self.vid = get_vid() if get_vid() is True else "72c2e535dbf174d24be5268bdf459798"
        self.remote_control = RemoteCtrl(self.vid, tel)

    def start_rvc_lock_control(self):
        """
        随机发送一次远控接闭锁请求
        """
        op = random.randint(1, 3)
        self.remote_control.rvc_lock_control(op)

    def start_rvc_panic_vehicle(self):
        """
        随机发送一次远控寻车
        """
        self.remote_control.rvc_panic_vehicle(op=random.randint(-1, 2))

    def start_rvc_open_windows(self):
        """
        随机打开全部车窗开合度
        """
        frontLeft = random.randint(0, 100)
        frontRight = random.randint(0, 100)
        secondRowLeft = random.randint(0, 100)
        secondRowRight = random.randint(0, 100)
        self.remote_control.rvc_open_windows(frontLeft=frontLeft, frontRight=frontRight, secondRowLeft=secondRowLeft,
                                             secondRowRight=secondRowRight)

    def start_rvc_close_windows(self):
        """
        随机关闭全部窗户的开合度
        """
        frontLeft = random.randint(0, 100)
        frontRight = random.randint(0, 100)
        secondRowLeft = random.randint(0, 100)
        secondRowRight = random.randint(0, 100)
        self.remote_control.rvc_close_windows(frontLeft=frontLeft, frontRight=frontRight, secondRowLeft=secondRowLeft,
                                              secondRowRight=secondRowRight)

    def start_rvc_tailgate_control(self):
        """
        开启或关闭后尾门
        """

        self.remote_control.rvc_tailgate_control(op=random.randrange(-1, 1, 2))

    def start_rvc_cocked_tailgate(self):
        """
        随机开启尾门开合度
        """
        self.remote_control.rvc_cocked_tailgate(position=random.randint(0, 100))
        requests.session()

    # def start_rvc_charge_soc_settings(self):
    #     """
    #     随机设置充电上线
    #     """
    #     self.remote_control.rvc_charge_soc_settings(max=random.randint(500, 1000))

    def start_rvc_ac_control(self):
        """
        随机开启关闭空调，并设置一个随机的温度
        """
        op = random.randrange(-1, 1, 2)
        temp = random.randrange(160, 280, 5)
        self.remote_control.rvc_ac_control(op, temp)

    # def start_rvc_seat_heat(self):
    #     """
    #     随机对主驾座椅和副驾座椅加热开启
    #     """
    #     master = random.randint(0, 3)
    #     secondary = random.randint(0, 3)
    #     self.remote_control.rvc_seat_heat(master, secondary)

    def start_rvc_driver_seat_heat(self):
        """
        随机主驾座椅加热挡位
        """
        self.remote_control.rvc_driver_seat_heat(level=random.randint(-1, 3))

    def start_rvc_passenger_seat_heat(self):
        """
        随机副驾座椅加热挡位
        """
        self.remote_control.rvc_passenger_seat_heat(level=random.randint(-1, 3))

    # def start_rvc_steering_wheel_heat(self):
    #     """
    #     方向盘加热
    #     """
    #     self.rvc_steering_wheel_heat()

    # def start_rvc_charge_operation(self):
    #     """
    #     随机开启关闭充电开关
    #     """
    #     op = random.randrange(-1, 1, 2)
    #     self.remote_control.rvc_charge_operation(op)

    def start_rvc_charge_Lidgate(self):
        """
        随机充电口盖开启关闭
        """
        op = random.randrange(-1, 1, 2)
        self.remote_control.rvc_charge_Lidgate(op)

    # def start_rvc_door_full_control(self):
    #     self.remote_control.rvc_door_full_control()

    def start_rvc_steering_wheel_heat(self):
        """
        随机方向盘加热
        """
        self.remote_control.rvc_steering_wheel_heat(level=random.randint(0, 3))

    def start_rvc_defrost_control(self):
        """
        随机开启关闭空调除霜
        """
        self.remote_control.rvc_defrost_control(op=random.randrange(-1, 1, 2))


def range_control(stop_event, Traversal_random=True, interval_time=10, time_out=1):
    """
        获取 RemoteVehicle 类中所有的方法
        :param Traversal_random:布尔值，如果为假循环执行类的所有方法，为真随机执行类的一个方法
        :param interval_time:运行方法间隔时间
        :param time_out:超时时间h
        """
    import time
    start_time = time.time()
    Vehicle = RemoteVehicle()
    while not stop_event.is_set():

        methods = [method for method in dir(Vehicle) if
                   callable(getattr(Vehicle, method)) and not method.startswith("__")]
        # print(len(methods))
        if not Traversal_random:
            for method in methods:
                time.sleep(interval_time)
                getattr(Vehicle, method)()
                code = Vehicle.remote_control.sendcmd()
                if code == 600007:
                    time.sleep(interval_time)
                    continue
        elif Traversal_random:
            time.sleep(interval_time)
            random_method = random.choice(methods)
            print(random_method)
            getattr(Vehicle, random_method)()
            code = Vehicle.remote_control.sendcmd()
            if code == 600007:
                time.sleep(interval_time)
                continue

        end_time = time.time()
        if end_time - start_time >= float(time_out) * 3600:
            break


if __name__ == '__main__':
    pass
    # range_control(1,True,1,20)
    # driver = RemoteVehicle()
    # driver.start_rvc_defrost_control()
    # driver.remote_control.sendcmd()
    # range_control(True)
    # print(driver.get_vid())
    # driver.start_rvc_ac_control()
    # time.sleep(1)
    # driver.remote_control.sendcmd()
    # print(driver.remote_control.get_token())

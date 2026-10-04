#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BaseRemoteSubscribe:
    slotID = None
    status = None
    cyclesType = None
    AppointWeekday = ""
    startTime = 0
    cmdCode = None
    cmdDetail = ""

    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime) -> None:
        self.slotID = slotID
        self.status = status
        self.cyclesType = cyclesType
        self.AppointWeekday = AppointWeekday
        self.startTime = startTime
class battery_pack_heat_Subscribe(BaseRemoteSubscribe):
    """
    电池预加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "battery_pack_heat"
        self.cmdDetail = '{"battery_pack_heat":{"op":1}}'


class conditional_ac_control_Subscribe(BaseRemoteSubscribe):
    """
    预约自动空调
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "conditional_ac_control"
        self.cmdDetail = '{"conditional_ac_control":{"op":1,"temp":195,"modeParams":[{"usageMode":69632,"CmdParams":[{"temperature":{"left":100,"right":400},"cmd":3},{"temperature":{"left":400,"right":9990},"cmd":2},{"temperature":{"left":-9990,"right":100},"cmd":1}]},{"usageMode":273,"CmdParams":[{"temperature":{"left":-9990,"right":9990},"cmd":3}]}]}}'

class ac_control_Subscribe(BaseRemoteSubscribe):
    """
    预约空调
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime,temp:int =230):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "ac_control"
        self.cmdDetail = '{{"ac_control":{{"op":1,"temp":{}}}}}'.format(temp)

class driver_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约主驾座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "driver_seat_heat"
        self.cmdDetail = f'{{"driver_seat_heat":{{"level":{level}}}}}'

class passenger_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约副驾座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "passenger_seat_heat"
        self.cmdDetail = f'{{"passenger_seat_heat":{{"level":{level}}}}}'

class rear_left_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约左后座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_left_seat_heat"
        self.cmdDetail = f'{{"rear_left_seat_heat":{{"level":{level}}}}}'

class rear_right_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约右后座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_right_seat_heat"
        self.cmdDetail = f'{{"rear_right_seat_heat":{{"level":{level}}}}}'

class driver_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约主驾座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "driver_seat_vent"
        self.cmdDetail = f'{{"driver_seat_vent":{{"level":{level}}}}}'

class passenger_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约副驾座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "passenger_seat_vent"
        self.cmdDetail = f'{{"passenger_seat_vent":{{"level":{level}}}}}'

class rear_left_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约左后座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_left_seat_vent"
        self.cmdDetail = f'{{"rear_left_seat_vent":{{"level":{level}}}}}'

class rear_right_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约右后座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_right_seat_vent"
        self.cmdDetail = f'{{"rear_right_seat_vent":{{"level":{level}}}}}'

class conditional_passenger_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约主驾自动座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "passenger_seat_heat"
        self.cmdDetail = '{"passenger_seat_heat":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_driver_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约副驾自动座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "driver_seat_heat"
        self.cmdDetail = '{"passenger_seat_heat":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_rear_left_seat_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约左后自动座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_left_seat_heat"
        self.cmdDetail = '{"rear_left_seat_heat":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_rear_right_seat_heatSubscribe(BaseRemoteSubscribe):
    """
    预约右后自动座椅加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_right_seat_heat"
        self.cmdDetail = '{"rear_right_seat_heat":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_driver_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约主驾自动座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "driver_seat_vent"
        self.cmdDetail = '{"driver_seat_vent":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_passenger_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约副驾自动座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "passenger_seat_vent"
        self.cmdDetail = '{"passenger_seat_vent":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_rear_left_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约左后自动座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_left_seat_vent"
        self.cmdDetail = '{"rear_left_seat_vent":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class conditional_rear_right_seat_vent_Subscribe(BaseRemoteSubscribe):
    """
    预约右后自动座椅通风
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "rear_right_seat_vent"
        self.cmdDetail = '{"rear_right_seat_vent":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":100,"right":9999}},{"level":1,"temperature":{"left":100,"right":9999},"outsideTemperature":{"left":-9999,"right":100}},{"level":2,"temperature":{"left":50,"right":100},"outsideTemperature":{"left":-9999,"right":100}},{"level":3,"temperature":{"left":-9999,"right":50},"outsideTemperature":{"left":-9999,"right":100}}]}}'

class steering_wheel_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约方向盘加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime, level:int = 1):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "steering_wheel_heat"
        self.cmdDetail = f'{{"steering_wheel_heat":{{"level":{level}}}}}'

class conditional_steering_wheel_heat_Subscribe(BaseRemoteSubscribe):
    """
    预约智能方向盘加热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "steering_wheel_heat"
        self.cmdDetail = '{"steering_wheel_heat":{"level":9,"autoParams":[{"level":-1,"temperature":{"left":150,"right":9999},"outsideTemperature":{"left":150,"right":9999}},{"level":1,"temperature":{"left":150,"right":9999},"outsideTemperature":{"left":-9999,"right":150}},{"level":2,"temperature":{"left":100,"right":150},"outsideTemperature":{"left":-9999,"right":150}},{"level":3,"temperature":{"left":-9999,"right":100},"outsideTemperature":{"left":-9999,"right":150}}]}}'

class ac_rapid_cooling_Subscribe(BaseRemoteSubscribe):
    """
    预约极速制冷
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "ac_rapid_cooling"
        self.cmdDetail = '{"ac_rapid_cooling":{"op":1}}'

class ac_rapid_heating_Subscribe(BaseRemoteSubscribe):
    """
    预约极速制热
    """
    def __init__(self, slotID, status, cyclesType, AppointWeekday, startTime):
        super().__init__(slotID, status, cyclesType, AppointWeekday, startTime)
        self.cmdCode = "ac_rapid_heating"
        self.cmdDetail = '{"ac_rapid_heating":{"op":1}}'
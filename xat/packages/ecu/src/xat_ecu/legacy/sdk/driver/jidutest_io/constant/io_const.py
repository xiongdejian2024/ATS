from enum import Enum


NiDeviceType = Enum(
    "NiDeviceType",
    (
        "cDAQ",
        "cModule_AI",
        "cModule_AO",
        "cModule_CI",
        "cModule_CO",
        "cModule_DI",
        "cModule_DO",
    ),
)

class DOOR(Enum):
    OPEN = True
    CLOSE= False

class HOOD(Enum):
    CLOSE = True
    OPEN= False

class TRUNK(Enum):
    CLOSE = True
    OPEN= False

class SEAT(Enum):
    OCCUPY = True
    NOT_OCCUPY= False

class BRAKE_PEDAL(Enum):
    ON = True
    OFF= False

class SWITCH(Enum):
    PRESS = True
    RELEASE = False

class LINE(Enum):
    ACTIVE = True
    INACTIVE = False


class WiperWashing(Enum):
    CLOSE = True
    OPEN = False

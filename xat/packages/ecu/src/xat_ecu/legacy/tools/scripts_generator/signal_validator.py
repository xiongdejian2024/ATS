import glob
import sys
import cantools
import importlib
from decimal import Decimal
from xat_ecu.legacy.sdk.can_lin.pcan_const import *



def validate_signal(bus_name=None, msg_name=None, signal_name=None, signal_value=None,
                    project_type="bgm", veh_type="force"):
    if project_type.lower() == "bgm":
        dut_dir = "../../sdk/dut/bgm/"
    elif project_type.lower() == "cgw":
        dut_dir = "../../sdk/dut/cgw/"
    else:
        return False, "project type not found"

    bus_type = ""
    if bus_name.lower() in PcanConst.BGM_CAN_BUS_LIST:
        bus_type = "dbc"
    elif bus_name.lower() in PcanConst.BGM_LIN_BUS_LIST:
        bus_type = "ldf"
    else:
        return False, "bus name '"+bus_name+"' not found"

    cls_file_path = dut_dir + bus_type + "_cls/" + veh_type.lower() + "/*"
    dir_list = glob.glob(cls_file_path)
    list.sort(dir_list)
    if project_type=="bgm":
        for cls_name in dir_list:
            if "v0_1_8" in cls_name:
                cls_dir_name = cls_name
    else:
        cls_dir_name = dir_list[-1]
    cls_list = glob.glob(cls_dir_name + "/*.py")
    file_name = ""
    for i in cls_list:
        if bus_name.lower() in i:
            file_name = i[:-3].replace("../", "").replace("/", ".")
    handle_moudle = importlib.import_module(file_name)
    try:
        float(signal_value)
        # Decimal(signal_value) % Decimal('0.1')
        cls_file_path = dut_dir +"data/"+ bus_type + "_file/" + veh_type.lower() + "/*"
        dir_list = glob.glob(cls_file_path)
        list.sort(dir_list)
        cls_dir_name = dir_list[-1]
        cls_list = glob.glob(cls_dir_name + "/*")
        file_name = ""
        minimum = 0
        maximum = 0
        scale = 0
        offset = 0
        is_scale_valid = False
        is_range_valid = False
        feeback = ""
        for cls_file in cls_list:
            if bus_name.lower() in cls_file.lower():
                file_name = cls_file
        if bus_type == "dbc":
            db = cantools.db.load_file(file_name)
            signal_retrieved = db.get_message_by_name(msg_name).get_signal_by_name(signal_name)
            is_scale_valid = False
            is_range_valid = False
            minimum = signal_retrieved.minimum
            maximum = signal_retrieved.maximum
            scale = signal_retrieved.scale
            offset = signal_retrieved.offset

        else:
            fhandle = open(file_name, 'r').readlines()
            for i in range(0, len(fhandle)):
                if "Vtsig_"+signal_name+" {" in fhandle[i]:
                    line = fhandle[i+1]
                    data = line.replace(" ", "").replace("\n", "").split(',')
                    minimum = Decimal(data[1])
                    maximum = Decimal(data[2])
                    scale = Decimal(data[3])
                    offset = Decimal(data[4][:-1])

        # check if signal_value can be divided by scale without remindant
        if round(Decimal(signal_value) / Decimal(scale), 10) == \
                round(round(Decimal(signal_value) / Decimal(scale), 10)):
            is_scale_valid = True
        if (minimum <= Decimal(signal_value) + offset <= maximum):
            is_range_valid = True
        if is_range_valid and is_scale_valid:
            return True, "%s.%s.%s=%s signal VALID in Scale %s, Offset %s, Minimum %s, Maximum %s" \
                   % (bus_name.lower().capitalize(), msg_name, signal_name, signal_value,
                      str(scale), str(offset),
                      str(minimum), str(maximum))
        elif not is_scale_valid and is_range_valid:
            return False, "%s.%s.%s=%s signal SCALE INVALID in Scale %s, Offset %s, Minimum %s, Maximum %s，" \
                          "signal value should be divided by scale without remainder" \
                   % (bus_name.lower().capitalize(), msg_name, signal_name, signal_value,
                      str(scale), str(offset),
                      str(minimum), str(maximum))
        elif is_scale_valid and not is_range_valid:
            return False, "%s.%s.%s=%s signal RANGE INVALID in Scale %s, Offset %s, Minimum %s, Maximum %s，" \
                          "(signal value+Offset) should in range [minimum, maximum]" \
                   % (bus_name.lower().capitalize(), msg_name, signal_name, signal_value,
                      str(scale), str(offset),
                      str(minimum), str(maximum))
        else:
            return False, "%s.%s.%s=%s signal RANGE AND SCALE INVALID in Scale %s, Offset %s, " \
                          "Minimum %s, Maximum %s，" \
                          "signal value should be divided by scale without remainder, " \
                          "(signal value+Offset) should in range [minimum, maximum]" \
                   % (bus_name.lower().capitalize(), msg_name, signal_name, signal_value,
                      str(signal_retrieved.scale), str(signal_retrieved.offset),
                      str(signal_retrieved.minimum), str(signal_retrieved.maximum))
    except:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/signal_validator.py")
        try:
            if signal_value:
                eval("handle_moudle.%s.%s.%s.%s" % (bus_name.lower().capitalize(), msg_name,
                                                               signal_name, signal_value))
                return True, "found signal value %s.%s.%s=%s" % \
                       (bus_name.lower().capitalize(), msg_name, signal_name, signal_value)
            elif signal_name:
                eval("handle_moudle.%s.%s.%s" % (bus_name.lower().capitalize(), msg_name,
                                                               signal_name))
                return True, "found signal name %s.%s.%s" % \
                       (bus_name.lower().capitalize(), msg_name, signal_name)
            elif msg_name:
                eval("handle_moudle.%s.%s" % (bus_name.lower().capitalize(), msg_name))
                return True, "found message name %s.%s" % \
                       (bus_name.lower().capitalize(), msg_name)
            elif bus_name:
                eval("handle_moudle.%s" % (bus_name.lower().capitalize()))
                return True, "found bus name %s" % \
                       (bus_name.lower().capitalize())
        except Exception as err:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/signal_validator.py")
            return False, err

if __name__ == "__main__":
    validate_signal(bus_name="bodycan", msg_name="BCU_04", signal_name="VehSpd", signal_value=20)
    path = "../../../zzzz.py"
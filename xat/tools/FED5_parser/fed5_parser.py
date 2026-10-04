# -*- coding: utf-8 -*-
"""
@File        : fed5_parser.py
@Author      : lei.tao
@Time        : 2023/06/26 23:32
@Description : 
@Examples    : FED5 data parser
"""
import time


SYSTEM_EVENT = {"01": "Power On Reset", "02": "Smu configuration fault", "03": "NVM operation fault"}
CLOCK_FAILURE_EVENT = {"01": "Clock SYSPLL Failure", "02": "Clock PERPLL Failure", "03": "Clock PLLx Threshold Failure", "04": "Clock PLLx/Fspb Alive Failure", "05": "Clock Fosc Threshold Failure", "06": "Clock Fosc NOT ALIVE Failure"}
POWER_FAILURE_EVENT = {"01": "Power VDD UnderVoltage Failure", "02": "Power VDD OverVoltage Failure", "03": "Power VDDP3 UnderVoltage Failure", "04": "Power VDDP3 OverVoltage Failure", "05": "Power VEXT OverVoltage Failure", "06": "Power VEXT UnderVoltage Failure", "07": "Power VDDPD UnderVoltage Failure", "08": "Power VDDPD OverVoltage Failure", "09": "Power VEVRSB UnderVoltage Failure", "0A": "Power VEVRSB OverVoltage Failure", "0B": "Power VDDM UnderVoltage Failure", "0C": "Power VDDM OverVoltage Failure"}
LOCKSTEP_FAILURE_EVENT = {"01": "Lockstep Pflash0 Read error", "02": "Lockstep Pflash1 Read error", "03": "Lockstep Pflash2 Read error", "04": "Lockstep CPU0 Read error", "05": "Lockstep CPU1 Read error", "06": "Lockstep CPU2 Read error"}
SAFETYFF_FAILURE_EVENT = {"01": "SafetyFF Power FlipFlop error", "02": "LSafetyFF PLLx FlipFlop error", "03": "SafetyFF SMU FlipFlop error", "04": "SafetyFF MTU FlipFlop error", "05": "SafetyFF SCU/SRU FlipFlop error", "06": "SafetyFF CCU FlipFlop error"}
RAMECC_FAILURE_EVENT = {"02": "SRAM ECC CPU0PSPR error", "03": "SRAM ECC CPU1PSPR error", "04": "SRAM ECC CPU2PSPR error", "05": "SRAM ECC CPU2DSPR error", "06": "SRAM ECC CPU1DSPR error", "07": "SRAM ECC CPU2DSPR error", "08": "SRAM ECC ERAY error", "09": "SRAM ECC GTM error", "0A": "SRAM ECC GTM error"}
PFLASHECC_FAILURE_EVENT = {"01": "Pflash NVM Safety endinit Protction Violation Error", "02": "Multiple byte Error Detection Tracking Buffer Full", "03": "PFlash ECC Correction logic Error", "04": "PFlash EDC Comparator Error", "05": "Pflash CPU FLASHCON Configuration Error", "06": "Pflash CPU FLASHCON stored Configuration Error", "07": "Pflash0 Access Violation", "08": "Pflash1 Access Violation", "09": "Pflash2 Access Violation", "0A": "Pflash2 SRI Address Error", "0B": "pflash Multibit error"}



def get_data(r_data, dl):
    data = r_data[:dl]
    raw_data = r_data[dl:]
    return data, raw_data


def parser(file):
    data = []
    if "\n" in file:
        if file.split('\n')[0][-1] == ' ':
            file = file.replace("\n", "")
        else:
            file = file.replace("\n", " ")
    elif "-" in file:
        file = file.replace("-", " ")
    elif "Complete Response: " in file:
        file = file.split("1002 62 FE D5 ")[-1]
    elif file.split(' ')[:4] == ['1002', '62', 'FE', 'D5']:
        file = file.split('D5 ')[-1]
        
    data1 = file.strip().split(' ')
    if len(data1) < 104:
        return "Response Messages Length Error"
    elif len(data1) > 104:
        data, err = get_data(data1, 104)
    else:
        data = data1
    #开始解析数据
    #print(data)
    parse_info_str = ""
    parse_info_str += "=" * 40 + "FED5 Data" + "=" * 40 + "\n"
    try:
        counter = ''
        for i in range(4):
            counter += data[i]
        count_id = int(counter, 16)
        parse_info_str += f"SYSSUP_RESET_COUNTER                  : {count_id}, original value: " + f"{' '.join(data[:4])}" + "\n"
        
        timestamp = ''
        for i in range(4,8):
            timestamp += data[i]
        timestamp_id = int(timestamp, 16)
        parse_info_str += "SYSSUP_RESET_TIMESTAMP                : {}, original value: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_id)), ' '.join(data[4:8]))
        
        if data[8] in SYSTEM_EVENT.keys():
            system_event = SYSTEM_EVENT[data[8]]
            parse_info_str += f"SYSSUP_SYSTEM_EVENT                   : {system_event}, original value: {data[8]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_SYSTEM_EVENT                   : {data[8]}" + "\n"

        if data[9] == "01":
            parse_info_str += f"SYSSUP_EXT_WATCHDOG_EVENT             : {data[9]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_EXT_WATCHDOG_EVENT             : {data[9]}" + "\n"
        
        if data[10] == "01":
            parse_info_str += f"SYSSUP_SW_RESET_EVENT                 : {data[10]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_SW_RESET_EVENT                 : {data[10]}" + "\n"

        parse_info_str += f"SYSSUP_TRAP_CLASS                     : {data[11]}" + "\n"
        parse_info_str += f"SYSSUP_TRAP_TRAPID                    : {data[12]}" + "\n"
        parse_info_str += f"SYSSUP_TRAP_LOG                       : {' '.join(data[13:73])}" + "\n"
        
        if data[75] in CLOCK_FAILURE_EVENT.keys():
            clock_event = CLOCK_FAILURE_EVENT[data[75]]
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {clock_event}, original value: {data[75]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {data[75]}" + "\n"
        
        if data[76] in POWER_FAILURE_EVENT.keys():
            power_event = POWER_FAILURE_EVENT[data[76]]
            parse_info_str += f"SYSSUP_POWER_FAILURE_EVENT            : {power_event}, original value: {data[76]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {data[76]}" + "\n"

        if data[77] in LOCKSTEP_FAILURE_EVENT.keys():
            lockstep_event = LOCKSTEP_FAILURE_EVENT[data[77]]
            parse_info_str += f"SYSSUP_LOCKSTEP_FAILURE_EVENT         : {lockstep_event}, original value: {data[77]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {data[77]}" + "\n"
        
        if data[78] in SAFETYFF_FAILURE_EVENT.keys():
            safetyff_event = SAFETYFF_FAILURE_EVENT[data[78]]
            parse_info_str += f"SYSSUP_SAFETYFF_FAILURE_EVENT         : {safetyff_event}, original value: {data[78]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {data[78]}" + "\n"
        
        if data[79] in RAMECC_FAILURE_EVENT.keys():
            ramecc_event = RAMECC_FAILURE_EVENT[data[79]]
            parse_info_str += f"SYSSUP_RAMECC_FAILURE_EVENT           : {ramecc_event}, original value: {data[79]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {data[79]}" + "\n"

        parse_info_str += f"SYSSUP_RAMECC_SSH_INSTANCE            : {data[80]}" + "\n"
        parse_info_str += f"SYSSUP_RAMECC_ERROR_LOCATION          : {' '.join(data[81:83])}" + "\n"
        parse_info_str += f"SYSSUP_FUNCTIONAL_SAFETY_FAULT_COUNTER: {' '.join(data[83:85])}" + "\n"

        if data[85] in PFLASHECC_FAILURE_EVENT.keys():
            ramecc_event = PFLASHECC_FAILURE_EVENT[data[85]]
            parse_info_str += f"SYSSUP_PFLASHECC_FAILURE_EVENT        : {ramecc_event}, original value: {data[85]}" + "\n"
        else:
            parse_info_str += f"SYSSUP_CLOCK_FAILURE_EVENT            : {data[85]}" + "\n"
        
        parse_info_str += f"SYSSUP_PFLASHECC_ERROR_LOCATION       : {' '.join(data[86:90])}" + "\n"
        parse_info_str += f"SYSSUP_OS_FAULT_EVENT                 : {data[90]}" + "\n"
        parse_info_str += f"SYSSUP_RESET_REGISTER_VALUE           : {' '.join(data[92:96])}" + "\n"
        parse_info_str += f"SYSSUP_MCUPerRSTCallLocation          : {' '.join(data[96:100])}" + "\n"
        parse_info_str += f"SYSSUP_FSMODE                         : {data[101]}" + "\n"
        parse_info_str += f"SYSSUP_TIC10024DET                    : {data[102]}" + "\n"
        parse_info_str += f"SYSSUP_SOFT_RESET                     : {data[103]}" + "\n"
        
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/FED5_parser/fed5_parser.py")
        raise e
    
    finally:
        return parse_info_str



if __name__ == '__main__':
    # aa = "10 02 62 F1 62 01 00 00 01 01 01 00 07 21 00 00 00 00 00 00 00 00 00 00 00 00 00 05 3F 14 00 00 07 15 00 3E 74 8A B8 00 00 65 01 99 99 00 00 00 00 38 00 00 07 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 00 07 21 06 06 06 06 06 0A 00 00 00 00 0A 0B 00 00 00 40 00 00 07 21 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    
    # data = parser(aa)
    # print(data)
    
    import sys
    if len(sys.argv) == 2:
        info_file = parser(sys.argv[1])
        print(info_file)

    else:
        print("Please input the FED5 bytes")
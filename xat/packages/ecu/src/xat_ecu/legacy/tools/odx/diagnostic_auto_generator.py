#!/usr/bin/python3

import sys
import os
from xat_ecu.legacy.common.logger import logger
import json
from xat_ecu.legacy.sdk.diagnosis.uds_const import *
from xat_ecu.legacy.sdk.diagnosis.uds_parsing_and_composition import DiagStruct
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding


def diagnostic_auto_generator_sa():

    with open("ecu_simulator/sdk/odx_json/diag_json/sa_diag_did.json", "r") as f:
        sa_diag_did = json.load(f)
    f.close()
    diag_struct = DiagStruct()
    requests = sa_diag_did.get("REQUESTS")
    pos_responses = sa_diag_did.get("POS-RESPONSES")

    with open("ecu_simulator/sdk/diagnostic_odx_client_simulator_app_auto.py", "w") as diag_app_auto:
        diag_app_auto.write("#!/usr/bin/python3\n")
        diag_app_auto.write("\n")
        diag_app_auto.write("# Automatic generation by ecu_simulator/tools/odx/diagnostic_auto_generator.py\n")
        diag_app_auto.write("\n")
        diag_app_auto.write("\n")
        diag_app_auto.write("class Diagnostic_Odx_Client_Sim_App_Auto:\n")
        diag_app_auto.write("   def __init__(self):\n")
        diag_app_auto.write("       pass\n")
        diag_app_auto.write("\n")

        for service_key in requests.keys():
            service = requests.get(service_key)
            for data_key in service.keys():
                data = diag_struct.composition_data("REQUEST", service_key, [data_key])
                data = DataTypeHanding.intlist_to_hexliststr(data)
                function_name = service_key + "_" + data_key + "_auto"
                function_name = function_name.lower()
                diag_app_auto.write("   def {}(self):\n".format(function_name))
                diag_app_auto.write("       self.client_sim.send_data({})\n".format(data))
                diag_app_auto.write("\n")

        # for service_key in pos_responses:
        #     service = requests.get(service_key)
        #     for data_key in service:
        #         data = diag_struct.composition_data("REQUESTS", service, [data_key])
        #         function_name = service_key + "_" + data_key + "_aute"
        #         function_name = function_name.lower()
        #         diag_app_auto.write("   def {}(self):\n".format(function_name))
        #         diag_app_auto.write("       self.client_sim.send_data({})\n".format(data))
        #         diag_app_auto.write("\n")


    diag_app_auto.close()
    print("================end=================")


if __name__ == '__main__':
    # work path: compass/
    diagnostic_auto_generator_sa()


#!/usr/bin/python3
import sys
# from sys import argv
import os
import json
import xmltodict
# from ecu_simulator.common.logger import logger


def pdx_to_py():
    os.system("unzip -o -d ./xat_ecu/legacy/sdk/data/pdx_file/odx ./xat_ecu/legacy/sdk/data/pdx_file/NIO_NT2_V0.4_210702.pdx")
    dirroot = "./xat_ecu/legacy/sdk/data/pdx_file/odx"
    for dirpath,dirnames,filenames in os.walk(dirroot):
        for file in filenames:
            dirfile = os.path.join(dirpath, file)
            if ".odx" in dirfile:
                odx_xml_to_json(dirfile)

def odx_xml_to_json(odxfile):
    main_name = (odxfile.split("/")[-1]).split(".")[0]
    if not os.path.exists("./xat_ecu/legacy/sdk/odx_json"):
        os.system("mkdir ./xat_ecu/legacy/sdk/odx_json")
    json_name = "{}_dignostic_data.json".format(main_name.lower())
    json_file_path = "./xat_ecu/legacy/sdk/odx_json/{}".format(json_name)

    with open(odxfile, "r", encoding='utf-8') as odx_xml_file:
        odx_xml_str = odx_xml_file.read()
        odx_xml_to_dict = xmltodict.parse(odx_xml_str)
        # print(type(odx_xml_to_dict))
        print(isinstance(odx_xml_to_dict, dict))
    odx_xml_file.close()

    with open(json_file_path, "w", encoding='utf-8') as json_file:
        json.dump(odx_xml_to_dict, json_file, indent=4)
    json_file.close()

    print("{} File created successfully".format(main_name))

def get_dlc_sd_udsservices_dignastic_data_json():
    pass

if __name__ == '__main__':
    # work path: compass/
    pdx_to_py()


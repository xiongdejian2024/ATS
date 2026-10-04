import os

from xat_ecu.legacy.sdk.dut.cgw.cgw_pcan import CgwPcan
from xat_ecu.legacy.sdk.can_lin.pcan_const import PcanConst
from xat_ecu.legacy.tools.scripts_generator.dbc_core import DbcCore
from xat_ecu.legacy.tools.scripts_generator.ldf_core import LdfCore


class BusTypeFilesParser:
    def __init__(self, veh_type, bus_type_enum, bus_file_ext_dir, bus_types_bus_parser_cls_obj_dicts):
        self.veh_type = veh_type

        self.bus_type_enum = bus_type_enum

        self.bus_file_ext_dir = bus_file_ext_dir

        self._bus_type_bus_parser_cls_obj_dicts = \
            None if bus_types_bus_parser_cls_obj_dicts is None else \
            bus_types_bus_parser_cls_obj_dicts[bus_type_enum.value]

        self.bus_names_to_bus_file_ext_filenames_map = \
            CgwPcan.get_bus_names_to_bus_filename_map_dict(dbc_ldf_folder=bus_file_ext_dir, veh_type=self.veh_type)

        self.bus_file_ext_filenames_to_bus_names_map = \
            {bus_file_name: bus_name.capitalize()
             for bus_name, bus_file_name in self.bus_names_to_bus_file_ext_filenames_map.items()}

        self.all_msgs_for_bus_type_dict = {}

        self.bus_name = None

        self.class_hierarchy_def_file_lines = []

    def get_cls_name(self, bus_file_name):
        try:
            cls_name = self.bus_file_ext_filenames_to_bus_names_map[bus_file_name]
        except KeyError:
            cls_name = None

        return cls_name

    def get_all_messages_for_bus_type(self):
        """
        Parse all messages and returns a list of all messages parsed out of the bus files

        :return:    all_msgs_for_bus_type_dict
        :rtype:     dict
        """
        if len(self.all_msgs_for_bus_type_dict) > 0:
            return self.all_msgs_for_bus_type_dict

        bus_file_names = os.listdir(self.bus_file_ext_dir)

        for bus_file_name in bus_file_names:
            bus_name = self.get_cls_name(bus_file_name)

            if bus_name is None:
                continue
            # Special case for Info CAN bus
            elif 'info' in bus_name.lower():
                bus_name = 'info'
            else:
                bus_name = bus_name.lower()

            bus_file_path = os.path.join(self.bus_file_ext_dir, bus_file_name)

            if self.bus_type_enum.value == PcanConst.BusType.CAN.value:
                bus_obj = DbcCore(bus_name, bus_file_path, self._bus_type_bus_parser_cls_obj_dicts)
            elif self.bus_type_enum.value == PcanConst.BusType.LIN.value:
                bus_obj = LdfCore(bus_name, bus_file_path, self._bus_type_bus_parser_cls_obj_dicts)
            else:
                raise RuntimeError('Unknown bus_type_enum = "{}"'.format(self.bus_type_enum))

            all_msgs_on_this_bus_dict = bus_obj.get_all_msg_dicts_on_bus()

            #        vvvvvvvvvvvvvvvvvvvv this_msg_info_on_all_buses vvvvvvvvvvvvvvvvvvvvvvvv
            # {1027: {"Adc1": {lots o' stuff on ADC bus}, "Body": {lots o' stuff on bodycan bus}}
            #        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            #
            for msg_id, lots_o_stuff_for_this_msg in all_msgs_on_this_bus_dict.items():
                if msg_id not in self.all_msgs_for_bus_type_dict:
                    self.all_msgs_for_bus_type_dict[msg_id] = {}
                else:
                    a = 1

                this_msg_info_on_all_buses = self.all_msgs_for_bus_type_dict[msg_id]

                if bus_name in this_msg_info_on_all_buses:
                    raise RuntimeError("msg_id({}) found twice on Bus({}}!".format(msg_id, bus_name))
                else:
                    this_msg_info_on_all_buses[bus_name] = lots_o_stuff_for_this_msg

            # The above loop replaces this evil line, which unfortunately stomps the msg_id entry
            # on one bus, when a second bus has the same msg_id :-( :-(.
            # self.all_msgs_for_bus_type_dict.update(all_msgs_on_this_bus_dict)

        return self.all_msgs_for_bus_type_dict

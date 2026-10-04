# -*- coding: utf-8 -*-
"""
@File        : arxml_reader.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/2/19 13:12
@Description : 
@Examples    :
"""
import logging
import os
import sys
import re
project_root = os.path.join(os.getcwd().split("ecu_simulator")[0], 'ecu_simulator')
import xat_ecu.legacy.tools.arxml_tool.autosarfactory as af

from xat_ecu.legacy.common.logger import Logger
from xat_ecu.legacy.tools.arxml_tool.can_base import *
from xat_ecu.legacy.tools.arxml_tool.lin_base import *
from xat_ecu.legacy.tools.arxml_tool.flexray_base import *
from xat_ecu.legacy.common.file_handle import *


class ArxmlParser:
    def __init__(self, arxml_file):
        self.arxml_root = None
        try:
            root, status = af.read([arxml_file])
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/arxml_tool/arxml_reader.py")
            logger.error(str(e))
        finally:
            self.arxml_root = root
        self.can_cluster, self.lin_cluster, self.fr_cluster = self.get_can_lin_fr_clusters()

    def get_can_lin_fr_clusters(self):
        """
        get channels:cluster_obj from ar_pkg:CommunicationCluster
        :return: channel:cluster_obj mapping for can/lin/FlexRay
        """
        clusters = af.get_node('/CommunicationClusters').get_elements()
        lin_clusters = {}  # {channel_name: af.cluster_obj}
        can_clusters = {}
        flexray_clusters = {}
        for c in clusters:
            if isinstance(c, af.LinCluster):
                lin_clusters.update({c.get_shortName(): c})
            elif isinstance(c, af.CanCluster):
                can_clusters.update({c.get_shortName(): c})
            elif isinstance(c, af.FlexrayCluster):
                flexray_clusters.update({c.get_shortName(): c})
        return can_clusters, lin_clusters, flexray_clusters

    def gen_lin_message_instance(self, frame_trigger:af.LinFrameTriggering) -> LinMessage:
        lin_msg_obj = LinMessage()
        # msg_name, from LinFrame()
        lin_frame = frame_trigger.get_frame()
        lin_msg_obj.set_msg_name(lin_frame.name)
        # msg_id, from LinFrameTriggering()
        lin_msg_obj.set_msg_id(frame_trigger.get_identifier())
        # msg_tx_method
        # ToDo
        # msg_cycle
        # ToDo
        # msg_length
        lin_msg_obj.set_msg_length(lin_frame.get_frameLength())
        # tx_node, ToDo, 当前fix为BGM
        lin_msg_obj.set_tx_node('BGM')
        # rx_nodes, ToDo, 当前fix为['CDC',ACU']
        lin_msg_obj.set_rx_nodes(['CDC', 'ACU'])
        # lin_signals
        lin_msg_obj.set_lin_signals(self.get_lin_signals_by_lin_frame(lin_frame))
        return lin_msg_obj

    def gen_flexray_message_instance(self, frame_trigger:af.FlexrayFrameTriggering) -> FlexrayMessage:
        # ToDo
        return FlexrayMessage()

    def gen_can_message_instance(self, frame_trigger:af.CanFrameTriggering) -> CanMessage:
        """
        can_message structure:
            msg_name
            msg_id
            msg_type
            msg_tx_method
            msg_cycle
            msg_length
            tx_node
            rx_nodes
            can_signals
        """
        can_msg_obj = CanMessage()
        # msg_name, from CanFrame()
        can_frame = frame_trigger.get_frame()
        can_msg_obj.set_msg_name(can_frame.name)
        # msg_id, from CanFrameTriggering()
        can_msg_obj.set_msg_id(frame_trigger.get_identifier())
        # msg_type (CAN/CAN_FD), check rx or tx behavior
        msg_type = frame_trigger.get_canFrameTxBehavior() if \
            frame_trigger.get_canFrameTxBehavior() is not None else frame_trigger.get_canFrameRxBehavior()
        if msg_type == af.CanFrameTxBehaviorEnum.VALUE_CAN_FD or msg_type == af.CanFrameRxBehaviorEnum.VALUE_CAN_FD:
            msg_type_set = "can_fd"
        elif msg_type == af.CanFrameTxBehaviorEnum.VALUE_CAN_20 or msg_type == af.CanFrameRxBehaviorEnum.VALUE_CAN_20:
            msg_type_set = 'can'
        else:
            logger.error("Msg name: {} got different msg_type {}".format(can_frame.name, msg_type))
        can_msg_obj.set_msg_type(msg_type_set)
        # msg_tx_method
        pdu_mappings = can_frame.get_pduToFrameMappings()
        if len(pdu_mappings) == 1:
            pdu_mapping = list(pdu_mappings)[0]
            isig_ipdu = pdu_mapping.get_pdu()
            if not isinstance(isig_ipdu, af.NmPdu) and not isinstance(isig_ipdu, af.NPdu):
                time_specs = isig_ipdu.get_iPduTimingSpecifications()
                if len(time_specs) == 0:
                    can_msg_obj.set_msg_tx_method("spontaneous")
                elif len(time_specs) > 1:
                    logger.error("Msg name: {} time_spec size > 1: {}".format(can_frame.name, time_specs))
                else:
                    time_spec = list(time_specs)[0]  # /communication/dpu/I-Signal-I-PDU
                    tx_mode_declaration = time_spec.get_transmissionModeDeclaration()
                    tx_mode_true_timing = tx_mode_declaration.get_transmissionModeTrueTiming()
                    if tx_mode_true_timing.get_cyclicTiming() != None:  # 有CYCLIC-TIMING，则是周期性的
                        can_msg_obj.set_msg_tx_method("cyclic")
                    else:  # 没有CYCLIC-TIMING，则是非周期性的
                        can_msg_obj.set_msg_tx_method("spontaneous")
            else:
                can_msg_obj.set_msg_tx_method("spontaneous")
        else:
            logger.error("Msg name: {} pdu_mappings size != 1: {}".format(can_frame.name, pdu_mappings))
        # msg_cycle
        if can_msg_obj.msg_tx_method == "cyclic":
            cycle_timing = tx_mode_true_timing.get_cyclicTiming()
            time_offset = cycle_timing.get_timeOffset().get_value()
            time_period = cycle_timing.get_timePeriod().get_value()
            # logger.info(time_period)
            can_msg_obj.set_msg_cycle(time_period)
        # msg_length
        can_msg_obj.set_msg_length(can_frame.get_frameLength())
        # tx_node, rx_node
        frame_ports = frame_trigger.get_framePorts()
        if len(frame_ports) != 1:
            logger.error("Msg name: {} frame_ports size != 1: {}".format(can_frame.name, frame_ports))
        else:
            frame_port_path_list = list(frame_ports)[0].path.split("/")
            rx_nodes = []
            tx_node = None
            if frame_port_path_list[4] == "FramePort_Out":
                tx_node = frame_port_path_list[2]
            elif frame_port_path_list[4] == "FramePort_In":
                rx_nodes.append(frame_port_path_list[2])
        can_msg_obj.set_tx_node(tx_node)
        can_msg_obj.set_rx_nodes(rx_nodes)
        # can_signals
        can_msg_obj.set_can_signals(self.get_can_signals_by_can_frame(can_frame))
        return can_msg_obj

    def gen_lin_signal_instance_by_isignal2ipdu_mapping(self, isignal2ipud_mapping):
        lin_signal = None
        isig = isignal2ipud_mapping.get_iSignal()
        if isig:  # 排除ISignalGroup
            lin_signal = LinSignal()
            # sig_name,需要将开头的"is"和结尾的"_[0-9]"去掉
            sig_name = re.sub("^is", "", isig.name)
            sig_name = re.sub("_[0-9]$", "", sig_name)
            lin_signal.set_sig_name(sig_name)
            # sig_start_bit,从ISignalToIPduMapping()中取
            lin_signal.set_sig_start_bit(isignal2ipud_mapping.get_startPosition())
            # sig_length
            lin_signal.set_sig_length(isig.get_length())
            # sig_value_init
            lin_signal.set_sig_value_init(isig.get_initValue())
            sw_data_def_props = isig.get_networkRepresentationProps()
            sw_data_def_variants = sw_data_def_props.get_swDataDefPropsVariants()
            sw_data_def_props_conditional = list(sw_data_def_variants)[0]
            base_type = sw_data_def_props_conditional.get_baseType()
            compute_method = sw_data_def_props_conditional.get_compuMethod()
            # sig_value_type
            value_type = compute_method.get_category()
            lin_signal.set_sig_value_type(value_type)
            # sig_value_table
            value_table, value_offset, value_factor = self.get_value_range_from_compu_method(compute_method)
            if value_type == "TEXTTABLE":
                lin_signal.set_sig_value_table(value_table)
            # compute_method
            # ToDo
            # sig_value_factor
            lin_signal.set_sig_value_factor(value_factor)
            # sig_value_offset
            lin_signal.set_sig_value_offset(value_offset)
            # sig_value_min, sig_value_max
            if isinstance(value_table, list):
                lin_signal.set_sig_value_min(min(value_table))
                lin_signal.set_sig_value_max(max(value_table))
            elif isinstance(value_table, dict):
                lin_signal.set_sig_value_min(min(value_table.values()))
                lin_signal.set_sig_value_max(max(value_table.values()))
        else:
            logger.error("isignal2ipud_mapping named {} has no isignal defined!".format(isignal2ipud_mapping.name))
        return lin_signal

    def gen_can_signal_instance_by_isignal2ipdu_mapping(self, isignal2ipud_mapping):
        can_signal = None
        isig = isignal2ipud_mapping.get_iSignal()
        if isig:  # 排除ISignalGroup
            can_signal = CanSignal()
            # sig_name,需要将开头的"is"和结尾的"_[0-9]"去掉
            sig_name = re.sub("^is", "", isig.name)
            sig_name = re.sub("_[0-9]$", "", sig_name)
            can_signal.set_sig_name(sig_name)
            # sig_start_bit,从ISignalToIPduMapping()中取
            can_signal.set_sig_start_bit(isignal2ipud_mapping.get_startPosition())
            # sig_length
            can_signal.set_sig_length(isig.get_length())
            # sig_value_init
            init_value_obj = isig.get_initValue()
            if init_value_obj:
                num_value_point = init_value_obj.get_value()
                can_signal.set_sig_value_init(num_value_point.get())
            sw_data_def_props = isig.get_networkRepresentationProps()
            sw_data_def_variants = sw_data_def_props.get_swDataDefPropsVariants()
            sw_data_def_props_conditional = list(sw_data_def_variants)[0]
            base_type = sw_data_def_props_conditional.get_baseType()
            compute_method = sw_data_def_props_conditional.get_compuMethod()
            # sig_value_type
            value_type = compute_method.get_category()
            can_signal.set_sig_value_type(value_type)
            # sig_value_table
            value_table, value_offset, value_factor = self.get_value_range_from_compu_method(compute_method)
            if value_type == "TEXTTABLE":
                can_signal.set_sig_value_table(value_table)
            # compute_method
            # ToDo
            # sig_value_factor
            can_signal.set_sig_value_factor(value_factor)
            # sig_value_offset
            can_signal.set_sig_value_offset(value_offset)
            # sig_value_min, sig_value_max
            if isinstance(value_table, list):
                can_signal.set_sig_value_min(min(value_table))
                can_signal.set_sig_value_max(max(value_table))
            elif isinstance(value_table, dict):
                can_signal.set_sig_value_min(min(value_table.values()))
                can_signal.set_sig_value_max(max(value_table.values()))
        else:
            logger.error("isignal2ipud_mapping named {} has no isignal defined!".format(isignal2ipud_mapping.name))
        return can_signal

    def get_can_signals_by_can_frame(self, can_frame) -> dict:
        pdu_mappings = can_frame.get_pduToFrameMappings()
        pdu = list(pdu_mappings)[0].get_pdu()
        can_signals = {}
        if not isinstance(pdu, af.NmPdu) and not isinstance(pdu, af.NPdu):  # af.NmPdu没有get_iSignalToPduMappings属性
            isig2ipdu_mappings = pdu.get_iSignalToPduMappings()
            for isig2ipdu_mapping in isig2ipdu_mappings:
                can_signal = self.gen_can_signal_instance_by_isignal2ipdu_mapping(isig2ipdu_mapping)
                if can_signal:
                    can_signals.update({can_signal.sig_name: can_signal})
        return can_signals

    def get_lin_signals_by_lin_frame(self, lin_frame) -> dict:
        pdu_mappings = lin_frame.get_pduToFrameMappings()
        pdu = None
        if len(pdu_mappings) == 1:
            pdu = list(pdu_mappings)[0].get_pdu()
            # logger.info(pdu)
        else:
            logger.error("lin_frame: {} pdu_to_frame_mappings number is not 1!".format(lin_frame.name))
        lin_signals = {}
        if isinstance(pdu, af.ISignalIPdu):
            isig2ipdu_mappings = pdu.get_iSignalToPduMappings()
            for isig2ipdu_mapping in isig2ipdu_mappings:
                lin_signal = self.gen_lin_signal_instance_by_isignal2ipdu_mapping(isig2ipdu_mapping)
                if lin_signal:
                    lin_signals.update({lin_signal.sig_name: lin_signal})
        return lin_signals


    def get_value_range_from_compu_method(self, compu_method):
        value_table = None
        v_offset = None
        v_factor = None
        compu_internal_to_pyhs = compu_method.get_compuInternalToPhys()
        if compu_internal_to_pyhs:
            # 没有COMPU-CONTENT，使用findall来寻找
            compu_scales = compu_internal_to_pyhs._node.findall('{*}COMPU-SCALES/*')
            if compu_method.get_category() == "TEXTTABLE":  # 枚举型的值表
                for cs in compu_scales:
                    v_min = cs.find("{*}LOWER-LIMIT").text
                    v_max = cs.find("{*}UPPER-LIMIT").text
                    if v_min != v_max:
                        logger.error("min {} != max {}".format(v_min, v_max))
                    # 获取值的名称
                    value_name = cs.find('{*}COMPU-CONST/*').text
                    if isinstance(value_table, dict):
                        value_table.update({value_name: int(v_min)})
                    else:
                        value_table = {value_name: int(v_min)}
            elif compu_method.get_category() == "IDENTICAL":  # IDENTICAL类型的没有compuInternalToPhys结构
                pass
            elif compu_method.get_category() == "LINEAR":
                if len(compu_scales) == 1:
                    v_min = compu_scales[0].find("{*}LOWER-LIMIT").text
                    v_max = compu_scales[0].find("{*}UPPER-LIMIT").text
                    compu_rational_coeffs = compu_scales[0].findall("{*}COMPU-RATIONAL-COEFFS/*")
                    for cef in compu_rational_coeffs:
                        if re.sub('\{.+\}', '', cef.tag) == 'COMPU-NUMERATOR':
                            v_offset, v_factor = [v.text for v in cef.findall("{*}V")]
                else:
                    logger.error("LINEAR value's scale number is abnormal {}".len(compu_scales))
                value_table = [int(v_min), int(v_max)] if v_min != None and v_max != None else []
        else:
            logger.error("compu_method name: {} has no compu_internal_to_pyhs function".format(compu_method.name))
        return value_table, v_offset, v_factor

    def get_msgs_by_cluster(self, cluster) -> dict:
        msgs = {}
        if isinstance(cluster, af.CanCluster):
            for var in cluster.get_canClusterVariants():
                if isinstance(var, af.CanClusterConditional):
                    ch = list(var.get_physicalChannels())[0]  # 考虑physicalChannel就一个
                    frame_triggers = ch.get_frameTriggerings()
                    for frame_trigger in frame_triggers:  # under /CommunicationClusters/InfoCANFD[CanClusterConditional]/InfoCANFD/
                        can_msg_inst = self.gen_can_message_instance(frame_trigger)
                        msgs.update({can_msg_inst.msg_name: can_msg_inst})
        elif isinstance(cluster, af.LinCluster):
            for var in cluster.get_linClusterVariants():
                if isinstance(var, af.LinClusterConditional):
                    ch = list(var.get_physicalChannels())[0]
                    frame_triggers = ch.get_frameTriggerings()
                    for frame_trigger in frame_triggers:
                        lin_msg_inst = self.gen_lin_message_instance(frame_trigger)
                        msgs.update({lin_msg_inst.msg_name: lin_msg_inst})
        elif isinstance(cluster, af.FlexrayCluster):
            for var in cluster.get_flexrayClusterVariants():
                if isinstance(var, af.FlexrayClusterConditional):
                    ch = list(var.get_physicalChannels())[0]
                    frame_triggers = ch.get_frameTriggerings()
                    for frame_trigger in frame_triggers:
                        logger.info(frame_trigger)
                        fr_msg_inst = self.gen_flexray_message_instance(frame_trigger)
        return msgs


def write_common_message_class(bus_name, msgs, folder_path="./can_lin_fr_class"):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "{}.py".format(bus_name.lower()))
    try:
        with open(file_path, 'w') as f:
            # for msg, msg_inst in msgs.items():
            #     if isinstance(msg_inst, CanMessage):
            #         # f.write("class {}:\n".format(bus_name))
            #         can_messages_write(msgs, f)
            can_messages_write(msgs, f)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/arxml_tool/arxml_reader.py")
        logger.error(str(e))


def can_messages_write(msgs, f_handler):
    for msg, msg_inst in msgs.items():
        msg_dict = msg_inst.return_in_dict()
        f_handler.write("class {}:\n".format(msg))
        # attr_list = sorted(msg_dict.keys())
        for attr in msg_dict.keys():
            if attr != 'can_signals':
                val = msg_dict.get(attr)
                val_set = "\"{}\"".format(val) if isinstance(val, str) else val
                f_handler.write("{s}{a} = {v}\n".format(s=' ' * 4, a=attr, v=val_set))
            elif attr == 'can_signals':
                for s_name, s_inst in msg_dict.get(attr).items():
                    sig_dict = s_inst.return_in_dict()
                    f_handler.write("\n{}class {}:\n".format(' '*4, s_name))
                    # s_attr_list = sorted(sig_dict.keys())
                    for sig_att in sig_dict.keys():
                        s_val = sig_dict.get(sig_att)
                        if sig_att == "bmuws_info":
                            s_str = "{s}{a} = {v}\n".format(s=' ' * 8, a=sig_att, v=s_val)
                            s_str = s_str.replace("'", "")
                        else:
                            s_val_set = "\"{}\"".format(s_val) if isinstance(s_val, str) and (not s_val.startswith("0b")) else s_val
                            s_str = "{s}{a} = {v}\n".format(s=' ' * 8, a=sig_att, v=s_val_set)
                        f_handler.write(s_str)

                        # if sig_att == "bmuws_info":
                        #     s_val_set = s_val_set.replace("'", "")
                        # f_handler.write("{s}{a} = {v}\n".format(s=' ' * 8, a=sig_att, v=s_val_set))

        f_handler.write("\n"*2)

def write_initpy(folder_path="./can_lin_fr_class"):
    folder_path = os.path.join(parent_dir, folder_path)
    module_name_list = FileHandle.get_file_names_from_dir_except_cpython(folder_path)
    module_name_list.remove("__init__") if "__init__" in module_name_list else None
    folder_path = os.path.join(folder_path, "__init__.py")
    with open(folder_path, "w") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("__all__ = {}\n".format(module_name_list))
        f.write("from . import *\n")


def main(arxml_path):
    arxml_db = ArxmlParser(arxml_path)
    can_clst, lin_clst, fr_clst = arxml_db.get_can_lin_fr_clusters()
    logger.info(can_clst)
    logger.info(lin_clst)
    logger.info(fr_clst)
    for c_name, c_obj in can_clst.items():
        logger.info("{} {} {}".format("="*30, c_name, "="*30))
        can_msgs = arxml_db.get_msgs_by_cluster(c_obj)
        write_common_message_class(c_name, can_msgs, folder_path="../../ ecu_simulator/sdk/data/can_lin_fr_cls/v_0_4_0")
    # for c_name, c_obj in lin_clst.items():
    #     logger.info("{} {} {}".format("="*30, c_name, "="*30))
    #     can_msgs = arxml_db.get_msgs_by_cluster(c_obj)
    #     write_common_message_class(c_name, can_msgs)
    # for c_name, c_obj in fr_clst.items():
    #     logger.info("{} {} {}".format("="*30, c_name, "="*30))
    #     can_msgs = arxml_db.get_msgs_by_cluster(c_obj)
    #     write_common_message_class(c_name, can_msgs)
    write_initpy(folder_path=" ecu_simulator/sdk/data/can_lin_fr_cls/v_0_4_0")


if __name__ == "__main__":
    logger = Logger().get_logger()
    arxml_path = os.path.join(project_root, 'ecu_simulator', 'sdk', 'data', 'arxml_file',
                              'SDB22R01_BGM_220218_AR-4.2.2_UnFlattened_All_PreRelease_NoVer.arxml')
    main(arxml_path)


    # logger.info(can_clst)
    # logger.info(lin_clst)
    # logger.info(fr_clst)
    # # can_msgs = arxml_db.get_msgs_by_cluster(can_clst.get('InfoCANFD'))
    # # easy_print(can_msgs)
    # # lin_msgs = arxml_db.get_msgs_by_cluster(lin_clst.get('CEM_LIN1'))
    # # easy_print_lin(lin_msgs)
    # fr_msgs = arxml_db.get_msgs_by_cluster(fr_clst.get('BackboneFR'))












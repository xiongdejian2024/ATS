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

current_path = os.path.dirname(os.path.realpath(__file__))

project_root111 = os.path.join(os.getcwd().split("ecu_simulator")[0], "ecu_simulator")
# print(sys.path)
import xat_ecu.legacy.tools.arxml_tool.autosarfactory as af
from openpyxl import load_workbook
from time import sleep

from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.tools.arxml_tool.can_base import *
from xat_ecu.legacy.tools.arxml_tool.lin_base import *
from xat_ecu.legacy.tools.arxml_tool.flexray_base import *
from xat_ecu.legacy.common.file_handle import *


class ArxmlParser:
    def __init__(self, arxml_file, dataid_path):
        self.arxml_root = None
        try:
            root, status = af.read([arxml_file])
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/arxml_tool/all_arxml_reader.py")
            logger.error(str(e))
        finally:
            self.arxml_root = root
        (
            self.can_cluster,
            self.lin_cluster,
            self.fr_cluster,
        ) = self.get_can_lin_fr_clusters()

        # 增加解析excle 获取 dataid
        self.dataid_dict = self.get_dataid_dict(dataid_path)

    def get_dataid_dict(self, dataid_path):
        dataid_dict = {}
        wb = load_workbook(dataid_path)
        ws = wb["E2E DataID List"]  # wb.get_sheet_by_name("E2E DataID List")

        for column in ws.iter_cols():
            if column[0].value == "Port Name":
                sig_group = column[1:]
            elif column[0].value == "DataID(Dec)":
                dataids = column[1:]

        length = len(sig_group)
        for i in range(0, length):
            sig_group_name = sig_group[i].value
            dataid = dataids[i].value
            dataid_dict[sig_group_name] = dataid
        wb.close()
        return dataid_dict

    def get_can_lin_fr_clusters(self):
        """
        get channels:cluster_obj from ar_pkg:CommunicationCluster
        :return: channel:cluster_obj mapping for can/lin/FlexRay
        """

        # clusters = af.get_node('/CommunicationClusters').get_elements()  # BGM
        clusters = af.get_node("/VehicleTopology").get_elements()
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

    def gen_lin_message_instance(
        self, frame_trigger: af.LinFrameTriggering
    ) -> LinMessage:
        lin_msg_obj = LinMessage()

        # print(frame_trigger.get_property_values())
        # {'Checksum': None, 'Timestamp': None, 'ShortName': 'FrTrMmpSmp_Lin1Fr01', 'Category': None, 'Uuid': None,
        # 'FramePorts': {FramePort(/ECUSystem/SMP/SMP/SMPCfg/SMPCfg/SMP_LIN1_SMP/FramePort_In),
        # FramePort(/ECUSystem/MMP/MMP/MMPCfg/MMPCfg/SMP_LIN1_MMP/FramePort_Out)},
        # 'Frame': LinUnconditionalFrame(/Communication/Frame/MmpSmp_Lin1Fr01), 'Identifier': 1, 'LinChecksum': ENHANCED}

        # print(frame_trigger.get_framePorts())
        # {FramePort(/ECUSystem/ECM/ECM/ECMCfg/ECMCfg/ECM_LIN3_ECM/FramePort_In), FramePort(/ECUSystem/BEXV/BEXV/BEXVCfg/BEXVCfg/ECM_LIN3_BEXV/FramePort_Out)}
        # {FramePort(/ECUSystem/ASWM/ASWM/ASWMCfg/ASWMCfg/CEM_LIN4_ASWM/FramePort_In), FramePort(/ECUSystem/BGM/BGM/BGMCfg/TLCM/CEM_LIN4_TLCM/FramePort_In), FramePort(/ECUSystem/BGM/BGM/BGMCfg/BGMCfg/CEM_LIN4_BGM/FramePort_Out)}

        # msg_name, from LinFrame()
        lin_frame = frame_trigger.get_frame()
        lin_msg_obj.set_msg_name(lin_frame.name)
        # msg_id, from LinFrameTriggering()
        lin_msg_obj.set_msg_id(frame_trigger.get_identifier())

        # msg_tx_method
        # ToDo
        # msg_cycle
        # ToDo
        if frame_trigger.get_identifier() in [60, 61]:
            lin_msg_obj.set_msg_tx_method("spontaneous")
        else:
            lin_msg_obj.set_msg_tx_method("cyclic")
            time_period = 0.039  # Temporary use
            lin_msg_obj.set_msg_cycle(time_period)

        # msg_tx_method
        # pdu_mappings = lin_frame.get_pduToFrameMappings()
        # if len(pdu_mappings) == 1:
        #     pdu_mapping = list(pdu_mappings)[0]
        #     isig_ipdu = pdu_mapping.get_pdu()
        #     if not isinstance(isig_ipdu, af.NmPdu) and not isinstance(isig_ipdu, af.NPdu) \
        #             and not isinstance(isig_ipdu, af.GeneralPurposeIPdu) \
        #             and not isinstance(isig_ipdu, af.GeneralPurposePdu):
        #         time_specs = isig_ipdu.get_iPduTimingSpecifications()
        #         if len(time_specs) == 0:
        #             lin_msg_obj.set_msg_tx_method("spontaneous")
        #         elif len(time_specs) > 1:
        #             logger.error("Msg name: {} time_spec size > 1: {}".format(lin_frame.name, time_specs))
        #         else:
        #             time_spec = list(time_specs)[0]  # /communication/dpu/I-Signal-I-PDU
        #             tx_mode_declaration = time_spec.get_transmissionModeDeclaration()
        #             tx_mode_true_timing = tx_mode_declaration.get_transmissionModeTrueTiming()
        #             if tx_mode_true_timing.get_cyclicTiming() != None:  # 有CYCLIC-TIMING，则是周期性的
        #                 lin_msg_obj.set_msg_tx_method("cyclic")
        #             else:  # 没有CYCLIC-TIMING，则是非周期性的
        #                 lin_msg_obj.set_msg_tx_method("spontaneous")
        #     else:
        #         lin_msg_obj.set_msg_tx_method("spontaneous")
        # else:
        #     logger.error("Msg name: {} pdu_mappings size != 1: {}".format(lin_frame.name, pdu_mappings))
        # # msg_cycle
        # if lin_msg_obj.msg_tx_method == "cyclic":
        #     cycle_timing = tx_mode_true_timing.get_cyclicTiming()
        #     time_offset = cycle_timing.get_timeOffset().get_value()
        #     time_period = cycle_timing.get_timePeriod().get_value()
        #     # logger.info(time_period)
        #     lin_msg_obj.set_msg_cycle(time_period)

        # msg_length
        lin_msg_obj.set_msg_length(lin_frame.get_frameLength())

        # tx_node, rx_node
        frame_ports = frame_trigger.get_framePorts()
        rx_nodes = []
        tx_node = None
        for frame_port in frame_ports:
            frame_port_list = frame_port.path.split("/")
            if frame_port_list[-1] == "FramePort_Out":
                if not tx_node:
                    tx_node = frame_port_list[-2].split("_")[-1]
                else:
                    logger.error(
                        "The number of TX cannot be greater than 1"
                    )  # to do 有出现
                    # raise ValueError("The number of TX cannot be greater than 1")
            elif frame_port_list[-1] == "FramePort_In":
                rx_nodes.append(frame_port_list[-2].split("_")[-1])
        # tx_node
        lin_msg_obj.set_tx_node(tx_node)
        # rx_nodes
        lin_msg_obj.set_rx_nodes(rx_nodes)

        (
            lin_signals,
            sig_group_dict,
            sig_group_dataid_dict,
        ) = self.get_lin_signals_by_lin_frame(lin_frame)

        lin_msg_obj.set_sig_group_dict(sig_group_dict)
        lin_msg_obj.set_sig_group_dataid_dict(sig_group_dataid_dict)
        # lin_signals
        lin_msg_obj.set_lin_signals(lin_signals)

        return lin_msg_obj

    def gen_flexray_message_instance(
        self, frame_trigger: af.FlexrayFrameTriggering
    ) -> FlexrayMessage:
        """
        flexray_message structure:
            msg_name
            msg_slotid
            msg_repetition
            msg_base_cycle
            msg_type
            msg_tx_method
            msg_channel
            msg_cycle
            msg_id
            msg_length
            tx_node
            rx_nodes
            flexray_signals
        """
        flexray_msg_obj = FlexrayMessage()
        # msg_name, from flexrayFrame()
        flexray_frame = frame_trigger.get_frame()
        flexray_msg_obj.set_msg_name(flexray_frame.name)

        # msg_id 等价, from flexrayFrameTriggering()
        # Each frame in FlexRay is identified by its slot id and communication cycle.
        absolutelyScheduledTimings = frame_trigger.get_absolutelyScheduledTimings()
        if len(absolutelyScheduledTimings) == 1:
            for absolutelyScheduledTiming in absolutelyScheduledTimings:
                communicationcycle = absolutelyScheduledTiming.get_communicationCycle()
                BaseCycle = communicationcycle.get_BaseCycle()
                flexray_msg_obj.set_msg_base_cycle(BaseCycle)
                CycleRepetition = communicationcycle.get_CycleRepetition()
                CycleRepetition = CycleRepetition.value
                CycleRepetition_int = int(CycleRepetition.split("-")[-1])
                flexray_msg_obj.set_msg_repetition(CycleRepetition_int)

                slotid = absolutelyScheduledTiming.get_slotID()
                flexray_msg_obj.set_msg_slotid(slotid)

                flexray_msg_obj.set_msg_id(
                    (slotid << 16) + (BaseCycle << 8) + CycleRepetition_int
                )
        else:
            logger.error(
                "num of absolutelyScheduledTimings is not meeting expectations, num is {}".format(
                    len(absolutelyScheduledTimings)
                )
            )

        # msg_tx_method
        flexray_msg_obj.set_msg_tx_method("cyclic")
        flexray_msg_obj.set_msg_cycle(0.005 * CycleRepetition_int)
        # pdu_mappings = flexray_frame.get_pduToFrameMappings()
        # if len(pdu_mappings) == 1:
        #     pdu_mapping = list(pdu_mappings)[0]
        #     isig_ipdu = pdu_mapping.get_pdu()
        #     if not isinstance(isig_ipdu, af.NmPdu) and not isinstance(isig_ipdu, af.NPdu) \
        #             and not isinstance(isig_ipdu, af.GeneralPurposeIPdu) \
        #             and not isinstance(isig_ipdu, af.GeneralPurposePdu):
        #         time_specs = isig_ipdu.get_iPduTimingSpecifications()
        #         if len(time_specs) == 0:
        #             flexray_msg_obj.set_msg_tx_method("spontaneous")
        #         elif len(time_specs) > 1:
        #             logger.error("Msg name: {} time_spec size > 1: {}".format(flexray_frame.name, time_specs))
        #         else:
        #             time_spec = list(time_specs)[0]  # /communication/dpu/I-Signal-I-PDU
        #             tx_mode_declaration = time_spec.get_transmissionModeDeclaration()
        #             tx_mode_true_timing = tx_mode_declaration.get_transmissionModeTrueTiming()
        #             if tx_mode_true_timing.get_cyclicTiming() != None:  # 有CYCLIC-TIMING，则是周期性的
        #                 flexray_msg_obj.set_msg_tx_method("cyclic")
        #             else:  # 没有CYCLIC-TIMING，则是非周期性的
        #                 flexray_msg_obj.set_msg_tx_method("spontaneous")
        #     else:
        #         flexray_msg_obj.set_msg_tx_method("spontaneous")
        # else:
        #     logger.error("Msg name: {} pdu_mappings size != 1: {}".format(flexray_frame.name, pdu_mappings))
        # msg_cycle
        # if flexray_msg_obj.msg_tx_method == "cyclic":
        #     cycle_timing = tx_mode_true_timing.get_cyclicTiming()
        #     time_offset = cycle_timing.get_timeOffset().get_value()
        #     time_period = cycle_timing.get_timePeriod().get_value()
        #     # logger.info(time_period)
        #     flexray_msg_obj.set_msg_cycle(time_period)
        # msg_length
        flexray_msg_obj.set_msg_length(flexray_frame.get_frameLength())
        # tx_node, rx_node
        frame_ports = frame_trigger.get_framePorts()
        rx_nodes = []
        tx_node = None
        for frame_port in frame_ports:
            frame_port_list = frame_port.path.split("/")
            if frame_port_list[-1] == "FramePort_Out":
                if not tx_node:
                    tx_node = frame_port_list[2]
                else:
                    raise ValueError("The number of TX cannot be greater than 1")

            elif frame_port_list[-1] == "FramePort_In":
                rx_nodes.append(frame_port_list[2])

        flexray_msg_obj.set_tx_node(tx_node)
        flexray_msg_obj.set_rx_nodes(rx_nodes)

        (
            flexray_signals,
            sig_group_dict,
            sig_group_dataid_dict,
        ) = self.get_flexray_signals_by_flexray_frame(flexray_frame)

        flexray_msg_obj.set_sig_group_dict(sig_group_dict)
        flexray_msg_obj.set_sig_group_dataid_dict(sig_group_dataid_dict)
        # flexray_signals
        flexray_msg_obj.set_flexray_signals(flexray_signals)

        return flexray_msg_obj

    def gen_can_message_instance(
        self, frame_trigger: af.CanFrameTriggering
    ) -> CanMessage:
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
        msg_type = (
            frame_trigger.get_canFrameTxBehavior()
            if frame_trigger.get_canFrameTxBehavior() is not None
            else frame_trigger.get_canFrameRxBehavior()
        )
        if (
            msg_type == af.CanFrameTxBehaviorEnum.VALUE_CAN_FD
            or msg_type == af.CanFrameRxBehaviorEnum.VALUE_CAN_FD
        ):
            msg_type_set = "can_fd"
        elif (
            msg_type == af.CanFrameTxBehaviorEnum.VALUE_CAN_20
            or msg_type == af.CanFrameRxBehaviorEnum.VALUE_CAN_20
        ):
            msg_type_set = "can"
        else:
            logger.error(
                "Msg name: {} got different msg_type {}".format(
                    can_frame.name, msg_type
                )
            )
        can_msg_obj.set_msg_type(msg_type_set)
        # msg_tx_method
        pdu_mappings = can_frame.get_pduToFrameMappings()
        if len(pdu_mappings) == 1:
            pdu_mapping = list(pdu_mappings)[0]
            isig_ipdu = pdu_mapping.get_pdu()
            if (
                not isinstance(isig_ipdu, af.NmPdu)
                and not isinstance(isig_ipdu, af.NPdu)
                and not isinstance(isig_ipdu, af.GeneralPurposeIPdu)
                and not isinstance(isig_ipdu, af.GeneralPurposePdu)
            ):
                time_specs = isig_ipdu.get_iPduTimingSpecifications()
                # if (
                #     not isinstance(isig_ipdu, af.NPdu)
                #     and not isinstance(isig_ipdu, af.GeneralPurposeIPdu)
                #     and not isinstance(isig_ipdu, af.GeneralPurposePdu)
                # ):
                #     if isinstance(isig_ipdu, af.NmPdu):
                #         time_specs = isig_ipdu.get_timestamp()
                #     else:
                #         time_specs = isig_ipdu.get_iPduTimingSpecifications()

                #     if time_specs is None or len(time_specs) == 0:
                if len(time_specs) == 0:
                    can_msg_obj.set_msg_tx_method("spontaneous")
                elif len(time_specs) > 1:
                    logger.error(
                        "Msg name: {} time_spec size > 1: {}".format(
                            can_frame.name, time_specs
                        )
                    )
                else:
                    time_spec = list(time_specs)[0]  # /communication/dpu/I-Signal-I-PDU
                    tx_mode_declaration = time_spec.get_transmissionModeDeclaration()
                    tx_mode_true_timing = (
                        tx_mode_declaration.get_transmissionModeTrueTiming()
                    )
                    if (
                        tx_mode_true_timing.get_cyclicTiming() != None
                    ):  # 有CYCLIC-TIMING，则是周期性的
                        can_msg_obj.set_msg_tx_method("cyclic")
                    else:  # 没有CYCLIC-TIMING，则是非周期性的
                        can_msg_obj.set_msg_tx_method("spontaneous")
            else:
                can_msg_obj.set_msg_tx_method("spontaneous")
        else:
            logger.error(
                "Msg name: {} pdu_mappings size != 1: {}".format(
                    can_frame.name, pdu_mappings
                )
            )
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
        rx_nodes = []
        tx_node = None
        for frame_port in frame_ports:
            frame_port_list = frame_port.path.split("/")
            if frame_port_list[-1] == "FramePort_Out":
                if not tx_node:
                    tx_node = frame_port_list[2]
                else:
                    raise ValueError("The number of TX cannot be greater than 1")

            elif frame_port_list[-1] == "FramePort_In":
                rx_nodes.append(frame_port_list[2])

        can_msg_obj.set_tx_node(tx_node)
        can_msg_obj.set_rx_nodes(rx_nodes)

        (
            can_signals,
            sig_group_dict,
            sig_group_dataid_dict,
        ) = self.get_can_signals_by_can_frame(can_frame)
        # can_signals
        can_msg_obj.set_sig_group_dict(sig_group_dict)
        can_msg_obj.set_can_signals(can_signals)
        can_msg_obj.set_sig_group_dataid_dict(sig_group_dataid_dict)

        return can_msg_obj

    def gen_lin_signal_instance_by_isignal2ipdu_mapping(
        self, isignal2ipud_mapping, sig_group_dict={}, sig_group_dataid_dict={}
    ):
        lin_signal = None
        isig = isignal2ipud_mapping.get_iSignal()
        isigs = isignal2ipud_mapping.get_iSignalGroup()
        if isig:  # 排除ISignalGroup
            lin_signal = LinSignal()
            # sig_name,需要将开头的"is"和结尾的"_[0-9]"去掉
            sig_name = re.sub("^is", "", isig.name)
            sig_name = re.sub("_[0-9]$", "", sig_name)
            sig_name = sig_name.split("_")[0]
            lin_signal.set_sig_name(sig_name)
            # sig_start_bit,从ISignalToIPduMapping()中取
            lin_signal.set_sig_start_bit(isignal2ipud_mapping.get_startPosition())
            lin_signal.set_update_id_bit(
                isignal2ipud_mapping.get_updateIndicationBitPosition()
            )
            # sig_length
            lin_signal.set_sig_length(isig.get_length())

            # sig_byteorder
            byteorder_enum = isignal2ipud_mapping.get_packingByteOrder()
            byteorder_enum_vaule = byteorder_enum.value
            if byteorder_enum_vaule == "MOST-SIGNIFICANT-BYTE-LAST":
                sig_byteorder = "Intel"
            elif byteorder_enum_vaule == "MOST-SIGNIFICANT-BYTE-FIRST":
                sig_byteorder = "Motorola"
            elif byteorder_enum_vaule == "OPAQUE":
                sig_byteorder = "Opaque"
            else:
                logger.error("sig_byteorder Not meeting expectations")
            lin_signal.set_sig_byteorder(sig_byteorder)

            # sig_value_init
            init_value_obj = isig.get_initValue()
            if init_value_obj:
                num_value_point = init_value_obj.get_value()
                lin_signal.set_sig_value_init(num_value_point.get())

            sw_data_def_props = isig.get_networkRepresentationProps()
            sw_data_def_variants = sw_data_def_props.get_swDataDefPropsVariants()
            sw_data_def_props_conditional = list(sw_data_def_variants)[0]
            base_type = sw_data_def_props_conditional.get_baseType()
            compute_method = sw_data_def_props_conditional.get_compuMethod()
            # sig_value_type
            value_type = compute_method.get_category()
            lin_signal.set_sig_value_type(value_type)
            # sig_value_table
            (
                value_table,
                value_table2,
                value_offset,
                value_factor,
            ) = self.get_value_range_from_compu_method(compute_method)
            if value_type == "TEXTTABLE":
                lin_signal.set_sig_value_table(value_table)
            if value_type == "SCALE_LINEAR_AND_TEXTTABLE":   
                lin_signal.set_sig_value_table(value_table2)
            # compute_method
            # ToDo
            # sig_value_factor
            lin_signal.set_sig_value_factor(value_factor)
            # sig_value_offset
            lin_signal.set_sig_value_offset(value_offset)
            # sig_value_min, sig_value_max 
            if isinstance(value_table, list):   # SCALE_LINEAR_AND_TEXTTABLE 的 最大值和最小值按照  LINEAR   的来
                lin_signal.set_sig_value_min(min(value_table))
                lin_signal.set_sig_value_max(max(value_table))
            elif isinstance(value_table, dict):
                lin_signal.set_sig_value_min(min(value_table.values()))
                lin_signal.set_sig_value_max(max(value_table.values()))
        elif isigs:  # ISignalGroup
            if isignal2ipud_mapping.get_updateIndicationBitPosition() is None:
                logger.info("这个信号组没有UB值")
                lin_signal = None
                sig_name = re.sub("^ig", "", isigs.name)
                sig_name = re.sub("_[0-9]$", "", sig_name)
                sig_name = sig_name.split("_")[0]
            else:
                lin_signal = LinSignal()
                # sig_name,需要将开头的"ig"和结尾的"_[0-9]"去掉
                sig_name = re.sub("^ig", "", isigs.name)
                sig_name = re.sub("_[0-9]$", "", sig_name)
                sig_name = sig_name.split("_")[0]  # 去掉 _数字_信号组
                sig_name_ub = sig_name + "_UB"  # 自己定义 UB 默认名字后加 _UB
                lin_signal.set_sig_name(sig_name_ub)
                # sig_start_bit,从ISignalToIPduMapping()中取
                lin_signal.set_sig_start_bit(
                    isignal2ipud_mapping.get_updateIndicationBitPosition()
                )  # 直接用 UB 的位置； 用 get_startPosition 得到的默认是信号组内第一信号的 startPosition
                lin_signal.set_update_id_bit(
                    isignal2ipud_mapping.get_updateIndicationBitPosition()
                )
                # sig_length
                lin_signal.set_sig_length(1)  # 自己定义 UB 默认用 1

                # sig_byteorder
                sig_byteorder = "Motorola"  # 自己定义 UB 默认用 Motorola
                lin_signal.set_sig_byteorder(sig_byteorder)

                # sig_value_init
                init_value = 1  # 自己定义 UB 默认为 1  信号组有效 ；   DBC 和 arxml 默认是 0
                lin_signal.set_sig_value_init(init_value)

                # sig_value_type
                value_type = "LINEAR"  # 自己定义 UB 默认为 "LINEAR"
                lin_signal.set_sig_value_type(value_type)
                # sig_value_table
                value_table = None
                value_offset = 0
                value_factor = 1
                # compute_method
                # ToDo
                # sig_value_factor
                lin_signal.set_sig_value_factor(value_factor)
                # sig_value_offset
                lin_signal.set_sig_value_offset(value_offset)
                # sig_value_min, sig_value_max
                lin_signal.set_sig_value_min(0)
                lin_signal.set_sig_value_max(1)

            iSignals = isigs._ISignalGroup__iSignals
            iSignals_list = []
            for (
                a_iSignal
            ) in (
                iSignals
            ):  # a_iSignal  such as  ISignal(/Communication/ISignal/isAsyALgtReqRngForSafeForBkpMin)
                str_iSignal = a_iSignal.path.split("/")[
                    -1
                ]  #  a_iSignal.path  such as  "/Communication/ISignal/isAsyALgtReqRngForSafeForBkpMin"
                str_iSignal = re.sub("^is", "", str_iSignal)
                str_iSignal = re.sub("_[0-9]$", "", str_iSignal)
                str_iSignal = str_iSignal.split("_")[0]
                iSignals_list.append(str_iSignal)
            iSignals_list.sort(key=str.lower)
            sig_group_dict[sig_name] = iSignals_list

            sig_group_short_name = sig_name.split("_")[0]
            data_id = self.dataid_dict.get(sig_group_short_name)
            if data_id is not None:
                sig_group_dataid_dict[sig_name] = data_id
        else:
            logger.error(
                "isignal2ipud_mapping named {} has no isignal defined!".format(
                    isignal2ipud_mapping.name
                )
            )
        return lin_signal, sig_group_dict, sig_group_dataid_dict

    def gen_flexray_signal_instance_by_isignal2ipdu_mapping(
        self, isignal2ipud_mapping, sig_group_dict={}, sig_group_dataid_dict={}, pdu_startposition=0
    ):
        # flexray_signal = None
        isig = isignal2ipud_mapping.get_iSignal()
        isigs = isignal2ipud_mapping.get_iSignalGroup()

        if isig:  # 排除ISignalGroup
            flexray_signal = FlexraySignal()
            # sig_name,需要将开头的"is"和结尾的"_[0-9]"去掉
            sig_name = re.sub("^is", "", isig.name)
            sig_name = re.sub("_[0-9]$", "", sig_name)
            sig_name = sig_name.split("_")[0]
            flexray_signal.set_sig_name(sig_name)
            # sig_start_bit,从ISignalToIPduMapping()中取
            flexray_signal.set_sig_start_bit(isignal2ipud_mapping.get_startPosition() + pdu_startposition)
            update_bit = isignal2ipud_mapping.get_updateIndicationBitPosition() + pdu_startposition if isinstance(isignal2ipud_mapping.get_updateIndicationBitPosition(), int) else isignal2ipud_mapping.get_updateIndicationBitPosition()
            flexray_signal.set_update_id_bit(update_bit)
            # sig_length
            flexray_signal.set_sig_length(isig.get_length())

            # sig_byteorder
            byteorder_enum = isignal2ipud_mapping.get_packingByteOrder()
            byteorder_enum_vaule = byteorder_enum.value
            if byteorder_enum_vaule == "MOST-SIGNIFICANT-BYTE-LAST":
                sig_byteorder = "Intel"
            elif byteorder_enum_vaule == "MOST-SIGNIFICANT-BYTE-FIRST":
                sig_byteorder = "Motorola"
            elif byteorder_enum_vaule == "OPAQUE":
                sig_byteorder = "Opaque"
            else:
                logger.error("sig_byteorder Not meeting expectations")
            flexray_signal.set_sig_byteorder(sig_byteorder)

            # sig_value_init
            init_value_obj = isig.get_initValue()
            if init_value_obj:
                num_value_point = init_value_obj.get_value()
                flexray_signal.set_sig_value_init(num_value_point.get())

            sw_data_def_props = isig.get_networkRepresentationProps()
            sw_data_def_variants = sw_data_def_props.get_swDataDefPropsVariants()
            sw_data_def_props_conditional = list(sw_data_def_variants)[0]
            base_type = sw_data_def_props_conditional.get_baseType()
            compute_method = sw_data_def_props_conditional.get_compuMethod()
            # sig_value_type
            value_type = compute_method.get_category()
            flexray_signal.set_sig_value_type(value_type)
            # sig_value_table
            (
                value_table,
                value_table2,
                value_offset,
                value_factor,
            ) = self.get_value_range_from_compu_method(compute_method)
            if value_type == "TEXTTABLE":
                flexray_signal.set_sig_value_table(value_table)
            if value_type == "SCALE_LINEAR_AND_TEXTTABLE":   
                flexray_signal.set_sig_value_table(value_table2)
            # compute_method
            # ToDo
            # sig_value_factor
            flexray_signal.set_sig_value_factor(value_factor)
            # sig_value_offset
            flexray_signal.set_sig_value_offset(value_offset)
            # sig_value_min, sig_value_max
            if isinstance(value_table, list):
                flexray_signal.set_sig_value_min(min(value_table))
                flexray_signal.set_sig_value_max(max(value_table))
            elif isinstance(value_table, dict):
                flexray_signal.set_sig_value_min(min(value_table.values()))
                flexray_signal.set_sig_value_max(max(value_table.values()))
        elif isigs:  # ISignalGroup
            if isignal2ipud_mapping.get_updateIndicationBitPosition() is None:
                logger.info("这个信号组没有UB值")
                flexray_signal = None
                sig_name = re.sub("^ig", "", isigs.name)
                sig_name = re.sub("_[0-9]$", "", sig_name)
                sig_name = sig_name.split("_")[0]
            else:
                flexray_signal = FlexraySignal()
                # sig_name,需要将开头的"ig"和结尾的"_[0-9]"去掉
                sig_name = re.sub("^ig", "", isigs.name)
                sig_name = re.sub("_[0-9]$", "", sig_name)
                sig_name = sig_name.split("_")[0]
                sig_name_ub = sig_name + "_UB"  # 自己定义 UB 默认名字后加 _UB
                flexray_signal.set_sig_name(sig_name_ub)
                # sig_start_bit,从ISignalToIPduMapping()中取
                flexray_signal.set_sig_start_bit(
                    isignal2ipud_mapping.get_updateIndicationBitPosition() + pdu_startposition
                )  # 直接用 UB 的位置； 用 get_startPosition 得到的默认是信号组内第一信号的 startPosition
                update_bit = isignal2ipud_mapping.get_updateIndicationBitPosition() + pdu_startposition if isinstance(isignal2ipud_mapping.get_updateIndicationBitPosition(), int) else isignal2ipud_mapping.get_updateIndicationBitPosition()
                flexray_signal.set_update_id_bit(update_bit)
                # sig_length
                flexray_signal.set_sig_length(1)  # 自己定义 UB 默认用 1

                # sig_byteorder
                sig_byteorder = "Motorola"  # 自己定义 UB 默认用 Motorola
                flexray_signal.set_sig_byteorder(sig_byteorder)

                # sig_value_init
                init_value = 1  # 自己定义 UB 默认为 1  信号组有效 ；   DBC 和 arxml 默认是 0
                flexray_signal.set_sig_value_init(init_value)

                # sig_value_type
                value_type = "LINEAR"  # 自己定义 UB 默认为 "LINEAR"
                flexray_signal.set_sig_value_type(value_type)
                # sig_value_table
                value_table = None
                value_offset = 0
                value_factor = 1
                # compute_method
                # ToDo
                # sig_value_factor
                flexray_signal.set_sig_value_factor(value_factor)
                # sig_value_offset
                flexray_signal.set_sig_value_offset(value_offset)
                # sig_value_min, sig_value_max
                flexray_signal.set_sig_value_min(0)
                flexray_signal.set_sig_value_max(1)

            iSignals = isigs._ISignalGroup__iSignals
            iSignals_list = []
            for (
                a_iSignal
            ) in (
                iSignals
            ):  # a_iSignal  such as  ISignal(/Communication/ISignal/isAsyALgtReqRngForSafeForBkpMin)
                str_iSignal = a_iSignal.path.split("/")[
                    -1
                ]  #  a_iSignal.path  such as  "/Communication/ISignal/isAsyALgtReqRngForSafeForBkpMin"
                str_iSignal = re.sub("^is", "", str_iSignal)
                str_iSignal = re.sub("_[0-9]$", "", str_iSignal)
                str_iSignal = str_iSignal.split("_")[0]
                iSignals_list.append(str_iSignal)
            iSignals_list.sort(key=str.lower)
            sig_group_dict[sig_name] = iSignals_list

            sig_group_short_name = sig_name.split("_")[0]
            data_id = self.dataid_dict.get(sig_group_short_name)
            if data_id is not None:
                sig_group_dataid_dict[sig_name] = data_id
        else:
            logger.error(
                "isignal2ipud_mapping named {} has no isignal defined!".format(
                    isignal2ipud_mapping.name
                )
            )
        return flexray_signal, sig_group_dict, sig_group_dataid_dict

    def gen_can_signal_instance_by_isignal2ipdu_mapping(
        self, isignal2ipud_mapping, sig_group_dict={}, sig_group_dataid_dict={}
    ):
        can_signal = None
        isig = isignal2ipud_mapping.get_iSignal()
        isigs = isignal2ipud_mapping.get_iSignalGroup()

        if isig:  # ISignal
            can_signal = CanSignal()
            # sig_name,需要将开头的"is"和结尾的"_[0-9]"去掉
            sig_name = re.sub("^is", "", isig.name)
            sig_name = re.sub("_[0-9]$", "", sig_name)
            sig_name = sig_name.split("_")[0]
            can_signal.set_sig_name(
                sig_name
            )  # NM 有的是  'isNM_PNC_USERDATA_ADCANFD_1_AcuADCANFDNmPdu' 上面 sig_name.split("_")[0] 不可以
            # sig_start_bit,从ISignalToIPduMapping()中取
            can_signal.set_sig_start_bit(isignal2ipud_mapping.get_startPosition())
            can_signal.set_update_id_bit(
                isignal2ipud_mapping.get_updateIndicationBitPosition()
            )
            # sig_length
            can_signal.set_sig_length(isig.get_length())

            # sig_byteorder
            byteorder_enum = isignal2ipud_mapping.get_packingByteOrder()
            byteorder_enum_vaule = byteorder_enum.value
            if byteorder_enum_vaule == "MOST-SIGNIFICANT-BYTE-LAST":
                sig_byteorder = "Intel"
            elif byteorder_enum_vaule == "MOST-SIGNIFICANT-BYTE-FIRST":
                sig_byteorder = "Motorola"
            elif byteorder_enum_vaule == "OPAQUE":
                sig_byteorder = "Opaque"
            else:
                logger.error("sig_byteorder Not meeting expectations")
            can_signal.set_sig_byteorder(sig_byteorder)

            # sig_value_init
            init_value_obj = isig.get_initValue()
            if init_value_obj:
                try:  # 有NM 会报错，直接填0
                    num_value_point = init_value_obj.get_value()
                    can_signal.set_sig_value_init(num_value_point.get())
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/arxml_tool/all_arxml_reader.py")
                    logger.error(f"NM 会报错,直接设置初始值为0 ，Error：{e}")
                    can_signal.set_sig_value_init(0)

            sw_data_def_props = isig.get_networkRepresentationProps()
            sw_data_def_variants = sw_data_def_props.get_swDataDefPropsVariants()
            sw_data_def_props_conditional = list(sw_data_def_variants)[0]
            base_type = sw_data_def_props_conditional.get_baseType()
            compute_method = sw_data_def_props_conditional.get_compuMethod()
            # sig_value_type
            value_type = compute_method.get_category()
            can_signal.set_sig_value_type(value_type)
            # sig_value_table
            (
                value_table,
                value_table2,
                value_offset,
                value_factor,
            ) = self.get_value_range_from_compu_method(compute_method)
            if value_type == "TEXTTABLE":
                can_signal.set_sig_value_table(value_table)
            if value_type == "SCALE_LINEAR_AND_TEXTTABLE":   
                can_signal.set_sig_value_table(value_table2)
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
        elif isigs:  # ISignalGroup
            if isignal2ipud_mapping.get_updateIndicationBitPosition() is None:
                logger.info("这个信号组没有UB值")
                can_signal = None
                sig_name = re.sub("^ig", "", isigs.name)
                sig_name = re.sub("_[0-9]$", "", sig_name)
                sig_name = sig_name.split("_")[0]
            else:
                can_signal = CanSignal()
                # sig_name,需要将开头的"ig"和结尾的"_[0-9]"去掉
                sig_name = re.sub("^ig", "", isigs.name)
                sig_name = re.sub("_[0-9]$", "", sig_name)
                sig_name = sig_name.split("_")[0]
                sig_name_ub = sig_name + "_UB"  # 自己定义 UB 默认名字后加 _UB
                can_signal.set_sig_name(sig_name_ub)
                # sig_start_bit,从ISignalToIPduMapping()中取
                can_signal.set_sig_start_bit(
                    isignal2ipud_mapping.get_updateIndicationBitPosition()
                )  # 直接用 UB 的位置； 用 get_startPosition 得到的默认是信号组内第一信号的 startPosition
                can_signal.set_update_id_bit(
                    isignal2ipud_mapping.get_updateIndicationBitPosition()
                )
                # sig_length
                can_signal.set_sig_length(1)  # 自己定义 UB 默认用 1

                # sig_byteorder
                sig_byteorder = "Motorola"  # 自己定义 UB 默认用 Motorola
                can_signal.set_sig_byteorder(sig_byteorder)

                # sig_value_init
                init_value = 1  # 自己定义 UB 默认为 1  信号组有效 ；   DBC 和 arxml 默认是 0
                can_signal.set_sig_value_init(init_value)

                # sig_value_type
                value_type = "LINEAR"  # 自己定义 UB 默认为 "LINEAR"
                can_signal.set_sig_value_type(value_type)
                # sig_value_table
                value_table = None
                value_offset = 0
                value_factor = 1
                # compute_method
                # ToDo
                # sig_value_factor
                can_signal.set_sig_value_factor(value_factor)
                # sig_value_offset
                can_signal.set_sig_value_offset(value_offset)
                # sig_value_min, sig_value_max
                can_signal.set_sig_value_min(0)
                can_signal.set_sig_value_max(1)

            iSignals = isigs._ISignalGroup__iSignals
            iSignals_list = []
            for (
                a_iSignal
            ) in (
                iSignals
            ):  # a_iSignal  such as  ISignal(/Communication/ISignal/isAsyALgtReqRngForSafeForBkpMin)
                str_iSignal = a_iSignal.path.split("/")[
                    -1
                ]  #  a_iSignal.path  such as  "/Communication/ISignal/isAsyALgtReqRngForSafeForBkpMin"
                str_iSignal = re.sub("^is", "", str_iSignal)
                str_iSignal = re.sub("_[0-9]$", "", str_iSignal)
                str_iSignal = str_iSignal.split("_")[0]
                iSignals_list.append(str_iSignal)
            iSignals_list.sort(key=str.lower)
            sig_group_dict[sig_name] = iSignals_list

            # for sig_group_name in self.dataid_dict:
            #     if sig_group_name in sig_name:
            #         sig_group_dataid_dict[sig_name] = self.dataid_dict[sig_group_name]
            #         break

            # 这个更优
            sig_group_short_name = sig_name.split("_")[0]
            data_id = self.dataid_dict.get(sig_group_short_name)
            if data_id is not None:
                sig_group_dataid_dict[sig_name] = data_id
        else:
            logger.error(
                "isignal2ipud_mapping named {} has no isignal defined!".format(
                    isignal2ipud_mapping.name
                )
            )
        return can_signal, sig_group_dict, sig_group_dataid_dict

    def get_can_signals_by_can_frame(self, can_frame) -> dict:
        pdu_mappings = can_frame.get_pduToFrameMappings()
        pdu = list(pdu_mappings)[0].get_pdu()
        can_signals = {}
        sig_group_dict = {}
        sig_group_dataid_dict = {}
        if (
            not isinstance(pdu, af.NmPdu)
            and not isinstance(pdu, af.NPdu)
            and not isinstance(pdu, af.GeneralPurposeIPdu)
            and not isinstance(pdu, af.GeneralPurposePdu)
        ):  # af.NmPdu没有get_iSignalToPduMappings属性
            isig2ipdu_mappings = pdu.get_iSignalToPduMappings()
            # if (
            #     not isinstance(pdu, af.NPdu)
            #     and not isinstance(pdu, af.GeneralPurposeIPdu)
            #     and not isinstance(pdu, af.GeneralPurposePdu)
            # ):  # af.NmPdu没有get_iSignalToPduMappings属性
            #     if isinstance(pdu, af.NmPdu):
            #         isig2ipdu_mappings = pdu._NmPdu__iSignalToIPduMappings
            #     else:
            #         isig2ipdu_mappings = pdu.get_iSignalToPduMappings()

            for isig2ipdu_mapping in isig2ipdu_mappings:
                (
                    can_signal,
                    sig_group_dict,
                    sig_group_dataid_dict,
                ) = self.gen_can_signal_instance_by_isignal2ipdu_mapping(
                    isig2ipdu_mapping, sig_group_dict, sig_group_dataid_dict
                )
                if can_signal:
                    can_signals.update({can_signal.sig_name: can_signal})
        return can_signals, sig_group_dict, sig_group_dataid_dict

    def get_lin_signals_by_lin_frame(self, lin_frame) -> dict:
        pdu_mappings = lin_frame.get_pduToFrameMappings()
        pdu = None
        if len(pdu_mappings) == 1:
            pdu = list(pdu_mappings)[0].get_pdu()
            # logger.info(pdu)
        else:
            logger.error(
                "lin_frame: {} pdu_to_frame_mappings number is not 1!".format(
                    lin_frame.name
                )
            )
        lin_signals = {}
        sig_group_dict = {}
        sig_group_dataid_dict = {}
        if isinstance(pdu, af.ISignalIPdu):
            isig2ipdu_mappings = pdu.get_iSignalToPduMappings()
            for isig2ipdu_mapping in isig2ipdu_mappings:
                (
                    lin_signal,
                    sig_group_dict,
                    sig_group_dataid_dict,
                ) = self.gen_lin_signal_instance_by_isignal2ipdu_mapping(
                    isig2ipdu_mapping, sig_group_dict, sig_group_dataid_dict
                )
                if lin_signal:
                    lin_signals.update({lin_signal.sig_name: lin_signal})
        return lin_signals, sig_group_dict, sig_group_dataid_dict

    def get_flexray_signals_by_flexray_frame(self, flexray_frame) -> dict:
        flexray_signals = {}
        sig_group_dict = {}
        sig_group_dataid_dict = {}
        pdu_mappings = flexray_frame.get_pduToFrameMappings()
        # pdu = None
        if (
            len(pdu_mappings) >= 1
        ):  # VDDM  SrsBackBoneFr01，VddmBackboneNmFr01    有两个mappings（PDU）   to do 目前暂用一个
            # pdu = list(pdu_mappings)[0].get_pdu()
            for pdu_mapping in list(pdu_mappings):
                pdu = pdu_mapping.get_pdu()
                pdu_startposition = pdu_mapping._PduToFrameMapping__startPosition  # pdu_startposition  多pdu的场景需要做对应偏移
                if isinstance(pdu, af.ISignalIPdu):
                    isig2ipdu_mappings = pdu.get_iSignalToPduMappings()
                    for isig2ipdu_mapping in isig2ipdu_mappings:
                        (
                            flexray_signal,
                            sig_group_dict,
                            sig_group_dataid_dict,
                        ) = self.gen_flexray_signal_instance_by_isignal2ipdu_mapping(
                            isig2ipdu_mapping, sig_group_dict, sig_group_dataid_dict, pdu_startposition
                        )
                        if flexray_signal:
                            flexray_signals.update(
                                {flexray_signal.sig_name: flexray_signal}
                            )
        else:
            logger.error(
                "flexray_frame: {} pdu_to_frame_mappings number is < 1!".format(
                    flexray_frame.name
                )
            )
        return flexray_signals, sig_group_dict, sig_group_dataid_dict

    def get_value_range_from_compu_method(self, compu_method):
        value_table = None
        value_table2 = None
        v_offset = None
        v_factor = None
        compu_internal_to_pyhs = compu_method.get_compuInternalToPhys()
        if compu_internal_to_pyhs:
            # 没有COMPU-CONTENT，使用findall来寻找
            compu_scales = compu_internal_to_pyhs._node.findall("{*}COMPU-SCALES/*")
            if compu_method.get_category() == "TEXTTABLE":  # 枚举型的值表
                for cs in compu_scales:
                    v_min = cs.find("{*}LOWER-LIMIT").text
                    v_max = cs.find("{*}UPPER-LIMIT").text
                    if v_min != v_max:
                        logger.error("min {} != max {}".format(v_min, v_max))
                    # 获取值的名称
                    value_name = cs.find("{*}COMPU-CONST/*").text
                    if isinstance(value_table, dict):
                        value_table.update({value_name: int(v_min)})
                    else:
                        value_table = {value_name: int(v_min)}
            elif (
                compu_method.get_category() == "IDENTICAL"
            ):  # IDENTICAL类型的没有compuInternalToPhys结构
                pass
            elif compu_method.get_category() == "LINEAR":
                if len(compu_scales) == 1:
                    v_min = compu_scales[0].find("{*}LOWER-LIMIT").text
                    v_max = compu_scales[0].find("{*}UPPER-LIMIT").text
                    compu_rational_coeffs = compu_scales[0].findall(
                        "{*}COMPU-RATIONAL-COEFFS/*"
                    )
                    for cef in compu_rational_coeffs:
                        if re.sub("\{.+\}", "", cef.tag) == "COMPU-NUMERATOR":
                            v_offset, v_factor = [v.text for v in cef.findall("{*}V")]
                else:
                    logger.error(
                        "LINEAR value's scale number is abnormal {}".format(len(compu_scales))
                    )
                value_table = (
                    [int(v_min), int(v_max)] if v_min != None and v_max != None else []
                )
            elif compu_method.get_category() == "SCALE_LINEAR_AND_TEXTTABLE":
                if len(compu_scales) >= 2:
                    for cs in compu_scales:
                        v_min = cs.find("{*}LOWER-LIMIT").text
                        v_max = cs.find("{*}UPPER-LIMIT").text
                        if v_min != v_max:   #  LINEAR
                            compu_rational_coeffs = cs.findall(
                                "{*}COMPU-RATIONAL-COEFFS/*"
                            )
                            for cef in compu_rational_coeffs:
                                if re.sub("\{.+\}", "", cef.tag) == "COMPU-NUMERATOR":
                                    v_offset, v_factor = [v.text for v in cef.findall("{*}V")]
                            value_table = (
                                [int(v_min), int(v_max)] if v_min != None and v_max != None else []
                            )
                        else:  # TEXTTABLE
                            # 获取值的名称
                            value_name = cs.find("{*}COMPU-CONST/*").text
                            if isinstance(value_table2, dict):
                                value_table2.update({value_name: int(v_min)})
                            else:
                                value_table2 = {value_name: int(v_min)}
                    
                else:
                    logger.error(
                        "LINEAR value's scale number is abnormal {}".format(len(compu_scales))
                    )
                
        else:
            # logger.error(
            #     "compu_method name: {} has no compu_internal_to_pyhs function".format(
            #         compu_method.name
            #     )
            # )
            logger.debug(
                "compu_method name: {} has no compu_internal_to_pyhs function".format(
                    compu_method.name
                )
            )  # 日志等级改成 Debug
        return value_table, value_table2, v_offset, v_factor

    def get_msgs_by_cluster(self, cluster) -> dict:
        msgs = {}
        if isinstance(cluster, af.CanCluster):
            for var in cluster.get_canClusterVariants():
                if isinstance(var, af.CanClusterConditional):
                    ch = list(var.get_physicalChannels())[0]  # 考虑physicalChannel就一个
                    frame_triggers = ch.get_frameTriggerings()
                    for (
                        frame_trigger
                    ) in (
                        frame_triggers
                    ):  # under /CommunicationClusters/InfoCANFD[CanClusterConditional]/InfoCANFD/
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
                    # lin 调度表
                    lin_scheduleTables = ch.get_scheduleTables()
                    lin_scheduleTable_dict = {}
                    for lin_scheduleTable in lin_scheduleTables:
                        lin_scheduleTable_name = lin_scheduleTable.name
                        # RUN_MODE = lin_scheduleTable._get_node_text
                        tableEntries = lin_scheduleTable.get_tableEntries()
                        applicationEntry_infos = []
                        for applicationEntry in tableEntries:
                            # lin_scheduleTable_delay = (
                            #     applicationEntry._ScheduleTableEntry__delay
                            # )
                            lin_scheduleTable_delay = applicationEntry.get_delay()
                            # lin_scheduleTable_positionInTable = (
                            #     applicationEntry._ScheduleTableEntry__positionInTable
                            # )
                            lin_scheduleTable_positionInTable = (
                                applicationEntry.get_positionInTable()
                            )
                            frameTriggerings = (
                                applicationEntry.get_frameTriggering_sun()
                            )

                            if frameTriggerings is None:
                                lin_msg_name = None
                            else:
                                lin_msg_name = frameTriggerings.split("/")[-1]
                                lin_msg_name = lin_msg_name.split("FrTr")[-1]

                            applicationEntry_info = (
                                lin_scheduleTable_positionInTable,
                                lin_msg_name,
                                lin_scheduleTable_delay,
                            )
                            applicationEntry_infos.append(applicationEntry_info)
                        lin_scheduleTable_dict[
                            lin_scheduleTable_name
                        ] = applicationEntry_infos
                        logger.info(lin_scheduleTable_dict)
                    msgs.update({"lin_scheduleTable": lin_scheduleTable_dict})

        elif isinstance(cluster, af.FlexrayCluster):
            for var in cluster.get_flexrayClusterVariants():
                if isinstance(var, af.FlexrayClusterConditional):
                    ch = list(var.get_physicalChannels())[0]
                    frame_triggers = ch.get_frameTriggerings()
                    for frame_trigger in frame_triggers:
                        logger.debug(frame_trigger)
                        fr_msg_inst = self.gen_flexray_message_instance(frame_trigger)
                        msgs.update({fr_msg_inst.msg_name: fr_msg_inst})
        return msgs


def write_common_message_class(bus_name, msgs, func, folder_path="./can_lin_fr_cls"):
    FileHandle.makedirs(folder_path)
    file_path = os.path.join(folder_path, "{}.py".format(bus_name.lower()))
    try:
        with open(file_path, "w") as f:
            func(msgs, f)
    except Exception as e:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/arxml_tool/all_arxml_reader.py")
        logger.error(str(e))


def can_messages_write(msgs, f_handler):
    for msg, msg_inst in msgs.items():
        msg_dict = msg_inst.return_in_dict()
        f_handler.write("class {}:\n".format(msg))
        # attr_list = sorted(msg_dict.keys())
        for attr in msg_dict.keys():
            if attr != "can_signals":
                val = msg_dict.get(attr)
                val_set = '"{}"'.format(val) if isinstance(val, str) else val
                f_handler.write("{s}{a} = {v}\n".format(s=" " * 4, a=attr, v=val_set))
            elif attr == "can_signals":
                for s_name, s_inst in msg_dict.get(attr).items():
                    sig_dict = s_inst.return_in_dict()
                    f_handler.write("\n{}class {}:\n".format(" " * 4, s_name))
                    # s_attr_list = sorted(sig_dict.keys())
                    for sig_att in sig_dict.keys():
                        s_val = sig_dict.get(sig_att)
                        if sig_att == "bmuws_info":
                            s_str = "{s}{a} = {v}\n".format(
                                s=" " * 8, a=sig_att, v=s_val
                            )
                            s_str = s_str.replace("'", "")
                        else:
                            s_val_set = (
                                '"{}"'.format(s_val)
                                if isinstance(s_val, str)
                                and (not s_val.startswith("0b"))
                                else s_val
                            )
                            s_str = "{s}{a} = {v}\n".format(
                                s=" " * 8, a=sig_att, v=s_val_set
                            )
                        f_handler.write(s_str)

                        # if sig_att == "bmuws_info":
                        #     s_val_set = s_val_set.replace("'", "")
                        # f_handler.write("{s}{a} = {v}\n".format(s=' ' * 8, a=sig_att, v=s_val_set))

        f_handler.write("\n" * 2)


def flexray_messages_write(msgs, f_handler):
    for msg, msg_inst in msgs.items():
        msg_dict = msg_inst.return_in_dict()
        f_handler.write("class {}:\n".format(msg))
        # attr_list = sorted(msg_dict.keys())
        for attr in msg_dict.keys():
            if attr != "flexray_signals":
                val = msg_dict.get(attr)
                val_set = '"{}"'.format(val) if isinstance(val, str) else val
                f_handler.write("{s}{a} = {v}\n".format(s=" " * 4, a=attr, v=val_set))
            elif attr == "flexray_signals":
                for s_name, s_inst in msg_dict.get(attr).items():
                    sig_dict = s_inst.return_in_dict()
                    f_handler.write("\n{}class {}:\n".format(" " * 4, s_name))
                    # s_attr_list = sorted(sig_dict.keys())
                    for sig_att in sig_dict.keys():
                        s_val = sig_dict.get(sig_att)
                        if sig_att == "bmuws_info":
                            s_str = "{s}{a} = {v}\n".format(
                                s=" " * 8, a=sig_att, v=s_val
                            )
                            s_str = s_str.replace("'", "")
                        else:
                            s_val_set = (
                                '"{}"'.format(s_val)
                                if isinstance(s_val, str)
                                and (not s_val.startswith("0b"))
                                else s_val
                            )
                            s_str = "{s}{a} = {v}\n".format(
                                s=" " * 8, a=sig_att, v=s_val_set
                            )
                        f_handler.write(s_str)

                        # if sig_att == "bmuws_info":
                        #     s_val_set = s_val_set.replace("'", "")
                        # f_handler.write("{s}{a} = {v}\n".format(s=' ' * 8, a=sig_att, v=s_val_set))

        f_handler.write("\n" * 2)


def lin_messages_write(msgs, f_handler):
    lin_scheduleTable_infos = msgs.get("lin_scheduleTable")
    if lin_scheduleTable_infos:
        f_handler.write("lin_scheduleTable = {}\n".format(lin_scheduleTable_infos))
        f_handler.write("\n" * 2)
    for msg, msg_inst in msgs.items():
        if msg != "lin_scheduleTable":
            msg_dict = msg_inst.return_in_dict()
            f_handler.write("class {}:\n".format(msg))
            # attr_list = sorted(msg_dict.keys())
            for attr in msg_dict.keys():
                if attr != "lin_signals":
                    val = msg_dict.get(attr)
                    val_set = '"{}"'.format(val) if isinstance(val, str) else val
                    f_handler.write(
                        "{s}{a} = {v}\n".format(s=" " * 4, a=attr, v=val_set)
                    )
                elif attr == "lin_signals":
                    for s_name, s_inst in msg_dict.get(attr).items():
                        sig_dict = s_inst.return_in_dict()
                        f_handler.write("\n{}class {}:\n".format(" " * 4, s_name))
                        # s_attr_list = sorted(sig_dict.keys())
                        for sig_att in sig_dict.keys():
                            s_val = sig_dict.get(sig_att)
                            if sig_att == "bmuws_info":
                                s_str = "{s}{a} = {v}\n".format(
                                    s=" " * 8, a=sig_att, v=s_val
                                )
                                s_str = s_str.replace("'", "")
                            else:
                                s_val_set = (
                                    '"{}"'.format(s_val)
                                    if isinstance(s_val, str)
                                    and (not s_val.startswith("0b"))
                                    else s_val
                                )
                                s_str = "{s}{a} = {v}\n".format(
                                    s=" " * 8, a=sig_att, v=s_val_set
                                )
                            f_handler.write(s_str)

                            # if sig_att == "bmuws_info":
                            #     s_val_set = s_val_set.replace("'", "")
                            # f_handler.write("{s}{a} = {v}\n".format(s=' ' * 8, a=sig_att, v=s_val_set))

            f_handler.write("\n" * 2)


def write_initpy(folder_path="./can_lin_fr_cls"):
    FileHandle.makedirs(folder_path)
    module_name_list = FileHandle.get_file_names_from_dir_except_cpython(folder_path)
    if "__init__" in module_name_list:
        module_name_list.remove("__init__")
    folder_path = os.path.join(folder_path, "__init__.py")
    with open(folder_path, "w") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("__all__ = {}\n".format(module_name_list))
        f.write("from . import *\n")


def main(arxml_path, dataid_path, folder_path):
    arxml_db = ArxmlParser(arxml_path, dataid_path)
    can_clst, lin_clst, fr_clst = arxml_db.get_can_lin_fr_clusters()
    logger.info(can_clst)
    logger.info(lin_clst)
    logger.info(fr_clst)
    parent_dir = project_root111
    folder_path = os.path.join(parent_dir, folder_path)
    for c_name, c_obj in can_clst.items():
        logger.info("{} {} {}".format("=" * 30, c_name, "=" * 30))
        can_msgs = arxml_db.get_msgs_by_cluster(c_obj)
        write_common_message_class(
            c_name, can_msgs, can_messages_write, folder_path=folder_path
        )
    for c_name, c_obj in lin_clst.items():
        logger.info("{} {} {}".format("=" * 30, c_name, "=" * 30))
        lin_msgs = arxml_db.get_msgs_by_cluster(c_obj)
        write_common_message_class(
            c_name, lin_msgs, lin_messages_write, folder_path=folder_path
        )
    for c_name, c_obj in fr_clst.items():
        logger.info("{} {} {}".format("=" * 30, c_name, "=" * 30))
        flexray_msgs = arxml_db.get_msgs_by_cluster(c_obj)
        write_common_message_class(
            c_name, flexray_msgs, flexray_messages_write, folder_path=folder_path
        )
    write_initpy(folder_path=folder_path)


if __name__ == "__main__":
    # Search  BGM
    # Work Path: ecu_simulator/
    # cmd :  python3 tools/arxml_tool/all_arxml_reader.py --arxml="SDB22R04_220926_Release.arxml" --dataid="SDB22R04_FIPV065_DataIDList_220914_1708.xlsx" --cls_path="sdk/data/mars1/can_lin_fr_cls/v_0_6_5"

    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--arxml", help="name of arxml", default="SDB22R05_221205_Release.arxml"
    )
    argparser.add_argument(
        "--dataid",
        help="dataid of signal group",
        default="SDB22R05_FIPV100_DataIDList_221214_1010.xlsx",
    )
    argparser.add_argument(
        "--cls_path",
        help="can lin fr cls_path",
        default="sdk/data/mars1/can_lin_fr_cls/v_1_0_0",
    )
    # Default is All
    args = argparser.parse_args()

    logger = Logger().get_logger()
    arxml_path = os.path.join(project_root111, "sdk", "data", "arxml_file", args.arxml)
    dataid_path = arxml_path.replace(args.arxml, args.dataid)
    folder_path = args.cls_path
    main(arxml_path, dataid_path, folder_path)

    # logger.info(can_clst)
    # logger.info(lin_clst)
    # logger.info(fr_clst)
    # # can_msgs = arxml_db.get_msgs_by_cluster(can_clst.get('InfoCANFD'))
    # # easy_print(can_msgs)
    # # lin_msgs = arxml_db.get_msgs_by_cluster(lin_clst.get('CEM_LIN1'))
    # # easy_print_lin(lin_msgs)
    # fr_msgs = arxml_db.get_msgs_by_cluster(fr_clst.get('BackboneFR'))

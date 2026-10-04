#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :configfile_utils.py
@Time         :2024/02/19 14:03:14
@Author       :jiabin.zhu@jiduauto.com
@Description  :
'''
import pickle
import time
import random
import uuid
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.api.interfaces.dp1.ConfigMasterV2T_pb2 import *
from xat_ecu.api.interfaces.dp1.VehicleCloud_pb2 import *


# from sdk_interface.interface.ConfigMasterV2T_pb2 import *
# from sdk_interface.interface.ConfigCenter.VehicleCloud_pb2 import *


class ConfigObj:
    """配置文件对象，用于写配置文件和读配置文件"""

    def __init__(self, file_path=None):
        if file_path:
            self.parse_config_file(file_path)
        else:
            # 注意所有参数均为bytes
            self.CRC = bytes([0x0, 0x0, 0x0, 0x0])  # 头信息的校验码，从headlen到COnfigDataLen进行计算，车端生成
            self.headlen = bytes([0x0, 0x24])  # 头信息长度，从CRC到ConfigDatalen，固定长度36，车端生成
            self.version = bytes([0x1])  # 协议版本号，当前为1
            self.confFileType = bytes([0x0])  # 文件类型，0 是json，1 二进制文件，云端下发
            self.publishID = bytes([0x0] * 8)  # 配置版本号,云端下发
            self.MD5 = bytes([0x0] * 16)  # MD5校验码，二进制值，云端下发
            self.ConfigDataLen = bytes([0x0, 0x0, 0x0, 0x1])  # 配置内容的长度
            self.content = bytes([0x0])  # ConfigDataLen 指定的长度

    def parse_config_file(self, file_path):
        """
        解析配置文件并赋值类属性
        @param file_path: 读取的配置文件路径
        """
        with open(file_path, 'rb') as file:
            data = file.read()
        self.CRC = data[0:4]
        self.headlen = data[4:6]
        self.version = data[6:7]
        self.confFileType = data[7:8]
        self.publishID = data[8:16]
        self.MD5 = data[16:32]
        self.ConfigDataLen = data[32:36]
        self.content = data[36: DataTypeHanding.to_int(self.ConfigDataLen)]
        return self.content

    def write_config_file(self, dst_path):
        """
        写配置文件至指定路径
        @param dst_path: 写入文件路径
        """
        self.handle_version()
        self.handle_confFileType()
        self.handle_publishID()
        self.handle_MD5()
        self.handle_content()
        self.ConfigDataLen = DataTypeHanding.to_bytes(f'{len(self.content):08x}')
        self.handle_CRC()

        data = self.CRC + self.headlen + self.version + self.confFileType + self.publishID + self.MD5 + self.ConfigDataLen + self.content
        with open(dst_path, 'wb') as file:
            file.write(data)

    def handle_CRC(self):
        """根据配置文件内容，输出CRC(4bytes)"""
        data = self.headlen + self.version + self.confFileType + self.publishID + self.MD5 + self.ConfigDataLen + self.content
        pass  # todo

    def handle_publishID(self):
        """处理publishID为8字节bytes"""
        if isinstance(self.publishID, int):  # 车云指令输入是int64类型
            self.publishID = bytes.fromhex(f'{self.publishID:08x}')

    def handle_confFileType(self):
        """处理confFileType为1字节bytes"""
        if isinstance(self.confFileType, int):  # 车云指令输入是int
            self.confFileType = bytes.fromhex(f'{self.confFileType:02x}')
        if isinstance(self.confFileType, str):
            self.confFileType = bytes.fromhex(self.confFileType.rjust(2, '0'))

    def handle_version(self):
        """处理version为1字节bytes"""
        if isinstance(self.version, int):
            self.version = bytes.fromhex(f'{self.version:02x}')
        if isinstance(self.version, str):
            self.version = bytes.fromhex(self.version.rjust(2, '0'))

    def handle_MD5(self):
        """处理version为16字节bytes"""
        if isinstance(self.MD5, int):
            self.MD5 = bytes.fromhex(f'{self.MD5:032x}')
        if isinstance(self.MD5, str):
            self.MD5 = bytes.fromhex(self.MD5.rjust(32, '0'))

    def handle_content(self):
        """处理配置文件内容为bytes"""
        if isinstance(self.content, str):  # 车云指令输入是str类型
            self.content = self.content.encode('utf-8')
        if isinstance(self.content, dict):
            self.content = pickle.dumps(self.content)


class V2TCmdSimulator:

    def __init__(self) -> None:
        pass


class VehicleCloudCmd:
    def __init__(self, pb_bytes, err=1, err_msg='abcd', cmd_type=1, req_timeout=0, service='v.configmaster',
                 api='TspAppConfigSet', wakeup=True) -> None:
        """
        @param pb_bytes: 车云路由具体指令
        @param err: 是否有异常，1代表无错误，非1代表有错误，当前2代表错误，101为超时未响应
        @param err_msg: 错误信息描述
        @param cmd_type: 1代表request，2表示response
        @param req_timeout: 请求超时时间，超过该时间，响应请求超时错误码。0为不限制，大于0为限制时间，单位毫秒，int32类型
        @param service: 默认云端下发配置的协议，即车端目标服务：v.configmaster。//车端处理结果上报协议，即云端目标服务：tsp.b-plat-cloud-config。//车端重启后向云端通知的协议，即云端目标服务：tsp.b-plat-cloud-config
        @param api: 默认TspAppConfigSet。//api：configStatusReport。//api：checkConfigVersion
        @param wakeup:
        """
        self.pb_bytes = pb_bytes  # todo
        self.err = err
        self.err_msg = err_msg
        self.cmd_type = cmd_type
        self.req_timeout = req_timeout
        self.service = service
        self.api = api
        self.wakeup = wakeup

    def gen_msgid(self):
        """请求的唯一ID，int64"""
        self.msg_id = random.getrandbits(32)  # todo： 响应内容与之对应？
        return self.msg_id

    def gen_trace_id(self):
        """链路跟踪id，请求与响应需保持一致，下行为云端系统生成，上行为车端生成"""
        self.trace_id = str(uuid.uuid1()).replace("-", "")
        return self.trace_id

    def return_cmd_bytes(self):
        """返回车云路由指令的bytes数据, 输出给V2T模拟器"""
        invoke = VehicleCloudInvoke()
        invoke.header.MergeFrom(self.ret_V2TInvokeHeader())
        invoke.body = self.pb_bytes

        return invoke.SerializeToString().hex()

    def ret_V2TInvokeHeader(self):
        header = V2TInvokeHeader()
        header.ver = '1.0.0'  # todo: 待对齐是否正确
        header.timeStamp = round(time.time() * 1000)  # 请求时的时间，unix时间戳，精确到毫秒
        header.type = self.cmd_type
        header.msgId = self.gen_msgid()
        header.traceId = self.gen_trace_id()
        header.reqTarget.MergeFrom(self.ret_ServiceUri())
        header.err.MergeFrom(self.ret_ErrorInfo())
        header.reqTimeout = self.req_timeout

        return header

    def ret_ServiceUri(self):
        service_uri = ServiceUri()
        service_uri.service = self.service
        service_uri.api = self.api
        service_uri.wakeup = self.wakeup

        return service_uri

    def ret_ErrorInfo(self):
        """网关侧，错误信息，双向通信都必填"""
        err_info = ErrorInfo()
        err_info.err = self.err
        err_info.msg = self.err_msg

        return err_info


class ConfigMasterV2TCmd:
    """模拟车云下发的配置文件"""

    def __init__(self, pb_ver, ModelName, ModelYear, Domain, AppName, ConfName, Action, ConfType, PushType,
                 SyncStrategy, Value, wakeup=False, PublishID=random.getrandbits(60)) -> None:
        """
        @param  pb_ver: pb协议的版本，比如V1、V2、V3等
        @param  ModelName: 车型，如：MarsOne，Venus
        @param  ModelYear: 款型，如：2023，2024
        @param Domain: 域控，如：tcam，bgm，cdc，acu
        @param AppName: 应用名称
        @param ConfName: 配置文件的名称
        @param Action: 配置动作，0代表默认update，1代表update，2代表删除
        @param ConfType: 配置的类型，0代表json类型，1代表file类型
        @param PushType: 配置推送方式，1代表推送内容，2代表推送链接地址
        @param SyncStrategy: 同步策略，1代表一轮休眠后同步，2表示P挡同步，3代表实时同步
        @param Value: json数据或者url地址
        @param wakeup: 是否唤醒应用所在的域控
        """
        self.pb_ver = pb_ver
        self.ModelName = ModelName
        self.ModelYear = ModelYear
        self.Domain = Domain
        self.AppName = AppName
        self.ConfName = ConfName
        self.Action = Action
        self.ConfType = ConfType
        self.PushType = PushType
        self.SyncStrategy = SyncStrategy
        self.Value = Value
        self.wakeup = wakeup
        self.PublishID = PublishID

    def ret_Conf(self):
        _Conf = Conf()
        _Conf.Domain = self.Domain
        _Conf.AppName = self.AppName
        _Conf.ConfName = self.ConfName
        # _Conf.PublishID = self.gen_PublishID()
        _Conf.PublishID = self.PublishID
        _Conf.Action = self.Action
        _Conf.ConfType = self.ConfType
        _Conf.PushType = self.PushType
        _Conf.Value = self.Value
        _Conf.SyncStrategy = self.SyncStrategy
        _Conf.Wakeup = self.wakeup
        _Conf.DomainVer = "1.0.0"
        _Conf.Md5 = self.gen_md5()

        return _Conf

    # def gen_PublishID(self):
    #     """发布的唯一标识，int64"""
    #     self.PublishID = random.getrandbits(60) # todo： 响应内容与之对应？

    #     return self.PublishID

    def gen_md5(self):
        """MD5校验码，为云端系统生成"""
        # self.md5_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, name="")).replace("-", "")
        import hashlib
        md5_obj = hashlib.md5()
        md5_obj.update(self.Value)
        self.md5_id = md5_obj.hexdigest().upper()

        return self.md5_id

    def gen_Timestamp(self):
        self.Timestamp = round(time.time() * 1000)

        return self.Timestamp

    def return_v2t_cmd_bytes(self):
        """返回云端配置下发指令的bytes数据, 输出给车端ConfigMaster"""
        invoke = ConfSyncData()
        invoke.Confs.MergeFrom([self.ret_Conf()])
        invoke.PbVer = self.pb_ver
        invoke.Timestamp = self.gen_Timestamp()
        invoke.ModelName = self.ModelName
        invoke.ModelYear = self.ModelYear

        return invoke.SerializeToString().hex()


class ConfSyncData_Resp(ConfigMasterV2TCmd):
    """车端的响应"""

    def __init__(self, status, status_msg) -> None:
        """
        @param status: 状态码，RS_SUCCESS代表成功，RS_FAIL代表失败
        @param status_msg: 描述
        """
        self.status = status
        self.status_msg = status_msg

    def ret_ConfSyncDataRespDetail(self):
        conf_res_det = ConfSyncDataRespDetail()
        conf_res_det.PublishID = self.PublishID
        conf_res_det.Status = self.status
        conf_res_det.StatusMessage = self.status_msg

        return conf_res_det

    def return_ConfSyncDataResp_cmd_bytes(self):
        """返回车端响应指令的bytes数据"""
        conf_resp = ConfSyncDataResp()
        conf_resp.Details.MergeFrom([self.ret_ConfSyncDataRespDetail()])

        return conf_resp.SerializeToString().hex()


class ConfigStatusRpt(ConfigMasterV2TCmd):
    """车端结果上报"""

    def __init__(self, StageType, StatusType, StatusMessage, ) -> None:
        """
        @param StageType: 上报的阶段类型，1代表配置master收到了，2代表配置中心收到了，3代表APP Check成功，4代表在应用中生效了
        @param StatusType： 上报的状态，1代表成功，非1代表失败
        @param StatusMessage：上报的状态message
        @param
        """
        self.StageType = StageType
        self.StatusType = StatusType
        self.StatusMessage = StatusMessage

    def gen_AppIndex(self):
        self.AppIndex = random.getrandbits(32)

        return self.AppIndex

    def ret_ConfReportData(self):
        confrep = ConfReportData()
        confrep.PublishID = self.PublishID
        confrep.Domain = self.Domain
        confrep.AppName = self.AppName
        confrep.ConfName = self.ConfName
        confrep.StatusData.MergeFrom([self.ret_ConfigStatusData()])

        return confrep

    def ret_ConfigStatusData(self):
        configsts = ConfigStatusData()
        configsts.StageType = self.StageType
        configsts.StatusType = self.StatusType
        configsts.StatusMessage = self.StatusMessage
        configsts.AppIndex = self.gen_AppIndex()
        configsts.Timestamp = self.gen_Timestamp()

        return configsts

    def return_ConfigStatusReport_cmd_bytes(self):
        """返回车端结果上报指令的bytes数据, 输出给云端V2T"""
        confstsrpt = ConfigStatusReport()
        confstsrpt.PbVer = self.pb_ver
        confstsrpt.Timestamp = self.gen_Timestamp()
        confstsrpt.Data.MergeFrom([self.ret_ConfReportData()])

        return confstsrpt.SerializeToString().hex()


class ConfigStatusRptResp(ConfigStatusRpt):
    """云端的响应"""

    def __init__(self, status, status_msg) -> None:
        """
        @param status: 状态码，RS_SUCCESS代表成功，RS_FAIL代表失败
        @param status_msg: 描述
        """
        self.status = status
        self.status_msg = status_msg

    def ret_ConfigStatusReportRespDetail(self):
        conf_sts_resp = ConfigStatusReportRespDetail()
        conf_sts_resp.PublishID = self.PublishID
        conf_sts_resp.AppIndex = self.gen_AppIndex()
        conf_sts_resp.Status = self.status
        conf_sts_resp.StatusMessage = self.status_msg

        return conf_sts_resp

    def return_ConfigStatusReportResp_cmd_bytes(self):
        """返回云端响应指令的bytes数据"""
        con_sts_rpt_resp = ConfigStatusReportResp()
        con_sts_rpt_resp.Details.MergeFrom(self.ret_ConfigStatusReportRespDetail())

        return con_sts_rpt_resp.SerializeToString().hex()


class NotyData(ConfigStatusRpt):
    """车端重启后向云端通知，云端根据维护的历史数据，主动下发确实或滞后的配置"""

    def __init__(self, IsEmpty: bool) -> None:
        """
        @param IsEmpty: 标识数组是否为空，方便车端处理
        """
        self.IsEmpty = IsEmpty

    def ret_AppDetail(self):
        app_Detail = AppDetail()
        app_Detail.PbVer = self.pb_ver
        app_Detail.PublishID = self.PublishID
        app_Detail.Domain = self.Domain
        app_Detail.AppName = self.AppName
        app_Detail.ConfName = self.ConfName
        app_Detail.StatusData.MergeFrom([self.ret_ConfigStatusData()])

        return app_Detail

    def return_NotifyData_cmd_bytes(self):
        notity_data = NotifyData()
        notity_data.IsEmpty = self.IsEmpty
        notity_data.Timestamp = self.gen_Timestamp()
        notity_data.Detail.MergeFrom([self.ret_AppDetail()])

        return notity_data.SerializeToString().hex()


class ReqCkConfigData(ConfigMasterV2TCmd):
    """车端支持云端查询车端配置文件版本号"""

    def __init__(self) -> None:
        pass

    def return_ReqCheckConfigData_cmd_bytes(self):
        Req_Check_ConfigData = ReqCheckConfigData()
        Req_Check_ConfigData.Timestamp = self.gen_Timestamp()

        return Req_Check_ConfigData.SerializeToString().hex()


class ServiceEventReqData(ConfigMasterV2TCmd):
    """数据服务在线实时检测"""

    def __init__(self, serviceName) -> None:
        self.serviceName = serviceName

    def ret_SoaServiceEvent(self):
        soa_ServiceEvent = SoaServiceEvent()
        soa_ServiceEvent.serviceName = self.serviceName
        soa_ServiceEvent.timestamp = self.gen_Timestamp()

    def return_event_res(self):
        ServiceEvent_Req = ServiceEventReq()
        ServiceEvent_Req.timestamp = self.gen_Timestamp()
        ServiceEvent_Req.events.MergeFrom()
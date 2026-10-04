# -*- coding: utf-8 -*-
"""
@File        : digital_key_can_protocol.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2022/10/18 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""
import hashlib
import hmac
import os
import sys
import uuid

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.diagnosis.aes_128_cbc import AES, Aes128, AesCmac128
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *

BNCM_KEY = bytes([0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16,
                  0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F])
BNCM_KEY = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
BNCM_IV = bytes([0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
                 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F])
KEYID = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
         0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
KEYID1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]


def bytes2str(ori_bytes: bytes) -> str:
    """字节串转十六进制字符串（大写）"""
    res = ''
    for byte in ori_bytes:
        res += f"{byte:02X}"
    return res


def cal_sha256(data: str = (bytes2str(BNCM_KEY) + bytes2str(BNCM_IV))):
    """计算哈希值"""  # TODO: 待确认用哪个函数计算哈希值
    return hashlib.sha256(data.encode('utf-8')).hexdigest().upper()


def cal_sha256_hmac(data: str = bytes2str(BNCM_IV), key=BNCM_KEY):
    return hmac.new(key, BNCM_IV, digestmod=hashlib.sha256).hexdigest().upper()


class BncmBgmPduEncrypt(Aes128):
    """BNCM和BGM间can通信加密"""

    def __init__(self, key=BNCM_KEY, iv=BNCM_IV, mode=AES.MODE_CBC):
        super().__init__(key, iv, mode)
        self.aes_cmac = AesCmac128(key)
        self.bgm_time = "00000000"

    def update_bgm_time(self, time_stamp: int) -> None:
        """更新BGM时间，用于数字钥匙指令加密"""
        self.bgm_time = f'{time_stamp:08X}'

    def decrypt_cmd(self, cipher: Union[bytearray, bytes]) -> bytes:
        """
        解析BGM的响应报文，寻钥匙或车控结果指令
        :param cipher: 密文(bytes)
        :return: 有效命令数据(bytes)，已去除4字节时间戳及pkcs7填充字节
        """
        cmac = DataTypeHanding.intlist_to_hexstr(cipher)[-28:]
        plain_data = self.decrypt(cipher[0:-14])
        if plain_data[-1] == 0:
            ori_data = plain_data
        else:
            fill = plain_data[-1]
            ori_data = plain_data[0:-fill]
        exp_cmac = self.aes_cmac.encrypt(DataTypeHanding.intlist_to_hexstr(ori_data))[0:28]
        if exp_cmac != cmac.upper():
            logger.error(f"当前报文CMAC计算异常, 应该是{exp_cmac}")
        return ori_data[4:]

    def assamble_encrypt_message(self, data: str) -> list:
        """
        对BNCM发送的原始数据包进行加密并拆包
        :param : BNCM发送的原始cmd
        :return: 加密并拆包为pdu列表
        """
        logger.info("发送指令明文：%s", data)
        return self.__assemble_pdus(self.__encrypt_message(data))

    def __encrypt_message(self, data: str) -> str:
        """
        BNCM和BGM通信报文的加密
        :param data: 待加密明文
        :return: 加密密文，截断14字节cmac + 密文
        """
        cmac = self.aes_cmac.encrypt(data)
        cmac14 = cmac[0:28]
        cipher_data = self.encrypt_pad_with_pkcs7(data).hex()
        res = cipher_data + cmac14
        logger.info(f"加密后密文是：{res}")
        return res

    def __assemble_pdus(self, data: str) -> list:
        """
        按BNCM和BGM的can协议要求，超过62字节的数据进行拆包
        :param : 原始数据，十六进制字符串形式
        :return: 列表形式的pdu包
        """
        pdus = []
        pdu_length = len(data) // 2
        header = 1
        ack = 0
        hello_msg = f"{header:02X}00010000{pdu_length:04X}{'00' * 56}{ack:02X}"
        pdus.append(DataTypeHanding.hexstr_to_inlist(hello_msg))

        rest_length = pdu_length
        while True:
            header += 1
            pdu = f"{header:02X}{data.ljust(124, '0')[0:124]}{ack:02X}"
            pdus.append(DataTypeHanding.hexstr_to_inlist(pdu))
            if rest_length > 62:
                rest_length = rest_length - 62
                data = data[124:]
            else:
                break
        return pdus

    def peps_approach(self, key_type=2, action=0x2, key_id: Union[int] = None) -> list:
        """
        加密靠近迎宾，靠近解锁，离车上锁报文, function_id固定0x20.对该功能组包
        :param key_type: 指令触发源的钥匙类型
        :param action: 功能的操作类型(0x01 迎宾灯, 0x02 解锁, 0x03 上锁)
        :param key_id: action为0x1和0x2时可选，16字节keyid
        :return: 按协议要求转换的多包列表[[64字节intlist], [64字节intlist]...]
        """
        # FunctionId + keyType + Action + [KeyId]
        ble_payload = f"20{key_type:02X}{action:02X}"
        if action in [1, 2]:
            ble_payload += DataTypeHanding.intlist_to_hexstr(key_id)
        return self.assamble_encrypt_message(self.bgm_time + ble_payload)

    def nfc_lock_cmd(self, key_id: Union[int] = None) -> list:
        """
        发送NFC刷卡事件通知
        :return:
        """
        if key_id is None:
            key_id = key_id1
        return self.assamble_encrypt_message(self.bgm_time + "3001" + DataTypeHanding.intlist_to_hexstr(key_id))

    def apa_cmd(self, action: int, account_info: str):
        """构造APA指令"""
        return self.assamble_encrypt_message(self.bgm_time + "0B" + f"{action:02X}" + account_info)

    def avp_cmd(self, action: int, account_info: str):
        """构造AVP指令"""
        return self.assamble_encrypt_message(self.bgm_time + "0A" + f"{action:02X}" + account_info)

    def charge_pile_open_charge_lid(self, action: int = 1) -> list:
        """
        发送NFC刷卡事件通知
        :return:
        """
        return self.assamble_encrypt_message(self.bgm_time + "81{:02X}".format(action))

    def _soc_rke_cmd(self, ble_payload: str, slot_index: int = 1) -> list:
        """
        对蓝牙车控指令组包 0x21 + SlotIndex+BLEPayload-Command长度 + 手机钥匙对应的序号+实际的蓝牙指令
        :param ble_payload: 蓝牙车控指令，ptoto3转换成的字符串
        :param slot_index: 手机钥匙对应的序号，1byte
        :return: pdus
        """
        ori_data = f'FF21{1 + len(ble_payload) // 2:04X}{slot_index:02X}{ble_payload}'
        return self.assamble_encrypt_message(self.bgm_time + ori_data)

    def rke_chargelidgate(self, op, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61) -> list:
        """充电口盖控制"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 12
        cd = CmdDetail()
        wc = ChargeLidGate()
        wc.op = op
        cd.charge_lid_gate.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_maxsoc(self, soc, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61) -> list:
        """RKE充电MaxSOC控制"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 5  # 充电SOC设置
        cd = CmdDetail()
        wc = ChargeSocSettings()
        wc.max = soc
        cd.charge_soc_settings.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_tailgate_control(self, op, position=100, slot_index: int = 1, exec_id: str = '', vid='',
                             vehicle_model=61) -> list:
        """RKE尾门控制(-1: 关，1:开，2：翘起(废弃)，3：设置开度值)"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 4  # 尾门控制
        cd = CmdDetail()
        wc = TailGateControl()
        wc.op = op
        wc.position = position
        cd.tailgate_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_door_full_closing_control(self, op, slot_index: int = 1, exec_id: str = '', vid='',
                                      vehicle_model=61) -> list:
        """五门全关控制"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 10
        cd = CmdDetail()
        wc = DoorFullClosingControl()
        wc.op = op
        cd.door_full_closing_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_panic_vehicle(self, op, slot_index: int = 1, exec_id: str = '', vid='', vehicle_model=61) -> list:
        """寻车控制 -1，关闭，1，鸣笛闪灯，2，仅闪灯"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 3
        cd = CmdDetail()
        wc = PanicVehicle()
        wc.op = op
        cd.panic_vehicle.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_window_control_cmd(self, p1, p2, p3, p4, slot_index: int = 1, exec_id: str = '',
                               vid='', vehicle_model=61) -> list:
        """RKE车窗控制"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 2  # 车窗

        cd = CmdDetail()
        wc = WindowControl()
        wc.frontLeft = p1
        wc.frontRight = p2
        wc.secondRowLeft = p3
        wc.secondRowRight = p4
        cd.window_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)
    
    def rke_driver_door_control_cmd(self, op, position, key_id: str = f'{1:032}', user_id: str = '',
                                        slot_index: int = 1, exec_id: str = '', vid='',vehicle_model=61) -> list:
        """
        RKE主驾门控制
        :param op: 1: 设置开度, 2: 关, 3: 全开（预留）
        """
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 33
        cd = CmdDetail()
        wc = DoorControl()
        wc.op = op
        wc.keyId = key_id
        wc.userId = user_id
        wc.position = position
        cd.driver_door_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)
    
    def rke_passenger_door_control_cmd(self, op, position, key_id: str = f'{1:032}', user_id: str = '',
                                        slot_index: int = 1, exec_id: str = '', vid='',vehicle_model=61) -> list:
        """
        RKE副驾门控制
        :param op: 1: 设置开度, 2: 关, 3: 全开（预留）
        """
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 34
        cd = CmdDetail()
        wc = DoorControl()
        wc.op = op
        wc.keyId = key_id
        wc.userId = user_id
        wc.position = position
        cd.passenger_door_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)
    
    def rke_rear_left_door_control_cmd(self, op, position, key_id: str = f'{1:032}', user_id: str = '',
                                        slot_index: int = 1, exec_id: str = '', vid='',vehicle_model=61) -> list:
        """
        RKE左后门控制
        :param op: 1: 设置开度, 2: 关, 3: 全开（预留）
        """
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 35
        cd = CmdDetail()
        wc = DoorControl()
        wc.op = op
        wc.keyId = key_id
        wc.userId = user_id
        wc.position = position
        cd.rear_left_door_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)
    
    def rke_rear_right_door_control_cmd(self, op, position, key_id: str = f'{1:032}', user_id: str = '',
                                        slot_index: int = 1, exec_id: str = '', vid='',vehicle_model=61) -> list:
        """
        RKE右后门控制
        :param op: 1: 设置开度, 2: 关, 3: 全开（预留）
        """
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 36
        cd = CmdDetail()
        wc = DoorControl()
        wc.op = op
        wc.keyId = key_id
        wc.userId = user_id
        wc.position = position
        cd.rear_right_door_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)
    
    def rke_four_door_control_cmd(self, op, driverPosition, passengerPosition, rearLeftPosition,
                                  rearRightPosition, key_id: str = f'{1:032}', user_id: str = '', 
                                  slot_index: int = 1, exec_id: str = '', vid='',vehicle_model=61) -> list:
        """
        RKE四门一键控制
        :param op: 1: 设置开度, 2: 关, 3: 全开（预留）
        """
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 37
        cd = CmdDetail()
        wc = FourDoorControl()
        wc.op = op
        wc.keyId = key_id
        wc.userId = user_id
        wc.driverPosition = driverPosition
        wc.passengerPosition = passengerPosition
        wc.rearLeftPosition = rearLeftPosition
        wc.rearRightPosition = rearRightPosition
        cd.four_door_control.MergeFrom(wc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_lock_cmd(self, op=2, key_id: str = f'{1:032}', slot_index: int = 1, user_id: str = '',
                     exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61) -> list:
        """RKE闭锁"""
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = exec_id if exec_id else str(uuid.uuid1()).replace("-", "")
        real_cmd.vid = vid
        real_cmd.vehicleModel = vehicle_model
        real_cmd.cmdCode = 1  # 解闭锁
        real_cmd.timestamp = 1000000012345678

        cd = CmdDetail()
        lc = LockControl()
        lc.op = op
        lc.keyId = key_id
        lc.userId = user_id
        cd.lock_control.MergeFrom(lc)
        real_cmd.cmdDetail.MergeFrom(cd)
        return self._soc_rke_cmd(real_cmd.SerializeToString().hex(), slot_index)

    def rke_unlock_cmd(self, key_id: str, slot_index: int = 1, user_id: str = '', exec_id: str = '',
                       vid: str = f'{1:032}', vehicle_model: int = 61) -> list:
        """RKE解锁"""
        return self.rke_lock_cmd(1, key_id, slot_index, user_id, exec_id, vid, vehicle_model)

    def rke_close_door_and_lock_cmd(self, key_id: str, slot_index: int = 1, user_id: str = '',
                                    exec_id: str = '', vid: str = f'{1:032}', vehicle_model: int = 61) -> list:
        """RKE关门+闭锁"""
        return self.rke_lock_cmd(3, key_id, slot_index, user_id, exec_id, vid, vehicle_model)

    def white_list_control_resp(self, sub_id: int, status: int, last_sync_time: int) -> list:
        """白名单控制响应报文，当前只考虑了0x11和0x12"""
        return self.assamble_encrypt_message(self.bgm_time + f"FF{sub_id:02X}0009{status:02X}{last_sync_time:016X}")

    def nfc_learning_resp(self, status: int, card_id=None) -> list:
        """NFC学卡请求"""
        if card_id is not None:
            return self.assamble_encrypt_message(
                self.bgm_time + f"FF140011{status:02X}" + DataTypeHanding.intlist_to_hexstr(card_id))
        else:
            return self.assamble_encrypt_message(self.bgm_time + f"FF140001{status:02X}")


if __name__ == '__main__':
    aes = AesCmac128(BNCM_KEY)
    real_resp = RealtimeCmdResp()
    real_cmd = RealtimeCmdReq()
    # print(aes.encrypt('058f0341ff220034010a203030303030303030303030303030313637313039353336322e303736373931351a0e507265436f6e646974696f6e4f4b2802'))
    dk_can_encrypt = BncmBgmPduEncrypt()
    # da = bytes([0x2b,0x1c,0x32,0x5f,0x9a,0x53,0xad,0x73,0x7d,0x23,0x0d,0x4b,0xc2,0xa6,0xff,0xdd,0x1d,0x8a,0x33,0x8c,0x2b,0x0b,0x8d,0xa9,0xc6,0x13,0x40,0xa5,0xf6,0x87,0xd0,0x7b])
    # print(DataTypeHanding.intlist_to_hexstr(
    #     dk_can_encrypt.decrypt(da)))？

    da = '86 72 B7 52 A3 B4 D3 78 EE BB C0 78 9B 92 AF A7 62 7E 2F 69 91 48 A4 99 DD 09 FA 28 B5 25'
    print(DataTypeHanding.intlist_to_hexstr(
        dk_can_encrypt.decrypt(da.replace(" ", '')[:-28]))[8:])
    da = '1B 76 FB 05 C4 33 24 F8 88 ED BB 6E 39 F2 F9 02 49 23 88 A7 80 4C E7 79 B8 4C 0F D7 3F F0'
    print(DataTypeHanding.intlist_to_hexstr(
        dk_can_encrypt.decrypt(da.replace(" ", '')[:-28]))[8:])

    # da = '58 72 D0 05 B0 16 13 46 04 9E 28 97 0D 4D 0F 18 8E FC 8A AC 6D 4F 13 C5 2C A8 91 94 B1 53 31 F3 D4 8A 15 9E 72 E3 FD A2 58 48 DE 0A E6 B8'
    # print(DataTypeHanding.intlist_to_hexstr(
    #     dk_can_encrypt.decrypt_cmd(bytes.fromhex(da))))
    # print(DataTypeHanding.intlist_to_hexstr(
    #     dk_can_encrypt.decrypt(da.replace(" ", '')[:-28])))
    real_resp.ParseFromString(bytes.fromhex(
        '0a20303030303030303030303030303030303030303030303030303030303030303110ffffffffffffffffff011a04425553592803'.replace(
            ' ', '')))
    print(real_resp)
    # print(real_cmd)

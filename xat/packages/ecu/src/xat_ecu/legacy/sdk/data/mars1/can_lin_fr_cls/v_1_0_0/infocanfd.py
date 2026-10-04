class BgmInfoCanFdFr22:
    msg_name = "BgmInfoCanFdFr22"
    msg_id = 513
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['S2SReceiver', 'CDC']
    sig_group_dict = {'ExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22': ['ExhibitionModeStsChks_0_BgmInfoCanFdSignalIPdu22', 'ExhibitionModeStsCntr_0_BgmInfoCanFdSignalIPdu22', 'ExhibitionModeStsExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22'], 'StatusOfOuterDoorSwLight': ['StatusOfOuterDoorSwLightDrvrSwLight', 'StatusOfOuterDoorSwLightLeReSwLight', 'StatusOfOuterDoorSwLightPassSwLight', 'StatusOfOuterDoorSwLightRiReSwLight']}
    sig_group_dataid_dict = {'ExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22': 9001}

    class StatusOfOuterDoorSwLightDrvrSwLight:
        sig_name = "StatusOfOuterDoorSwLightDrvrSwLight"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ExhibitionModeStsExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22:
        sig_name = "ExhibitionModeStsExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class StatusOfOuterDoorSwLightRiReSwLight:
        sig_name = "StatusOfOuterDoorSwLightRiReSwLight"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22_UB:
        sig_name = "ExhibitionModeSts_0_BgmInfoCanFdSignalIPdu22_UB"
        sig_start_bit = 12
        update_id_bit = 12
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ExhibitionModeStsChks_0_BgmInfoCanFdSignalIPdu22:
        sig_name = "ExhibitionModeStsChks_0_BgmInfoCanFdSignalIPdu22"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ExhibitionModeStsCntr_0_BgmInfoCanFdSignalIPdu22:
        sig_name = "ExhibitionModeStsCntr_0_BgmInfoCanFdSignalIPdu22"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class StatusOfOuterDoorSwLight_UB:
        sig_name = "StatusOfOuterDoorSwLight_UB"
        sig_start_bit = 16
        update_id_bit = 16
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class StatusOfOuterDoorSwLightPassSwLight:
        sig_name = "StatusOfOuterDoorSwLightPassSwLight"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class StatusOfOuterDoorSwLightLeReSwLight:
        sig_name = "StatusOfOuterDoorSwLightLeReSwLight"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevSts4_Off': 0, 'DevSts4_On': 1, 'DevSts4_Err': 2, 'DevSts4_Resd': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SentrWarnReq_1_BgmInfoCanFdSignalIPdu22:
        sig_name = "SentrWarnReq_1_BgmInfoCanFdSignalIPdu22"
        sig_start_bit = 63
        update_id_bit = 62
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WinGlbCmd1:
        sig_name = "WinGlbCmd1"
        sig_start_bit = 23
        update_id_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClsGlbCmd_Idle': 0, 'OpenClsGlbCmd_GlobalOpenWindow': 1, 'OpenClsGlbCmd_GlobalCloseWindowAndSunroof': 2, 'OpenClsGlbCmd_GlobalCloseWindow': 3, 'OpenClsGlbCmd_GlobalStop': 4, 'OpenClsGlbCmd_Resd1': 5, 'OpenClsGlbCmd_Resd2': 6, 'OpenClsGlbCmd_Resd3': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class BgmInfoCanFdFr21:
    msg_name = "BgmInfoCanFdFr21"
    msg_id = 1152
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['S2SReceiver', 'CCM', 'CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class LockSysStsPrmt:
        sig_name = "LockSysStsPrmt"
        sig_start_bit = 15
        update_id_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSysStsPrmt_Idle': 0, 'LockSysStsPrmt_NFC_PSD': 1, 'LockSysStsPrmt_ANTI_LOCK_KEY_FORGET': 2, 'LockSysStsPrmt_NO_KEY_PRESENT': 3, 'LockSysStsPrmt_CLOSE_DOOR_AUDIO': 4, 'LockSysStsPrmt_ANTI_RELOCK': 5, 'LockSysStsPrmt_AUTO_RELOCK': 6}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class TelmRemoteAuthStartSts:
        sig_name = "TelmRemoteAuthStartSts"
        sig_start_bit = 23
        update_id_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReminderWhileLock_1_BgmInfoCanFdSignalIPdu21:
        sig_name = "ReminderWhileLock_1_BgmInfoCanFdSignalIPdu21"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReminderWhileLock_IDLE': 0, 'ReminderWhileLock_NOT_SET_APPROACH_LOCK_HMI': 1, 'ReminderWhileLock_DOOR_CLOSE_STOP_DUR_CLOSE_BY_APPROACH': 2, 'ReminderWhileLock_DOOR_CLOSE_STOP_DUR_CLOSE_BY_NFC_PE': 3, 'ReminderWhileLock_KEY_FORGET_REMINDER_NFC': 4}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class KeyReadReqFromSrv:
        sig_name = "KeyReadReqFromSrv"
        sig_start_bit = 19
        update_id_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocn1_KeyLocnIdle': 0, 'KeyLocn1_KeyLocnAll': 1, 'KeyLocn1_KeyLocnAllExt': 2, 'KeyLocn1_KeyLocnDrvrExt': 3, 'KeyLocn1_KeyLocnPassExt': 4, 'KeyLocn1_KeyLocnTrExt': 5, 'KeyLocn1_KeyLocnAllInt': 6, 'KeyLocn1_KeyLocnDrvrInt': 7, 'KeyLocn1_KeyLocnPassInt': 8, 'KeyLocn1_KeyLocnResvInt': 9, 'KeyLocn1_KeyLocnResvIntSimple': 10}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DKServiceSts:
        sig_name = "DKServiceSts"
        sig_start_bit = 9
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class BgmInfoCanFdDevFr03:
    msg_name = "BgmInfoCanFdDevFr03"
    msg_id = 384
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 48
    tx_node = "BGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'EveKeyId': ['EveKeyIdByte0', 'EveKeyIdByte1', 'EveKeyIdByte10', 'EveKeyIdByte11', 'EveKeyIdByte12', 'EveKeyIdByte13', 'EveKeyIdByte14', 'EveKeyIdByte15', 'EveKeyIdByte2', 'EveKeyIdByte3', 'EveKeyIdByte4', 'EveKeyIdByte5', 'EveKeyIdByte6', 'EveKeyIdByte7', 'EveKeyIdByte8', 'EveKeyIdByte9'], 'KeyReadStsToLockgBLE': ['KeyReadStsToLockgBLEKey0', 'KeyReadStsToLockgBLEKey1', 'KeyReadStsToLockgBLEKey10', 'KeyReadStsToLockgBLEKey11', 'KeyReadStsToLockgBLEKey2', 'KeyReadStsToLockgBLEKey3', 'KeyReadStsToLockgBLEKey4', 'KeyReadStsToLockgBLEKey5', 'KeyReadStsToLockgBLEKey6', 'KeyReadStsToLockgBLEKey7', 'KeyReadStsToLockgBLEKey8', 'KeyReadStsToLockgBLEKey9'], 'BLEKeyReadStsToVMM': ['BLEKeyReadStsToVMMKey0', 'BLEKeyReadStsToVMMKey1', 'BLEKeyReadStsToVMMKey10', 'BLEKeyReadStsToVMMKey11', 'BLEKeyReadStsToVMMKey2', 'BLEKeyReadStsToVMMKey3', 'BLEKeyReadStsToVMMKey4', 'BLEKeyReadStsToVMMKey5', 'BLEKeyReadStsToVMMKey6', 'BLEKeyReadStsToVMMKey7', 'BLEKeyReadStsToVMMKey8', 'BLEKeyReadStsToVMMKey9'], 'KeyReadStsToVMMNFC': ['KeyReadStsToVMMNFCNFCKeyPrsnt', 'KeyReadStsToVMMNFCNFCPsdNotPsd'], 'DoorLockUnlockCmdNFC': ['DoorLockUnlockCmdNFCKeyId1', 'DoorLockUnlockCmdNFCKeyPrsntSts1', 'DoorLockUnlockCmdNFCPsdNotPsd'], 'BLEAccountInfo': ['BLEAccountInfoByte0', 'BLEAccountInfoByte1', 'BLEAccountInfoByte2', 'BLEAccountInfoByte3', 'BLEAccountInfoByte4', 'BLEAccountInfoByte5', 'BLEAccountInfoByte6', 'BLEAccountInfoByte7']}
    sig_group_dataid_dict = {}

    class KeyReadStsToLockgBLEKey5:
        sig_name = "KeyReadStsToLockgBLEKey5"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EveKeyId_UB:
        sig_name = "EveKeyId_UB"
        sig_start_bit = 312
        update_id_bit = 312
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 312
        byte = 39
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BLEAccountInfoByte1:
        sig_name = "BLEAccountInfoByte1"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyIdByte3:
        sig_name = "EveKeyIdByte3"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyReadStsToLockgBLEKey8:
        sig_name = "KeyReadStsToLockgBLEKey8"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EveKeyIdByte14:
        sig_name = "EveKeyIdByte14"
        sig_start_bit = 303
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 303
        byte = 37
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEAccountInfoByte6:
        sig_name = "BLEAccountInfoByte6"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyReadStsToLockgBLEKey10:
        sig_name = "KeyReadStsToLockgBLEKey10"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorLockUnlockCmdNFCKeyPrsntSts1:
        sig_name = "DoorLockUnlockCmdNFCKeyPrsntSts1"
        sig_start_bit = 171
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 171
        byte = 21
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorLockUnlockCmdNFCKeyId1:
        sig_name = "DoorLockUnlockCmdNFCKeyId1"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyId1_Key0': 0, 'KeyId1_Key1': 1, 'KeyId1_Key2': 2, 'KeyId1_Key3': 3, 'KeyId1_Key4': 4, 'KeyId1_Key5': 5, 'KeyId1_Key6': 6, 'KeyId1_Key7': 7, 'KeyId1_Key8': 8, 'KeyId1_Key9': 9, 'KeyId1_Key10': 10, 'KeyId1_Key11': 11}
        compute_method = None
        length = 4
        startbit = 175
        byte = 21
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class KeyReadStsToLockgBLEKey0:
        sig_name = "KeyReadStsToLockgBLEKey0"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class KeyReadStsToLockgBLE_UB:
        sig_name = "KeyReadStsToLockgBLE_UB"
        sig_start_bit = 58
        update_id_bit = 58
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BLEKeyReadStsToVMM_UB:
        sig_name = "BLEKeyReadStsToVMM_UB"
        sig_start_bit = 59
        update_id_bit = 59
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class KeyReadStsToLockgBLEKey11:
        sig_name = "KeyReadStsToLockgBLEKey11"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BLEAccountInfoByte3:
        sig_name = "BLEAccountInfoByte3"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 127
        byte = 15
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyReadStsToVMMNFCNFCPsdNotPsd:
        sig_name = "KeyReadStsToVMMNFCNFCPsdNotPsd"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EveKeyIdByte8:
        sig_name = "EveKeyIdByte8"
        sig_start_bit = 255
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEAccountInfoByte2:
        sig_name = "BLEAccountInfoByte2"
        sig_start_bit = 119
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyReadStsToVMMNFC_UB:
        sig_name = "KeyReadStsToVMMNFC_UB"
        sig_start_bit = 57
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class KeyIdEveTyp:
        sig_name = "KeyIdEveTyp"
        sig_start_bit = 79
        update_id_bit = 81
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Invalid': 0, 'Approach_Light': 1, 'Approach_Second': 2, 'Unlock': 3, 'Reserved1': 4, 'Reserved2': 5}
        compute_method = None
        length = 3
        startbit = 79
        byte = 9
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class KeyReadStsToVMMNFCNFCKeyPrsnt:
        sig_name = "KeyReadStsToVMMNFCNFCKeyPrsnt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class KeyReadStsToLockgBLEKey9:
        sig_name = "KeyReadStsToLockgBLEKey9"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BLEKeyReadStsToVMMKey9:
        sig_name = "BLEKeyReadStsToVMMKey9"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BLEKeyReadStsToVMMKey4:
        sig_name = "BLEKeyReadStsToVMMKey4"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BLEAccountInfoByte4:
        sig_name = "BLEAccountInfoByte4"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEDCChrgLidRKEReq:
        sig_name = "BLEDCChrgLidRKEReq"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EveKeyIdByte2:
        sig_name = "EveKeyIdByte2"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEAccountInfoByte5:
        sig_name = "BLEAccountInfoByte5"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 143
        byte = 17
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyReadStsToVMMKey3:
        sig_name = "BLEKeyReadStsToVMMKey3"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BLEKeyReadStsToVMMKey5:
        sig_name = "BLEKeyReadStsToVMMKey5"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EveKeyIdByte13:
        sig_name = "EveKeyIdByte13"
        sig_start_bit = 295
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 295
        byte = 36
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyIdByte6:
        sig_name = "EveKeyIdByte6"
        sig_start_bit = 239
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyIdByte15:
        sig_name = "EveKeyIdByte15"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 311
        byte = 38
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DoorLockUnlockCmdNFC_UB:
        sig_name = "DoorLockUnlockCmdNFC_UB"
        sig_start_bit = 168
        update_id_bit = 168
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class KeyReadStsToLockgBLEKey3:
        sig_name = "KeyReadStsToLockgBLEKey3"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BLEKeyReadStsToVMMKey8:
        sig_name = "BLEKeyReadStsToVMMKey8"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EveKeyIdByte9:
        sig_name = "EveKeyIdByte9"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 263
        byte = 32
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyReadStsToVMMKey0:
        sig_name = "BLEKeyReadStsToVMMKey0"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BLEKeyReadStsToVMMKey1:
        sig_name = "BLEKeyReadStsToVMMKey1"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EveKeyIdByte4:
        sig_name = "EveKeyIdByte4"
        sig_start_bit = 223
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyIdByte7:
        sig_name = "EveKeyIdByte7"
        sig_start_bit = 247
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyReadStsToVMMKey10:
        sig_name = "BLEKeyReadStsToVMMKey10"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class KeyReadStsToLockgBLEKey4:
        sig_name = "KeyReadStsToLockgBLEKey4"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class KeyReadStsToSrv:
        sig_name = "KeyReadStsToSrv"
        sig_start_bit = 87
        update_id_bit = 95
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EveKeyIdByte1:
        sig_name = "EveKeyIdByte1"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DoorLockUnlockCmdNFCPsdNotPsd:
        sig_name = "DoorLockUnlockCmdNFCPsdNotPsd"
        sig_start_bit = 169
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 169
        byte = 21
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BLEKeyReadStsToVMMKey2:
        sig_name = "BLEKeyReadStsToVMMKey2"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BLEAccountInfoByte0:
        sig_name = "BLEAccountInfoByte0"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyReadStsToVMMKey7:
        sig_name = "BLEKeyReadStsToVMMKey7"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EveKeyIdByte5:
        sig_name = "EveKeyIdByte5"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyIdByte0:
        sig_name = "EveKeyIdByte0"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class KeyReadStsToLockgBLEKey1:
        sig_name = "KeyReadStsToLockgBLEKey1"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class MobDeBtnCarLctrSts:
        sig_name = "MobDeBtnCarLctrSts"
        sig_start_bit = 52
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarFindrHornLiReqFromTelm_NoReq': 0, 'CarFindrHornLiReqFromTelm_HornReq': 1, 'CarFindrHornLiReqFromTelm_LiReq': 2, 'CarFindrHornLiReqFromTelm_HornLiReq': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class BLEKeyReadStsToVMMKey6:
        sig_name = "BLEKeyReadStsToVMMKey6"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class KeyReadStsToLockgBLEKey2:
        sig_name = "KeyReadStsToLockgBLEKey2"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EveKeyIdByte10:
        sig_name = "EveKeyIdByte10"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 271
        byte = 33
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyReadStsToVMMKey11:
        sig_name = "BLEKeyReadStsToVMMKey11"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BLEAccountInfo_UB:
        sig_name = "BLEAccountInfo_UB"
        sig_start_bit = 160
        update_id_bit = 160
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 160
        byte = 20
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class KeyReadReqFromVMM:
        sig_name = "KeyReadReqFromVMM"
        sig_start_bit = 76
        update_id_bit = 80
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocn1_KeyLocnIdle': 0, 'KeyLocn1_KeyLocnAll': 1, 'KeyLocn1_KeyLocnAllExt': 2, 'KeyLocn1_KeyLocnDrvrExt': 3, 'KeyLocn1_KeyLocnPassExt': 4, 'KeyLocn1_KeyLocnTrExt': 5, 'KeyLocn1_KeyLocnAllInt': 6, 'KeyLocn1_KeyLocnDrvrInt': 7, 'KeyLocn1_KeyLocnPassInt': 8, 'KeyLocn1_KeyLocnResvInt': 9, 'KeyLocn1_KeyLocnResvIntSimple': 10}
        compute_method = None
        length = 4
        startbit = 76
        byte = 9
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class EveKeyIdByte11:
        sig_name = "EveKeyIdByte11"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 279
        byte = 34
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MobDevChrgngLidOpnReq:
        sig_name = "MobDevChrgngLidOpnReq"
        sig_start_bit = 85
        update_id_bit = 94
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class KeyReadStsToLockgBLEKey6:
        sig_name = "KeyReadStsToLockgBLEKey6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BLEAccountInfoByte7:
        sig_name = "BLEAccountInfoByte7"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyIdByte12:
        sig_name = "EveKeyIdByte12"
        sig_start_bit = 287
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 287
        byte = 35
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EveKeyTyp:
        sig_name = "EveKeyTyp"
        sig_start_bit = 69
        update_id_bit = 82
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyTyp_NoKeyConnected': 0, 'KeyTyp_NFC_Card': 1, 'KeyTyp_BLE_Key': 2, 'KeyTyp_BLE_UWB_KeyFob': 3, 'KeyTyp_Temp_BLE_Key': 4, 'KeyTyp_ICCE_BLE_Key': 5, 'KeyTyp_ICCE_NFC_Key': 6, 'KeyTyp_CCC_NFC_BLE_UWB_Key': 7, 'KeyTyp_CCC_NFC_Key': 8, 'KeyTyp_CCC_NFC_BLE_Key': 9}
        compute_method = None
        length = 4
        startbit = 69
        byte = 8
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class KeyReadStsToLockgBLEKey7:
        sig_name = "KeyReadStsToLockgBLEKey7"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyPrsntSts1_KeyPrsntStsIdle': 0, 'KeyPrsntSts1_KeyPrsntStsInProgs': 1, 'KeyPrsntSts1_KeyPrsntStsNotPrsnt': 2, 'KeyPrsntSts1_KeyPrsntStsPrsnt': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class BgmInfoCanFdFr18:
    msg_name = "BgmInfoCanFdFr18"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['CDC']
    sig_group_dict = {'SteerWhlScRightButtonLe_2_BgmInfoCanFdSignalIPdu18': ['SteerWhlScRightButtonLeChks_2_BgmInfoCanFdSignalIPdu18', 'SteerWhlScRightButtonLeCntr_2_BgmInfoCanFdSignalIPdu18', 'SteerWhlScRightButtonLeSteerWhlTouchSwt2_2_BgmInfoCanFdSignalIPdu18'], 'SteerWhlScButtonMidLe2_2_BgmInfoCanFdSignalIPdu18': ['SteerWhlScButtonMidLe2Chks_2_BgmInfoCanFdSignalIPdu18', 'SteerWhlScButtonMidLe2Cntr_2_BgmInfoCanFdSignalIPdu18', 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2_2_BgmInfoCanFdSignalIPdu18']}
    sig_group_dataid_dict = {'SteerWhlScRightButtonLe_2_BgmInfoCanFdSignalIPdu18': 8090, 'SteerWhlScButtonMidLe2_2_BgmInfoCanFdSignalIPdu18': 8088}

    class SteerWhlScButtonMidLe2Cntr_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScButtonMidLe2Cntr_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 83
        byte = 10
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlScRightButtonLeCntr_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScRightButtonLeCntr_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HmiAndAudReq_1_BgmInfoCanFdSignalIPdu18:
        sig_name = "HmiAndAudReq_1_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 15
        update_id_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVBattPumpFltSts_1_BgmInfoCanFdSignalIPdu18:
        sig_name = "HVBattPumpFltSts_1_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 11
        update_id_bit = 12
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PumpFltSts_No_Error': 0, 'PumpFltSts_Short_to_battery': 1, 'PumpFltSts_Short_to_GND': 2, 'PumpFltSts_Open_circuit': 3, 'PumpFltSts_Over_temperature': 4, 'PumpFltSts_Over_voltage': 5, 'PumpFltSts_Stuck': 6, 'PumpFltSts_DryRun': 7, 'PumpFltSts_Pending': 8}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlScRightButtonLeChks_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScRightButtonLeChks_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SteerWhlScRightButtonLeSteerWhlTouchSwt2_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScRightButtonLeSteerWhlTouchSwt2_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt_NotAvailble': 0, 'SteerWhlTouchSwt_ShortPress': 1, 'SteerWhlTouchSwt_LongPress': 2, 'SteerWhlTouchSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlScButtonMidLe2SteerWhlTouchSwt2_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScButtonMidLe2SteerWhlTouchSwt2_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt_NotAvailble': 0, 'SteerWhlTouchSwt_ShortPress': 1, 'SteerWhlTouchSwt_LongPress': 2, 'SteerWhlTouchSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlScRightButtonLe_2_BgmInfoCanFdSignalIPdu18_UB:
        sig_name = "SteerWhlScRightButtonLe_2_BgmInfoCanFdSignalIPdu18_UB"
        sig_start_bit = 4
        update_id_bit = 4
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerWhlScButtonMidLe2_2_BgmInfoCanFdSignalIPdu18_UB:
        sig_name = "SteerWhlScButtonMidLe2_2_BgmInfoCanFdSignalIPdu18_UB"
        sig_start_bit = 64
        update_id_bit = 64
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CarTiGlb_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "CarTiGlb_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 39
        update_id_bit = 13
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlScLeftButtonRi_1_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScLeftButtonRi_1_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchSwt_NotAvailble': 0, 'SteerWhlTouchSwt_ShortPress': 1, 'SteerWhlTouchSwt_LongPress': 2, 'SteerWhlTouchSwt_Error': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlScButtonMidLe2Chks_2_BgmInfoCanFdSignalIPdu18:
        sig_name = "SteerWhlScButtonMidLe2Chks_2_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BgmInfoCanFdDevFr02:
    msg_name = "BgmInfoCanFdDevFr02"
    msg_id = 608
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "BGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'CarModChgRsp': ['CarModChgRspAlrmIssue', 'CarModChgRspCarModSts1', 'CarModChgRspStaticIssue', 'CarModChgRspStatus']}
    sig_group_dataid_dict = {}

    class CarModChgRspStaticIssue:
        sig_name = "CarModChgRspStaticIssue"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StaticIssue_Idle': 0, 'StaticIssue_NotCorrect': 1}
        compute_method = None
        length = 8
        startbit = 95
        byte = 11
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PwrEstimdAtStbForVisy:
        sig_name = "PwrEstimdAtStbForVisy"
        sig_start_bit = 5
        update_id_bit = 30
        sig_length = 11
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class UsgModKeeperReqAct:
        sig_name = "UsgModKeeperReqAct"
        sig_start_bit = 23
        update_id_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DrvrStrtReq:
        sig_name = "DrvrStrtReq"
        sig_start_bit = 7
        update_id_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StrtReq2_NotReqd': 0, 'StrtReq2_Reqd': 1, 'StrtReq2_RemReqd': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CarModChgRspAlrmIssue:
        sig_name = "CarModChgRspAlrmIssue"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmIssue_Idle': 0, 'AlrmIssue_NotCorrect': 1}
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class StartInhibitSts:
        sig_name = "StartInhibitSts"
        sig_start_bit = 10
        update_id_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CarModChgRspStatus:
        sig_name = "CarModChgRspStatus"
        sig_start_bit = 103
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Status_Idle': 0, 'Status_Failure': 1, 'Status_Succeed': 2}
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CarModChgRsp_UB:
        sig_name = "CarModChgRsp_UB"
        sig_start_bit = 104
        update_id_bit = 104
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 104
        byte = 13
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class UsgModKeeperReq:
        sig_name = "UsgModKeeperReq"
        sig_start_bit = 35
        update_id_bit = 46
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CarModChgReq:
        sig_name = "CarModChgReq"
        sig_start_bit = 63
        update_id_bit = 79
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModeReq_NORMAL': 0, 'CarModeReq_TRANSPORT': 1, 'CarModeReq_FACTORY': 2, 'CarModeReq_CRASH': 3, 'CarModeReq_IDLE': 4, 'CarModeReq_DYNO': 5}
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class UsgModDrvProxyReq:
        sig_name = "UsgModDrvProxyReq"
        sig_start_bit = 9
        update_id_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class KeyReadReqFromLockg:
        sig_name = "KeyReadReqFromLockg"
        sig_start_bit = 71
        update_id_bit = 78
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyLocn1_KeyLocnIdle': 0, 'KeyLocn1_KeyLocnAll': 1, 'KeyLocn1_KeyLocnAllExt': 2, 'KeyLocn1_KeyLocnDrvrExt': 3, 'KeyLocn1_KeyLocnPassExt': 4, 'KeyLocn1_KeyLocnTrExt': 5, 'KeyLocn1_KeyLocnAllInt': 6, 'KeyLocn1_KeyLocnDrvrInt': 7, 'KeyLocn1_KeyLocnPassInt': 8, 'KeyLocn1_KeyLocnResvInt': 9, 'KeyLocn1_KeyLocnResvIntSimple': 10}
        compute_method = None
        length = 4
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class MobDevRPAReqResp:
        sig_name = "MobDevRPAReqResp"
        sig_start_bit = 67
        update_id_bit = 77
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 67
        byte = 8
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class UsgModDwnSwtReq:
        sig_name = "UsgModDwnSwtReq"
        sig_start_bit = 39
        update_id_bit = 47
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class UsgModProxyKeepLow:
        sig_name = "UsgModProxyKeepLow"
        sig_start_bit = 19
        update_id_bit = 26
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CarModChgRspCarModSts1:
        sig_name = "CarModChgRspCarModSts1"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModSts1_CarModNorm': 0, 'CarModSts1_CarModTrnsp': 1, 'CarModSts1_CarModFcy': 2, 'CarModSts1_CarModCrash': 3, 'CarModSts1_CarModDyno': 5}
        compute_method = None
        length = 3
        startbit = 111
        byte = 13
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FOTAStatus:
        sig_name = "FOTAStatus"
        sig_start_bit = 55
        update_id_bit = 42
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'Query': 1, 'Downloading': 2, 'Active': 3, 'Update': 4, 'Rollback': 5, 'UpdateFailNotDriving': 6}
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CdcInfoCANFDNmFr:
    msg_name = "CdcInfoCANFDNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmInfoCanFdFr19:
    msg_name = "BgmInfoCanFdFr19"
    msg_id = 789
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']
    sig_group_dict = {'VehTiAndData_3_BgmInfoCanFdSignalIPdu19': ['VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19', 'VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19', 'VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19', 'VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19', 'VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19', 'VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19', 'VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19']}
    sig_group_dataid_dict = {}

    class VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 13
        byte = 1
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 5
        byte = 0
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndData_3_BgmInfoCanFdSignalIPdu19_UB:
        sig_name = "VehTiAndData_3_BgmInfoCanFdSignalIPdu19_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 46
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CdcInfoCanFdFr03:
    msg_name = "CdcInfoCanFdFr03"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class MmedHdPwrMod:
        sig_name = "MmedHdPwrMod"
        sig_start_bit = 27
        update_id_bit = 37
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MmedMaiPwrMod_OnlyMCURunning': 0, 'MmedMaiPwrMod_STR': 1, 'MmedMaiPwrMod_SystemInit': 2, 'MmedMaiPwrMod_HMIOFF': 3, 'MmedMaiPwrMod_RunMode': 4, 'MmedMaiPwrMod_RemoteMode': 5, 'MmedMaiPwrMod_ReadyToSTR': 6, 'MmedMaiPwrMod_ReadyToSleep': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class BgmInfoCanFdDevFr01:
    msg_name = "BgmInfoCanFdDevFr01"
    msg_id = 225
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'DigKeyApproachReq': ['DigKeyApproachReqDigKeyApproaReq', 'DigKeyApproachReqKeyId1']}
    sig_group_dataid_dict = {}

    class DigKeyApproachReqDigKeyApproaReq:
        sig_name = "DigKeyApproachReqDigKeyApproaReq"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DigKeyApproaReq_Idle': 0, 'DigKeyApproaReq_ApproachLightRequest': 1, 'DigKeyApproaReq_ApproachUnlockRequest': 2, 'DigKeyApproaReq_ApproachLockRequest': 3, 'DigKeyApproaReq_ApproachTrunkRequest1': 4, 'DigKeyApproaReq_ApproachTrunkRequest2': 5, 'DigKeyApproaReq_ApproachTrunkRequest3': 6, 'DigKeyApproaReq_ApproachUnlckReqFromDrvr': 7}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BattCpRel:
        sig_name = "BattCpRel"
        sig_start_bit = 7
        update_id_bit = 20
        sig_length = 8
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BattRFild:
        sig_name = "BattRFild"
        sig_start_bit = 15
        update_id_bit = 19
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BattSnsrCalcnNotVldFild:
        sig_name = "BattSnsrCalcnNotVldFild"
        sig_start_bit = 23
        update_id_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DigKeyApproachReqKeyId1:
        sig_name = "DigKeyApproachReqKeyId1"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'KeyId1_Key0': 0, 'KeyId1_Key1': 1, 'KeyId1_Key2': 2, 'KeyId1_Key3': 3, 'KeyId1_Key4': 4, 'KeyId1_Key5': 5, 'KeyId1_Key6': 6, 'KeyId1_Key7': 7, 'KeyId1_Key8': 8, 'KeyId1_Key9': 9, 'KeyId1_Key10': 10, 'KeyId1_Key11': 11}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DigKeyApproachReq_UB:
        sig_name = "DigKeyApproachReq_UB"
        sig_start_bit = 32
        update_id_bit = 32
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class BgmInfoCanFdFr23:
    msg_name = "BgmInfoCanFdFr23"
    msg_id = 80
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']
    sig_group_dict = {'AccrPedlRat_2_BgmInfoCanFdSignalIPdu23': ['AccrPedlRatAccrPedlRat_2_BgmInfoCanFdSignalIPdu23', 'AccrPedlRatChks_2_BgmInfoCanFdSignalIPdu23', 'AccrPedlRatCntr_2_BgmInfoCanFdSignalIPdu23']}
    sig_group_dataid_dict = {'AccrPedlRat_2_BgmInfoCanFdSignalIPdu23': 868}

    class AccrPedlRatChks_2_BgmInfoCanFdSignalIPdu23:
        sig_name = "AccrPedlRatChks_2_BgmInfoCanFdSignalIPdu23"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AccrPedlRat_2_BgmInfoCanFdSignalIPdu23_UB:
        sig_name = "AccrPedlRat_2_BgmInfoCanFdSignalIPdu23_UB"
        sig_start_bit = 39
        update_id_bit = 39
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AccrPedlRatCntr_2_BgmInfoCanFdSignalIPdu23:
        sig_name = "AccrPedlRatCntr_2_BgmInfoCanFdSignalIPdu23"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AccrPedlRatAccrPedlRat_2_BgmInfoCanFdSignalIPdu23:
        sig_name = "AccrPedlRatAccrPedlRat_2_BgmInfoCanFdSignalIPdu23"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]


class CdcInfoCanFdFr04:
    msg_name = "CdcInfoCanFdFr04"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AsySftyHWLReqBkp:
        sig_name = "AsySftyHWLReqBkp"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AsySftyHWLReq_NoRequest': 0, 'AsySftyHWLReq_TurnOn': 1, 'AsySftyHWLReq_TurnOff': 2, 'AsySftyHWLReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OutsidePrkOutReq_0_CdcInfoCanFdSignalIPdu04:
        sig_name = "OutsidePrkOutReq_0_CdcInfoCanFdSignalIPdu04"
        sig_start_bit = 23
        update_id_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BgmInfoCanFdFr20:
    msg_name = "BgmInfoCanFdFr20"
    msg_id = 821
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 32
    tx_node = "BGM"
    rx_nodes = ['CDC']
    sig_group_dict = {'BLEKeyPrsntSts_1_BgmInfoCanFdSignalIPdu20': ['BLEKeyPrsntStsChks_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsCntr_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone0_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone10_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone11_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone12_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone13_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone14_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone15_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone1_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone2_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone3_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone4_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone5_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone6_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone7_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone8_1_BgmInfoCanFdSignalIPdu20', 'BLEKeyPrsntStsZone9_1_BgmInfoCanFdSignalIPdu20']}
    sig_group_dataid_dict = {'BLEKeyPrsntSts_1_BgmInfoCanFdSignalIPdu20': 8513}

    class ReLeOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReLeOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 239
        update_id_bit = 148
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 239
        byte = 29
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone10_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone10_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 177
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 177
        byte = 22
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BLEKeyPrsntStsZone12_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone12_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 191
        byte = 23
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class OutdLeOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdLeOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 199
        update_id_bit = 143
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone5_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone5_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 182
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 182
        byte = 22
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BLEKeyPrsntStsZone8_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone8_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 179
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 179
        byte = 22
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AudWarnOfSnsrParkAssiRgtPosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiRgtPosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 20
        update_id_bit = 124
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class BLEKeyPrsntStsChks_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsChks_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 167
        byte = 20
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 231
        update_id_bit = 149
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 31
        update_id_bit = 123
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone13_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone13_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 190
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 190
        byte = 23
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class InsdRiOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdRiOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 111
        update_id_bit = 132
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OutdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 85
        update_id_bit = 138
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ReRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 247
        update_id_bit = 147
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OutdLeOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdLeOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 207
        update_id_bit = 142
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 207
        byte = 25
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone1_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone1_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 174
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 174
        byte = 21
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class OutdRiOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdRiOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 223
        update_id_bit = 140
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 223
        byte = 27
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class InsdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 57
        update_id_bit = 128
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BLEKeyPrsntStsCntr_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsCntr_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 171
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 171
        byte = 21
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class InsdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 59
        update_id_bit = 129
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BLEKeyPrsntStsZone0_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone0_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 175
        byte = 21
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BLEKeyPrsntSts_1_BgmInfoCanFdSignalIPdu20_UB:
        sig_name = "BLEKeyPrsntSts_1_BgmInfoCanFdSignalIPdu20_UB"
        sig_start_bit = 156
        update_id_bit = 156
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 156
        byte = 19
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AudWarnLvOfSnsrParkAssiLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 5
        update_id_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SnsrFltFrntShoSideRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltFrntShoSideRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 89
        update_id_bit = 144
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 89
        byte = 11
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class OutdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 81
        update_id_bit = 136
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 81
        byte = 10
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReRiOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReRiOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 255
        update_id_bit = 146
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 255
        byte = 31
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class InsdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 61
        update_id_bit = 130
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AudWarnLvOfSnsrParkAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AudWarnLvOfSnsrParkAssiRgt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiRgt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 1
        update_id_bit = 112
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BLEKeyPrsntStsZone11_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone11_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 176
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 176
        byte = 22
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BLEKeyPrsntStsZone9_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone9_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 178
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 178
        byte = 22
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class InsdLeOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdLeOfSnsrPrkgAssiRe_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 79
        update_id_bit = 134
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone3_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone3_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 172
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 172
        byte = 21
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BLEKeyPrsntStsZone14_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone14_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 189
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 189
        byte = 23
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BLEKeyPrsntStsZone15_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone15_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 188
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 188
        byte = 23
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PrkgDstCtrlSts_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "PrkgDstCtrlSts_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 95
        update_id_bit = 151
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgDstCtrlSysSts_Off': 0, 'PrkgDstCtrlSysSts_Standby': 1, 'PrkgDstCtrlSysSts_FrontRearActive': 2, 'PrkgDstCtrlSysSts_FrontActive': 3, 'PrkgDstCtrlSysSts_RearActive': 4, 'PrkgDstCtrlSysSts_SystemFailure': 5, 'PrkgDstCtrlSysSts_Inhibited': 6, 'PrkgDstCtrlSysSts_Initialize': 7, 'PrkgDstCtrlSysSts_Covered': 8, 'PrkgDstCtrlSysSts_FrontActiveTrailerMode': 9, 'PrkgDstCtrlSysSts_Reserved1': 10, 'PrkgDstCtrlSysSts_Reserved2': 11, 'PrkgDstCtrlSysSts_Reserved3': 12, 'PrkgDstCtrlSysSts_Reserved4': 13, 'PrkgDstCtrlSysSts_Reserved5': 14, 'PrkgDstCtrlSysSts_Reserved6': 15}
        compute_method = None
        length = 4
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnLvOfSnsrParkAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiRe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 3
        update_id_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerOFF': 0, 'BuzzerON_Keep': 1, 'BuzzerON_2Hz': 2, 'BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InsdRiOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdRiOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 103
        update_id_bit = 133
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OutdRiOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdRiOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 215
        update_id_bit = 141
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone7_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone7_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 180
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 180
        byte = 22
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SnsrFltOfPrkgDstCtrl_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltOfPrkgDstCtrl_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 119
        update_id_bit = 159
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltOfPrkgDstCtrl2_NoFault': 0, 'SnsrFltOfPrkgDstCtrl2_Front_USS_Fault': 1, 'SnsrFltOfPrkgDstCtrl2_Rear_USS_Fault': 2, 'SnsrFltOfPrkgDstCtrl2_Front_and_Rear_USS_Fault': 3, 'SnsrFltOfPrkgDstCtrl2_Reserve1': 4, 'SnsrFltOfPrkgDstCtrl2_Reserve2': 5, 'SnsrFltOfPrkgDstCtrl2_Reserve3': 6, 'SnsrFltOfPrkgDstCtrl2_Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 119
        byte = 14
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BLEKeyPrsntStsZone4_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone4_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 183
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 183
        byte = 22
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PrkgDstCtrlWarn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "PrkgDstCtrlWarn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 9
        update_id_bit = 150
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WarningInd_NoWarning': 0, 'WarningInd_Warning': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SnsrFltReShoSideLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltReShoSideLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 116
        update_id_bit = 158
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 116
        byte = 14
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SnsrFltFrntShoSideLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltFrntShoSideLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 91
        update_id_bit = 145
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 91
        byte = 11
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InsdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 63
        update_id_bit = 131
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BLEKeyPrsntStsZone2_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone2_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 173
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 173
        byte = 21
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AudWarnOfSnsrParkAssiRePosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiRePosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 23
        update_id_bit = 125
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class SnsrFltReShoSideRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltReShoSideRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 114
        update_id_bit = 157
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 114
        byte = 14
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class FrntLeOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntLeOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 39
        update_id_bit = 122
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AudWarnOfSnsrParkAssiFrntPosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiFrntPosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 15
        update_id_bit = 127
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class OutdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 87
        update_id_bit = 139
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class InsdLeOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdLeOfSnsrPrkgAssiFrnt_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 71
        update_id_bit = 135
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AudWarnOfSnsrParkAssiLePosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiLePosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 12
        update_id_bit = 126
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoRequest': 0, 'Region1': 1, 'Region2': 2, 'Region3': 3, 'Region4': 4, 'Reserve': 5}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class OutdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 83
        update_id_bit = 137
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntRiOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntRiOfSnsrOfPrkgAssiSide_2_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 55
        update_id_bit = 120
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FrntRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 47
        update_id_bit = 121
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BLEKeyPrsntStsZone6_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "BLEKeyPrsntStsZone6_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 181
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Validity_NotValid': 0, 'Validity_Valid': 1}
        compute_method = None
        length = 1
        startbit = 181
        byte = 22
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class BgmInfoCANFDNmFr:
    msg_name = "BgmInfoCANFDNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmInfoCanFdDevFr04:
    msg_name = "BgmInfoCanFdDevFr04"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FCSILEDIndctn_0_BgmInfoCanFdDevSignalIPdu04:
        sig_name = "FCSILEDIndctn_0_BgmInfoCanFdDevSignalIPdu04"
        sig_start_bit = 22
        update_id_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NO_COLOR': 0, 'WHITE': 1, 'BLUE': 2, 'GREEN_BREATH': 3, 'GREEN': 4, 'BLUE_BREATH': 5, 'RESERVED': 6, 'RED': 7}
        compute_method = None
        length = 3
        startbit = 22
        byte = 2
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class MobDevAVPReq:
        sig_name = "MobDevAVPReq"
        sig_start_bit = 6
        update_id_bit = 30
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AVPFct_NoReq': 0, 'AVPFct_StartPrepare': 1, 'AVPFct_Start': 2, 'AVPFct_Stop': 3, 'AVPFct_StopRecover': 4, 'AVPFct_Out': 5, 'AVPFct_Reserved1': 6, 'AVPFct_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class MobDevRPAReq:
        sig_name = "MobDevRPAReq"
        sig_start_bit = 3
        update_id_bit = 29
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RPAReqJIDU_NoRequest': 0, 'RPAReqJIDU_RPA_Start_Request': 1, 'RPAReqJIDU_APA_Quit_Request': 2, 'RPAReqJIDU_ParkOutMod_Request': 3, 'RPAReqJIDU_APA_ParkOut_Request': 4, 'RPAReqJIDU_Park_Out_Front_Left': 5, 'RPAReqJIDU_Park_Out_Front_Right': 6, 'RPAReqJIDU_Park_Out_Rear_Left': 7, 'RPAReqJIDU_Park_Out_Rear_Right': 8, 'RPAReqJIDU_Park_Out_Left_Front': 9, 'RPAReqJIDU_Park_Out_Right_Front': 10, 'RPAReqJIDU_APA_Pausing_Request': 11, 'RPAReqJIDU_APA_Continue_Request': 12, 'RPAReqJIDU_Quit_Because_Mobile_Device_Power_Low': 13, 'RPAReqJIDU_Park_Out_Front': 14, 'RPAReqJIDU_Park_Out_Rear': 15}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehICns:
        sig_name = "VehICns"
        sig_start_bit = 15
        update_id_bit = 28
        sig_length = 9
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b10000000, 0b01111111, 1, 7)]

    class IgnRlyFb_1_BgmInfoCanFdDevSignalIPdu04:
        sig_name = "IgnRlyFb_1_BgmInfoCanFdDevSignalIPdu04"
        sig_start_bit = 7
        update_id_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CdcInfoCanFdFr12:
    msg_name = "CdcInfoCanFdFr12"
    msg_id = 192
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 16
    tx_node = "CDC"
    rx_nodes = ['BGM']
    sig_group_dict = {'CDCDrvrGearShiftDirReq2_0_CdcInfoCanFdSignalIPdu12': ['CDCDrvrGearShiftDirReq2Chks_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq2Cntr_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq2DwnRTipAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq2DwnTipAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq2PosnAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq2UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq2UpTipAut_0_CdcInfoCanFdSignalIPdu12'], 'CDCDrvrGearShiftDirReq1_0_CdcInfoCanFdSignalIPdu12': ['CDCDrvrGearShiftDirReq1Chks_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq1Cntr_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq1DwnRTipAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq1DwnTipAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq1PosnAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12'], 'CDCDrvrGearShiftParkReq_0_CdcInfoCanFdSignalIPdu12': ['CDCDrvrGearShiftParkReq1_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftParkReqChks_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftParkReqCntr_0_CdcInfoCanFdSignalIPdu12', 'CDCDrvrGearShiftParkReqSts_0_CdcInfoCanFdSignalIPdu12']}
    sig_group_dataid_dict = {'CDCDrvrGearShiftDirReq2_0_CdcInfoCanFdSignalIPdu12': 8045, 'CDCDrvrGearShiftDirReq1_0_CdcInfoCanFdSignalIPdu12': 8044, 'CDCDrvrGearShiftParkReq_0_CdcInfoCanFdSignalIPdu12': 8511}

    class CDCDrvrGearShiftDirReq2_0_CdcInfoCanFdSignalIPdu12_UB:
        sig_name = "CDCDrvrGearShiftDirReq2_0_CdcInfoCanFdSignalIPdu12_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CDCDrvrGearShiftParkReq1_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftParkReq1_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtPark1_SwtParkNotActv': 0, 'SwtPark1_SwtParkActv': 1}
        compute_method = None
        length = 1
        startbit = 71
        byte = 8
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCDrvrGearShiftParkReqCntr_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftParkReqCntr_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CDCDrvrGearShiftDirReq2DwnRTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2DwnRTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCDrvrGearShiftParkReqChks_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftParkReqChks_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCDrvrGearShiftDirReq1_0_CdcInfoCanFdSignalIPdu12_UB:
        sig_name = "CDCDrvrGearShiftDirReq1_0_CdcInfoCanFdSignalIPdu12_UB"
        sig_start_bit = 16
        update_id_bit = 16
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CDCDrvrGearShiftDirReq2Chks_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2Chks_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCGearShiftUnitSt_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCGearShiftUnitSt_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFlt': 0, 'NoUpTipAut': 1, 'NoDwnTipAut': 2, 'NoPark': 3, 'SrvRqrd': 4, 'NoUpUpTipAut': 5, 'NoDownDownTipAut': 6, 'Nounlock': 7}
        compute_method = None
        length = 3
        startbit = 79
        byte = 9
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CDCDrvrGearShiftParkReq_0_CdcInfoCanFdSignalIPdu12_UB:
        sig_name = "CDCDrvrGearShiftParkReq_0_CdcInfoCanFdSignalIPdu12_UB"
        sig_start_bit = 64
        update_id_bit = 64
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1UpTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UpTipAut1_UpTipAutNotActv': 0, 'UpTipAut1_UpTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CDCDrvrGearShiftDirReq2UpDTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2UpDTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CDCDrvrGearShiftDirReq1Chks_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1Chks_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCDrvrGearShiftDirReq1PosnAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1PosnAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnAut_PosnAutNotActv': 0, 'PosnAut_PosnAutActv': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CDCDrvrGearShiftParkReqSts_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftParkReqSts_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 70
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClutchPedlPsd_No': 0, 'ClutchPedlPsd_Yes': 1, 'ClutchPedlPsd_Reserved1': 2, 'ClutchPedlPsd_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 70
        byte = 8
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1UpDTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CDCDrvrGearShiftDirReq1DwnTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1DwnTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DwnTipAut1_DwnTipAutNotActv': 0, 'DwnTipAut1_DwnTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CDCDrvrGearShiftDirReq1Cntr_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1Cntr_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CDCDrvrGearShiftDirReq2DwnTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2DwnTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DwnTipAut1_DwnTipAutNotActv': 0, 'DwnTipAut1_DwnTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CDCDrvrGearShiftDirReq1DwnRTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq1DwnRTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCDrvrGearShiftDirReq2UpTipAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2UpTipAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UpTipAut1_UpTipAutNotActv': 0, 'UpTipAut1_UpTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CDCDrvrGearShiftDirReq2Cntr_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2Cntr_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CDCDrvrGearShiftDirReq2PosnAut_0_CdcInfoCanFdSignalIPdu12:
        sig_name = "CDCDrvrGearShiftDirReq2PosnAut_0_CdcInfoCanFdSignalIPdu12"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnAut_PosnAutNotActv': 0, 'PosnAut_PosnAutActv': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CdcInfoCanFdFr11:
    msg_name = "CdcInfoCanFdFr11"
    msg_id = 1104
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.32
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']
    sig_group_dict = {'CDCActT_0_CdcInfoCanFdSignalIPdu11': ['CDCActTEngT_0_CdcInfoCanFdSignalIPdu11', 'CDCActTEngTQf_0_CdcInfoCanFdSignalIPdu11']}
    sig_group_dataid_dict = {}

    class CDCActTEngT_0_CdcInfoCanFdSignalIPdu11:
        sig_name = "CDCActTEngT_0_CdcInfoCanFdSignalIPdu11"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCActTEngTQf_0_CdcInfoCanFdSignalIPdu11:
        sig_name = "CDCActTEngTQf_0_CdcInfoCanFdSignalIPdu11"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CDCActT_0_CdcInfoCanFdSignalIPdu11_UB:
        sig_name = "CDCActT_0_CdcInfoCanFdSignalIPdu11_UB"
        sig_start_bit = 12
        update_id_bit = 12
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CDCCoolantFlwReq_0_CdcInfoCanFdSignalIPdu11:
        sig_name = "CDCCoolantFlwReq_0_CdcInfoCanFdSignalIPdu11"
        sig_start_bit = 23
        update_id_bit = 29
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]


class BgmInfoCanFdFr17:
    msg_name = "BgmInfoCanFdFr17"
    msg_id = 800
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['S2SReceiver', 'CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class GearLvrIllmnSts_1_BgmInfoCanFdSignalIPdu17:
        sig_name = "GearLvrIllmnSts_1_BgmInfoCanFdSignalIPdu17"
        sig_start_bit = 63
        update_id_bit = 62
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class GearLvrFaultIndcn_1_BgmInfoCanFdSignalIPdu17:
        sig_name = "GearLvrFaultIndcn_1_BgmInfoCanFdSignalIPdu17"
        sig_start_bit = 61
        update_id_bit = 58
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFlt': 0, 'CDCFltEGSMNoFlt': 1, 'CDCSerFltEGSMSligtFlt': 2, 'CDCNoFltEGSMFlt': 3, 'CDCSligtFltEGSMSerFlt': 4, 'CDCSerFltEGSMSerFlt': 5}
        compute_method = None
        length = 3
        startbit = 61
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class IndirectLifeDetnAndCareDiWarn:
        sig_name = "IndirectLifeDetnAndCareDiWarn"
        sig_start_bit = 29
        update_id_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WhlSpdCmpFac_1_BgmInfoCanFdSignalIPdu17:
        sig_name = "WhlSpdCmpFac_1_BgmInfoCanFdSignalIPdu17"
        sig_start_bit = 47
        update_id_bit = 50
        sig_length = 5
        sig_value_factor = 0.005
        sig_value_offset = 0.92
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 16
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 47
        byte = 5
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class IndirectLifeDetnAndCareLvl1Warn:
        sig_name = "IndirectLifeDetnAndCareLvl1Warn"
        sig_start_bit = 28
        update_id_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class CdcInfoCanFdFr10:
    msg_name = "CdcInfoCanFdFr10"
    msg_id = 784
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class NOPCoolReqFromCDC_0_CdcInfoCanFdSignalIPdu10:
        sig_name = "NOPCoolReqFromCDC_0_CdcInfoCanFdSignalIPdu10"
        sig_start_bit = 7
        update_id_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7



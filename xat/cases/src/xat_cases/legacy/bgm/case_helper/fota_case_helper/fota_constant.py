'''
Author: tom
Date: 2023-02-13 13:32:45
LastEditors: Do not edit
LastEditTime: 2023-07-20 12:54:06
FilePath: /yangliu/sat/xat_cases/legacy/bgm/case_helper/fota_case_helper/fota_constant.py
'''

FOTA_ERROR_CODE_LISTS = [
    '"stateCode":"0102"',
    '"stateCode":"0103"',
    '"stateCode":"0201"',
    '"stateCode":"0202"',
    '"stateCode":"0203"',
    '"stateCode":"0204"',
    '"stateCode":"0205"',
    '"stateCode":"0206"',
    '"stateCode":"0207"',
    '"stateCode":"0208"',
    '"stateCode":"0209"',
    '"stateCode":"020A"',
    '"stateCode":"020B"',
    '"stateCode":"020C"',
    '"stateCode":"020D"',
    '"stateCode":"020E"',
    '"stateCode":"020F"',
    '"stateCode":"0210"',
    '"stateCode":"0211"',
    '"stateCode":"0212"',    
    '"stateCode":"0213"',
    '"stateCode":"0214"',
    '"stateCode":"0215"',
    '"stateCode":"0216"',
    '"stateCode":"0217"',
    '"stateCode":"0218"',    
    '"stateCode":"0219"',
    '"stateCode":"021A"',
    '"stateCode":"021B"',
    '"stateCode":"021D"',
    '"stateCode":"021E"',
    '"stateCode":"0220"',
    '"stateCode":"0221"',
    '"stateCode":"0222"',
    '"stateCode":"02F3"',
    '"stateCode":"0102"',
    '"stateCode":"0103"',
    '"stateCode":"0202"',
    '"stateCode":"0203"',
    '"stateCode":"0204"',  
    '"stateCode":"0205"',
    '"stateCode":"0206"',
    '"stateCode":"0207"',
    '"stateCode":"0208"',
    '"stateCode":"0209"',
    '"stateCode":"020A"',
    '"stateCode":"020B"',
    '"stateCode":"020C"',
    '"stateCode":"020D"',
    '"stateCode":"020E"',
    '"stateCode":"020F"',
    '"stateCode":"0210"',
    '"stateCode":"0211"',
    '"stateCode":"0212"',
    '"stateCode":"0213"',
    '"stateCode":"0214"',
    '"stateCode":"0215"',
    '"stateCode":"0216"',
    '"stateCode":"0217"',
    '"stateCode":"0218"',
    '"stateCode":"0219"',
    '"stateCode":"021A"',
    '"stateCode":"021B"',
    '"stateCode":"021C"',
    '"stateCode":"021D"',
    '"stateCode":"021E"',
    '"stateCode":"021F"',
    '"stateCode":"0220"',
    '"stateCode":"0221"',
    '"stateCode":"0222"',
    '"stateCode":"02F4"',
    '"stateCode":"0301"',
    '"stateCode":"03F1"',
    '"stateCode":"03F2"',
    '"stateCode":"03F3"',
    '"stateCode":"0305"',
    '"stateCode":"0306"',
    '"stateCode":"0307"',
    '"stateCode":"03F5"',
    '"stateCode":"0308"',
    '"stateCode":"0309"',
    '"stateCode":"030A"',
    '"stateCode":"030B"',
    '"stateCode":"030C"',
    '"stateCode":"030D"',
    '"stateCode":"030E"',
    '"stateCode":"030F"',
    '"stateCode":"0310"',
    '"stateCode":"0311"',
    '"stateCode":"0312"',
    '"stateCode":"0313"',
    '"stateCode":"0314"',
    '"stateCode":"0315"',
    '"stateCode":"0316"',
    '"stateCode":"0317"',
    '"stateCode":"0318"',
    '"stateCode":"0319"',
    '"stateCode":"031A"',
    '"stateCode":"031B"',
    '"stateCode":"031C"',
    '"stateCode":"031D"',
    '"stateCode":"031F"',
    '"stateCode":"0320"',
    '"stateCode":"0321"',
    '"stateCode":"0322"',
    '"stateCode":"0323"',
    '"stateCode":"0324"',
    '"stateCode":"0325"',
    '"stateCode":"0326"',
    '"stateCode":"0327"',
    '"stateCode":"0328"',
    '"stateCode":"0329"',
    '"stateCode":"032A"',
    '"stateCode":"032B"',
    '"stateCode":"0000"',
    '"stateCode":"0301"',
    '"stateCode":"0308"',
    '"stateCode":"0309"',
    '"stateCode":"030A"',
    '"stateCode":"030B"',
    '"stateCode":"030C"',
    '"stateCode":"030D"',
    '"stateCode":"030E"',
    '"stateCode":"030F"',
    '"stateCode":"0310"',
    '"stateCode":"0311"',
    '"stateCode":"0312"',
    '"stateCode":"0313"',
    '"stateCode":"0314"',
    '"stateCode":"0315"',
    '"stateCode":"0316"',
    '"stateCode":"0317"',
    '"stateCode":"0318"',
    '"stateCode":"0319"',
    '"stateCode":"031A"',
    '"stateCode":"031B"',
    '"stateCode":"031C"',
    '"stateCode":"031D"',
    '"stateCode":"031F"',
    '"stateCode":"0320"',
    '"stateCode":"0321"',
    '"stateCode":"0322"',
    '"stateCode":"0323"',
    '"stateCode":"0324"',
    '"stateCode":"0325"',
    '"stateCode":"0326"',
    '"stateCode":"0327"',
    '"stateCode":"0328"',
    '"stateCode":"0329"',
    '"stateCode":"032A"',
    '"stateCode":"0F01"',
    '"stateCode":"0302"',
    '"stateCode":"03F7"',
    '"stateCode":"03F8"'
    ]

FOTA_FACTORY_END_WORDS = [
    'FOTA Status:23',
    'factory_file_suffix is not match',
    'init => update_status_sync'
]

VERSION_DEBUG_FRONT_PRO = '''{\\"data\\":{\\"baseLineVer\\":\\"6100000055 BL\\",\\"ecu\\":[
{\\"HWPN\\":\\"8895036214  F\\",\\"SWPN\\":\\"6160110065 NA,2960110065 AA\\",\\"ecuId\\":\\"6011\\",\\"name\\":\\"BGM\\"},
{\\"HWPN\\":\\"8895036217  A\\",\\"SWPN\\":\\"6110110065 NA\\",\\"ecuId\\":\\"1011\\",\\"name\\":\\"TCAM\\"},
{\\"HWPN\\":\\"8895037351  C\\",\\"SWPN\\":\\"6130110100 AA\\",\\"ecuId\\:\\"3011"\\,\\"name\\":\\"CDC\\"},
{\\"HWPN\\":\\"8895036224  A\\",\\"SWPN\\":\\"6130210100 AB,1130210100 AB,1230210100 AB,1330210100 AB,1430210100 AB,1530210100 AB,1630210100 AB,2030210100 AB\\",\\"ecuId\\":\\"3021\\",\\"name\\":\\"AUD\\"},
{\\"HWPN\\":\\"8895037286  B\\",\\"SWPN\\":\\"6130310100 AF\\",\\"ecuId\\":\\"3031\\",\\"name\\":\\"CD\\"}]]
,\\"taskId\\":'''

VERSION_DEBUG_BACK_PRO = '''},\\"type\\":40}'''

VERSION_DEBUG_1 = '''{\\"data\\":{\\"baseLineVer\\":\\"6100000055 BL\\",\\"ecu\\":[
{\\"HWPN\\":\\"'''

VERSION_DEBUG_2 = '''\\",\\"SWPN\\":\\"6160110065 NA,2960110065 AA\\",\\"ecuId\\":\\"6011\\",\\"name\\":\\"BGM\\"}
,{\\"HWPN\\":\\"'''

VERSION_DEBUG_2_CDC = '''\\",\\"SWPN\\":\\"\\",\\"ecuId\\":\\"3011\\",\\"name\\":\\"CDC\\"}]
,\\"taskId\\":'''

VERSION_DEBUG_3 = '''\\",\\"SWPN\\":\\"6110110065 NA\\",\\"ecuId\\":\\"1011\\",\\"name\\":\\"TCAM\\"}]
,\\"taskId\\":'''

VERSION_DEBUG_4 = '''\\",\\"SWPN\\":\\"6160110065 NA,2960110065 AA\\",\\"ecuId\\":\\"6011\\",\\"name\\":\\"BGM\\"}]
,\\"taskId\\":'''

VERSION_DEBUG_BACK ='''},\\"type\\":40}'''

UA_SKIP_need_skip_download = "need_skip_download"

UA_SKIP_allow_same_version_flash = '''\\"allow_same_version_flash\\"'''

SKIP_DEBUG_MUST_USED_IN_TWO_DOMAIN_FRONT = '''[\n\\"acu_ua\\",\n\\"fota_mode_requeset_cdc\\",\n\\"fota_mode_requeset_acu\\",\n\\"fota_mode_requeset_ecm3\\",\n\\"baseline:6100000055 BL\\",\n\\"upload_version_from_debug_file\\",\n\\"ecm3_down_hv\\",\n\\"before_group_1081\\",\n\\"before_group_hv_ctl\\"'''

SKIP_DEBUG_MUST_USED_IN_TWO_DOMAIN_BACK = '''\n]'''
#    "time_check",
#    "wait_hmi",
#    "start_download",
#    "update_precondition_check",
# [
#    "acu_ua",
#    "cdc_ua",
#    "fota_mode_requeset_cdc",
#    "version_collect",
#    "fota_mode_requeset_acu",
#    "fota_mode_requeset_ecm3",
#    "baseline:6100000055 BL",
#    "upload_version_from_debug_file",
#    "ecm3_down_hv",
#    "before_group_1081",
#    "before_group_hv_ctl"
# ]

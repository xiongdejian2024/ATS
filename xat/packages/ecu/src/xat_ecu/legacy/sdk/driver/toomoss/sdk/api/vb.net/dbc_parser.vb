Imports System.Runtime.InteropServices
Module dbc_parser

    Public Const DBC_PARSER_OK As Int32 = 0
    Public Const DBC_PARSER_FILE_OPEN As Int32 = -1
    Public Const DBC_PARSER_FILE_FORMAT As Int32 = -2
    Public Const DBC_PARSER_DEV_DISCONNECT As Int32 = -3
    Public Const DBC_PARSER_HANDLE_ERROR As Int32 = -4
    Public Const DBC_PARSER_GET_INFO_ERROR As Int32 = -5
    Public Const DBC_PARSER_DATA_ERROR As Int32 = -6
    Public Const DBC_PARSER_SLAVE_NACK As Int32 = -7

    Declare Function DBC_ParserFile Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal pDBCFileName As String) As UInt64
    Declare Function DBC_GetMsgQuantity Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64) As Int32
    Declare Function DBC_GetMsgName Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal index As Int32, ByVal pMsgName As String) As Int32
    Declare Function DBC_GetMsgSignalQuantity Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String) As Int32
    Declare Function DBC_GetMsgSignalName Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByVal index As Int32, ByVal pSignalName As String) As Int32
    Declare Function DBC_GetMsgPublisher Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByVal pPublisher As String) As Int32
    '设置信号值
    Declare Function DBC_SetSignalValue Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByVal pSignalName As String, ByVal Value As double) As Int32
    '获取信号值
    Declare Function DBC_GetSignalValue Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByVal pSignalName As String, ByRef pValue As double) As Int32
    Declare Function DBC_GetSignalValueStr Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByVal pSignalName As String, ByVal pValueStr As String) As Int32
    '将CAN消息数据填充到信号里面
    Declare Function DBC_SyncCANMsgToValue Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByRef pCANMsg As CAN_MSG,ByVal MsgLen As Int32) As Int32
    Declare Function DBC_SyncCANFDMsgToValue Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByRef pCANFDMsg As CANFD_MSG, ByVal MsgLen As Int32) As Int32
    '将信号数据填充到CAN消息里面
    Declare Function DBC_SyncValueToCANMsg Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByRef pCANMsg As CAN_MSG) As Int32
    Declare Function DBC_SyncValueToCANFDMsg Lib "USB2XXX.dll" (ByVal DBCHandle As UInt64, ByVal pMsgName As String, ByRef pCANFDMsg As CANFD_MSG) As Int32

End Module

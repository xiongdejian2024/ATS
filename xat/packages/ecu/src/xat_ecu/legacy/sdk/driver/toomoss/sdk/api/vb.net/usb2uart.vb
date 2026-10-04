Imports System.Runtime.InteropServices
Module usb2uart
    '定义初始化UART初始化数据类型
    Public Structure UART_CONFIG
        Dim BaudRate As UInt32 '波特率
        Dim WordLength As Byte '数据位宽，0-8bit,1-9bit
        Dim StopBits As Byte   '停止位宽，0-1bit,1-0.5bit,2-2bit,3-1.5bit
        Dim Parity As Byte     '奇偶校验，0-No,4-Even,6-Odd
        Dim TEPolarity As Byte 'TE输出控制，0x80-输出TE信号，且低电平有效，0x81-输出TE信号，且高电平有效，0x00不输出TE信号
    End Structure
    '定义函数返回错误代码
    Public Const UART_SUCCESS           = (0)   '函数执行成功
    Public Const UART_ERR_NOT_SUPPORT   = (-1)  '适配器不支持该函数
    Public Const UART_ERR_USB_WRITE_FAIL= (-2)  'USB写数据失败
    Public Const UART_ERR_USB_READ_FAIL = (-3)  'USB读数据失败
    Public Const UART_ERR_CMD_FAIL      = (-4)  '命令执行失败
    '数据位宽
    Public Const UART_WORD_LENGTH_8BIT   = 0
    Public Const UART_WORD_LENGTH_9BIT   = 1
    '停止位
    Public Const UART_STOP_BITS_1        = 0'1bit
    Public Const UART_STOP_BITS_05       = 1'0.5bit
    Public Const UART_STOP_BITS_2        = 2'2bit
    Public Const UART_STOP_BITS_15       = 3'1.5bit
    '奇偶校验位
    Public Const UART_PARITY_NO          = 0
    Public Const UART_PARITY_EVEN        = 4
    Public Const UART_PARITY_ODD         = 6
    'TE控制信号输出
    Public Const UART_TE_DISEN           = &H00
    Public Const UART_TE_EN_LOW          = &H80
    Public Const UART_TE_EN_HIGH         = &H81
    '使能内部上拉电阻，CAN&LIN适配器支持
    Public Const UART_PPR_DISABLE        = &H40
    Public Const UART_PPR_ENABLE         = &H41

    Declare Function UART_Init Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal Channel As Byte, <[In]()> ByVal pConfig As UART_CONFIG());
    Declare Function UART_WriteBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal Channel As Byte,<[In]()> ByVal pWriteData As Byte(),ByVal DataSize As UInt32);
    Declare Function UART_WriteBytesAsync Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal Channel As Byte,<[In]()> ByVal pWriteData As Byte(),ByVal DataSize As UInt32);
    Declare Function UART_WriteBytesInterval Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal Channel As Byte,<[In]()> ByVal pWriteData As Byte(),ByVal DataSize As UInt32,ByVal IntervalTimeMs As Byte);
    Declare Function UART_ReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal Channel As Byte,<[Out]()> ByVal pReadData As Byte(),ByVal TimeOutMs As UInt32);
    Declare Function UART_ClearData Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal Channel As Byte);

End Module

Module USB2XXXCANFDTest
    '开始测试之前，请将CAN1_H接CAN2_H，CAN1_L接CAN2_L
    '若提示找不到USB2XXX.dll文件，请将工程中的USB2XXX.dll和libusb-1.0.dll文件复制到exe文件输出目录下
    Sub Main()
        Dim ret As Int32
        Dim State As Boolean
        Dim DeviceHandle(20) As UInt32

        ret = USB_ScanDevice(DeviceHandle)
        If ret <= 0 Then
            Console.WriteLine("No Device Connected")
        End If

        State = USB_OpenDevice(DeviceHandle(0))
        If State Then
            Console.WriteLine("Open Device Success!")
        End If
        '初始化配置CAN
        Dim CANFDConfig As CANFD_INIT_CONFIG
        CANFDConfig.Mode = 0        '0-正常模式，1-自发自收模式,若需要正常发送数据到CAN总线，需要设置为正常模式
        CANFDConfig.RetrySend = 1   '使能自动重传
        CANFDConfig.ISOCRCEnable = 1 '使能ISOCRC
        CANFDConfig.ResEnable = 1   '使能内部终端电阻（若总线上没有终端电阻，则必须使能终端电阻才能正常传输数据）
        '波特率参数可以用TCANLINPro软件里面的波特率计算工具计算
        '仲裁段波特率参数,波特率=40M/NBT_BRP*(1+NBT_SEG1+NBT_SEG2)
        CANFDConfig.NBT_BRP = 1
        CANFDConfig.NBT_SEG1 = 59
        CANFDConfig.NBT_SEG2 = 20
        CANFDConfig.NBT_SJW = 2
        '数据域波特率参数,波特率=40M/DBT_BRP*(1+DBT_SEG1+DBT_SEG2)
        CANFDConfig.DBT_BRP = 1
        CANFDConfig.DBT_SEG1 = 14
        CANFDConfig.DBT_SEG2 = 5
        CANFDConfig.DBT_SJW = 2
        ret = CANFD_Init(DeviceHandle(0), 0, CANFDConfig)
        If ret <> CANFD_SUCCESS Then
            Console.WriteLine("Init CAN1 Faild!")
        Else
            Console.WriteLine("Init CAN1 Success!")
        End If
        ret = CANFD_Init(DeviceHandle(0), 1, CANFDConfig)
        If ret <> CANFD_SUCCESS Then
            Console.WriteLine("Init CAN2 Faild!")
        Else
            Console.WriteLine("Init CAN2 Success!")
        End If
        '发送普通CAN数据帧
        Dim CanMsg(5) As CANFD_MSG
        Dim i As Long
        For i = 0 To 4
            CanMsg(i).ID = i
            CanMsg(i).DLC = 8
            CanMsg(i).Flags = 0
            Dim j As Long
            ReDim CanMsg(i).Data(63)
            For j = 0 To 7
                CanMsg(i).Data(j) = j
            Next j
        Next i

        Dim SendedNum As Long
        SendedNum = CANFD_SendMsg(DeviceHandle(0), 0, CanMsg, 5)
        If SendedNum >= 0 Then
            Console.WriteLine("CAN1 Success Send Frames:" + CStr(SendedNum))
        Else
            Console.WriteLine("CAN1 Send can msg error!")
        End If

        Threading.Thread.Sleep(10)

        Dim CanMsgBuffer(10240) As CANFD_MSG
        Dim GetCanNum As Long
        GetCanNum = CANFD_GetMsg(DeviceHandle(0), 1, CanMsgBuffer, CanMsgBuffer.Length)
        Console.WriteLine("CAN2 Get frames:" + CStr(GetCanNum))
        For i = 0 To (GetCanNum - 1)
            Console.WriteLine("")
            Console.WriteLine("CanMsg[" + CStr(i) + "].Flags = " + CanMsgBuffer(i).Flags.ToString("X"))
            Console.WriteLine("CanMsg[" + CStr(i) + "].ID = " + CStr(CanMsgBuffer(i).ID))
            Console.WriteLine("CanMsg[" + CStr(i) + "].TimeStamp = " + CStr(CanMsgBuffer(i).TimeStamp))
            Console.Write("CanMsg[" + CStr(i) + "].Data = ")
            For j = 0 To (CanMsgBuffer(i).DLC - 1)
                Console.Write(CStr(CanMsgBuffer(i).Data(j)) + " ")
            Next j
            Console.WriteLine("")
        Next i
        '发送CANFD数据帧
        For i = 0 To 4
            CanMsg(i).ID = i
            CanMsg(i).DLC = 16
            CanMsg(i).Flags = CANFD_MSG_FLAG_FDF
            Dim j As Long
            ReDim CanMsg(i).Data(63)
            For j = 0 To 15
                CanMsg(i).Data(j) = j
            Next j
        Next i
        SendedNum = CANFD_SendMsg(DeviceHandle(0), 0, CanMsg, 5)
        If SendedNum >= 0 Then
            Console.WriteLine("CAN1 Success Send Frames:" + CStr(SendedNum))
        Else
            Console.WriteLine("CAN1 Send can msg error!")
        End If
        Threading.Thread.Sleep(10)
        GetCanNum = CANFD_GetMsg(DeviceHandle(0), 1, CanMsgBuffer, CanMsgBuffer.Length)
        Console.WriteLine("CAN2 Get frames:" + CStr(GetCanNum))
        For i = 0 To (GetCanNum - 1)
            Console.WriteLine("")
            Console.WriteLine("CanMsg[" + CStr(i) + "].Flags = " + CanMsgBuffer(i).Flags.ToString("X"))
            Console.WriteLine("CanMsg[" + CStr(i) + "].ID = " + CStr(CanMsgBuffer(i).ID))
            Console.WriteLine("CanMsg[" + CStr(i) + "].TimeStamp = " + CStr(CanMsgBuffer(i).TimeStamp))
            Console.Write("CanMsg[" + CStr(i) + "].Data = ")
            For j = 0 To (CanMsgBuffer(i).DLC - 1)
                Console.Write(CStr(CanMsgBuffer(i).Data(j)) + " ")
            Next j
            Console.WriteLine("")
        Next i
        '发送CANFD加速数据帧
        For i = 0 To 4
            CanMsg(i).ID = i
            CanMsg(i).DLC = 32
            CanMsg(i).Flags = CANFD_MSG_FLAG_FDF Or CANFD_MSG_FLAG_BRS
            Dim j As Long
            ReDim CanMsg(i).Data(63)
            For j = 0 To 31
                CanMsg(i).Data(j) = j
            Next j
        Next i
        SendedNum = CANFD_SendMsg(DeviceHandle(0), 0, CanMsg, 5)
        If SendedNum >= 0 Then
            Console.WriteLine("CAN1 Success Send Frames:" + CStr(SendedNum))
        Else
            Console.WriteLine("CAN1 Send can msg error!")
        End If
        Threading.Thread.Sleep(10)
        GetCanNum = CANFD_GetMsg(DeviceHandle(0), 1, CanMsgBuffer, CanMsgBuffer.Length)
        Console.WriteLine("CAN2 Get frames:" + CStr(GetCanNum))
        For i = 0 To (GetCanNum - 1)
            Console.WriteLine("")
            Console.WriteLine("CanMsg[" + CStr(i) + "].Flags = " + CanMsgBuffer(i).Flags.ToString("X"))
            Console.WriteLine("CanMsg[" + CStr(i) + "].ID = " + CStr(CanMsgBuffer(i).ID))
            Console.WriteLine("CanMsg[" + CStr(i) + "].TimeStamp = " + CStr(CanMsgBuffer(i).TimeStamp))
            Console.Write("CanMsg[" + CStr(i) + "].Data = ")
            For j = 0 To (CanMsgBuffer(i).DLC - 1)
                Console.Write(CStr(CanMsgBuffer(i).Data(j)) + " ")
            Next j
            Console.WriteLine("")
        Next i
    End Sub

End Module

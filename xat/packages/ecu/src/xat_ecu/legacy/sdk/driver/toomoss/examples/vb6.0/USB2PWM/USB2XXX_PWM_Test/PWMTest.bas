Attribute VB_Name = "LINEXTest"
Public Declare Function AllocConsole Lib "kernel32.dll" () As Long
Public Declare Function FreeConsole Lib "kernel32.dll" () As Long
Public Declare Function SetConsoleTitle Lib "kernel32.dll" Alias "SetConsoleTitleA" (ByVal lpConsoleTitle As String) As Long
Public Declare Sub Sleep Lib "kernel32.dll" (ByVal dwMilliseconds As Long)

Private Declare Function GetStdHandle Lib "kernel32.dll" (ByVal nStdHandle As Long) As Long

Private Declare Function WriteConsole Lib "kernel32.dll" Alias "WriteConsoleA" _
                                                (ByVal hConsoleOutput As Long, _
                                                 lpBuffer As Any, _
                                                 ByVal nNumberOfCharsToWrite As Long, _
                                                 lpNumberOfCharsWritten As Long, _
                                                 lpReserved As Any) As Long
                                                 
Private Declare Function ReadConsole Lib "kernel32.dll" Alias "ReadConsoleA" _
                                                (ByVal hConsoleInput As Long, _
                                                lpBuffer As Any, _
                                                ByVal nNumberOfCharsToRead As Long, _
                                                lpNumberOfCharsRead As Long, _
                                                lpReserved As Any) As Long
                                                
Private Declare Function SetConsoleMode Lib "kernel32" (ByVal hConsoleHandle As Long, ByVal dwMode As Long) As Long

Private Const INPUT_HANDLE = -10&
Private Const OUTPUT_HANDLE = -11&
Private Const ERROR_HANDLE = -12&

Private Const LINE_INPUT = &H2
Private Const ECHO_INPUT = &H4
Private Const MOUSE_INPUT = &H10
Private Const PROCESSED = &H1

Public Function Printf(ByVal hConsoleOutput As Long, ByVal str As String) As Long
    Call WriteConsole(hConsoleOutput, ByVal str, Len(str), vbNull, vbNull)
End Function

Sub Main()
    Call AllocConsole
    Call SetConsoleTitle("PWM Test")
    
    Dim inputHandle As Long
    Dim str As String
    Dim outputHandle As Long
    Dim ret As Long
    Dim State As Boolean
    Dim DeviceHandle(20) As Long
    outputHandle = GetStdHandle(OUTPUT_HANDLE)
    
    ret = USB_ScanDevice(VarPtr(DeviceHandle(0)))
    If ret <= 0 Then
        str = "No device connected" + vbNewLine
        Call WriteConsole(outputHandle, ByVal str, Len(str), vbNull, vbNull)
        End
    End If
    
    State = USB_OpenDevice(DeviceHandle(0))
    If State Then
        str = "Open device success!" + vbNewLine
        Call WriteConsole(outputHandle, ByVal str, Len(str), vbNull, vbNull)
    End If
    'Init PWM,
    Dim PWMConfig As PWM_CONFIG
    PWMConfig.ChannelMask = &H40 'LIN1 Output PWM
    PWMConfig.Prescaler(6) = 84
    PWMConfig.Precision(6) = 1000
    PWMConfig.Pulse(6) = 500
    PWMConfig.Phase(6) = 0
    PWMConfig.Polarity(6) = 1
    ret = PWM_Init(DeviceHandle(0), PWMConfig)
    If ret <> PWM_SUCCESS Then
        str = "Config PWM faild!" + vbNewLine
        Call WriteConsole(outputHandle, ByVal str, Len(str), vbNull, vbNull)
    Else
        str = "Config PWM success!" + vbNewLine
        Call WriteConsole(outputHandle, ByVal str, Len(str), vbNull, vbNull)
    End If
    'Output PWM
    ret = PWM_Start(DeviceHandle(0), PWMConfig.ChannelMask, 0)
    If ret <> PWM_SUCCESS Then
        str = "Output PWM faild!" + vbNewLine
        Call WriteConsole(outputHandle, ByVal str, Len(str), vbNull, vbNull)
    Else
        str = "Output PWM success!" + vbNewLine
        Call WriteConsole(outputHandle, ByVal str, Len(str), vbNull, vbNull)
    End If
    
    inputHandle = GetStdHandle(INPUT_HANDLE)
    Call ReadConsole(inputHandle, vbNull, 255, vbNull, vbNull)
    Call FreeConsole
End Sub


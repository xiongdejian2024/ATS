from enum import IntEnum


class Doip:
    SERVER_PORT = 13400


class Can:
    # block_size = 8
    # st = 20
    block_size = 0
    st = 0


class ValidService(IntEnum):
    """As described in ISO 14229-1:2013 Table 23"""

    DiagnosticSessionControl = 0x10
    ECUReset = 0x11
    SecurityAccess = 0x27
    CommunicationControl = 0x28
    TesterPresent = 0x3E
    AccessTimingParameter = 0x83
    SecuredDataTransmission = 0x84
    ControlDTCSetting = 0x85
    ResponseOnEvent = 0x86
    LinkControl = 0x87
    ReadDataByIdentifier = 0x22
    ReadMemoryByAddress = 0x23
    ReadScalingDataByIdentifier = 0x24
    ReadDataByPeriodicIdentifier = 0x2A
    DynamicallyDefineDataIdentifier = 0x2C
    WriteDataByIdentifier = 0x2E
    WriteMemoryByAddress = 0x3D
    ClearDiagnosticInformation = 0x14
    ReadDTCInformation = 0x19
    InputOutputControlByIdentifier = 0x2F
    RoutineControl = 0x31
    RequestDownload = 0x34
    RequestUpload = 0x35
    TransferData = 0x36
    RequestTransferExit = 0x37
    RequestFileTransfer = 0x38

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class ValidResponse(IntEnum):
    NegativeResponse = 0x7F
    DiagnosticSessionControlResp = 0x50
    ECUResetResp = 0x51
    SecurityAccessResp = 0x67
    CommunicationControlResp = 0x68
    TesterPresentResp = 0x7E
    AccessTimingParameterResp = 0xC3
    SecuredDataTransmissionResp = 0xC4
    ControlDTCSettingResp = 0xC5
    ResponseOnEventResp = 0xC6
    LinkControlResp = 0xC7
    ReadDataByIdentifierResp = 0x62
    ReadMemoryByAddressResp = 0x63
    ReadScalingDataByIdentifierResp = 0x64
    ReadDataByPeriodicIdentifierResp = 0x6A
    DynamicallyDefineDataIdentifierResp = 0x6C
    WriteDataByIdentifierResp = 0x6E
    WriteMemoryByAddressResp = 0x7D
    ClearDiagnosticInformationResp = 0x54
    ReadDTCInformationResp = 0x59
    InputOutputControlByIdentifierResp = 0x6F
    RoutineControlResp = 0x71
    RequestDownloadResp = 0x74
    RequestUploadResp = 0x75
    TransferDataResp = 0x76
    RequestTransferExitResp = 0x77
    RequestFileTransferResp = 0x78

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class NegativeResponseCode(IntEnum):
    """As described in ISO 14229-1:2013 Annex A"""

    generalReject = 0x10
    serviceNotSupported = 0x11
    subFunctionNotSupported = 0x12
    incorrectMessageLengthOrInvalidFormat = 0x13
    responseTooLong = 0x14
    busyRepeatRequest = 0x21
    conditionsNotCorrect = 0x22
    requestSequenceError = 0x24
    noResponseFromSubnetComponent = 0x25
    failurePreventsExecutionOfRequestedAction = 0x26
    requestOutOfRange = 0x31
    securityAccessDenied = 0x33
    invalidKey = 0x35
    exceedNumberOfAttempts = 0x36
    requiredTimeDelayNotExpired = 0x37
    uploadDownloadNotAccepted = 0x70
    transferDataSuspended = 0x71
    generalProgrammingFailure = 0x72
    wrongBlockSequenceCounter = 0x73
    requestCorrectlyReceivedResponsePending = 0x78
    subFunctionNotSupportedInActiveSession = 0x7E
    serviceNotSupportedInActiveSession = 0x7F
    # additional codes used in conjunction with conditionsNotCorrect (0x22)
    rpmTooHigh = 0x81
    rpmTooLow = 0x82
    engineIsRunning = 0x83
    engineIsNotRunning = 0x84
    engineRunTimeTooLow = 0x85
    temperatureTooHigh = 0x86
    temperatureTooLow = 0x87
    vehicleSpeedTooHigh = 0x88
    vehicleSpeedTooLow = 0x89
    throttlePedalTooHigh = 0x8A
    throttlePedalTooLow = 0x8B
    transmissionRangeNotInNeutral = 0x8C
    transmissionRangeNotInGear = 0x8D
    brakeSwitchesNotClosed = 0x8F
    shiftLeverNotInPark = 0x90
    torqueConverterClutchLocked = 0x91
    voltageTooHigh = 0x92
    voltageTooLow = 0x93

    @classmethod
    def return_key(cls, value):
        for item in cls:
            if value == item.value:
                return item.__dict__.get("_name_")

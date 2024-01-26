from ctypes import c_int, POINTER, CDLL
from msp_types import *
from msp_constants import *

rtl2 = CDLL("./drtl3.dll")

''' 
Анализ состояния обработки кадра производится при помощи функций msp_GetMessageStatus(), 
msp_RetrieveMessage(), msp_GetCurrentEntry(), msp_ReadStackWord() (см. модуль config, п. 6.8.4). 
Вместо msp_RetrieveMessage() можно использовать msp_BCRetrieveMessage().
'''


def error_check(result, func, args):
    error = ERROR_CODES.get(result, None)
    if error:
        raise RuntimeError(error, func.__name__, args)
    return result

def get_last_error(result, func, args):
    err = msp_GetLastError()
    if err != 0:
        error_check(err, func, args)
    return result

msp_GetLastError = rtl2.msp_GetLastError
msp_GetLastError.restype = msp_ERROR

msp_Startup = rtl2.msp_Startup
msp_Startup.restype = msp_ERROR
msp_Startup.errcheck = error_check

msp_Cleanup = rtl2.msp_Cleanup
msp_Cleanup.restype = msp_ERROR
msp_Cleanup.errcheck = error_check

msp_Open = rtl2.msp_Open
msp_Open.argtypes = [c_int]
msp_Open.restype = msp_DEVHANDLE
msp_Open.errcheck = error_check

msp_Close = rtl2.msp_Close
msp_Close.argtypes = [msp_DEVHANDLE]
msp_Close.restype = msp_ERROR
msp_Close.errcheck = error_check

msp_OpenEx = rtl2.msp_OpenEx
msp_OpenEx.argtypes = [c_int, c_int]
msp_OpenEx.restype = msp_DEVHANDLE
msp_OpenEx.errcheck = error_check

msp_SelectMode = rtl2.msp_SelectMode
msp_SelectMode.argtypes = [msp_DEVHANDLE, msp_MODE]
msp_SelectMode.restype = msp_ERROR
msp_SelectMode.errcheck = error_check

msp_Configure = rtl2.msp_Configure
msp_Configure.argtypes = [
    msp_DEVHANDLE, msp_MODE, POINTER(msp_FLAGID), POINTER(msp_REGVALUE)
]
msp_Configure.restype = msp_ERROR
msp_Configure.errcheck = error_check

msp_GetFlag = rtl2.msp_GetFlag
msp_GetFlag.argtypes = [msp_DEVHANDLE, msp_FLAGID]
msp_GetFlag.restype = msp_BIT
msp_GetFlag.errcheck = get_last_error

msp_SetFlag = rtl2.msp_SetFlag
msp_SetFlag.argtypes = [msp_DEVHANDLE, msp_FLAGID, msp_BIT]
msp_SetFlag.restype = msp_ERROR
msp_SetFlag.errcheck = error_check

msp_SetFlagsIndirect = rtl2.msp_SetFlagsIndirect
msp_SetFlagsIndirect.argtypes = [msp_DEVHANDLE, POINTER(msp_FLAGID), msp_BIT]
msp_SetFlagsIndirect.restype = msp_ERROR
msp_SetFlagsIndirect.errcheck = error_check


msp_ReadReg = rtl2.msp_ReadReg
msp_ReadReg.argtypes = [msp_DEVHANDLE, msp_REGID]
msp_ReadReg.restype = msp_WORD
msp_ReadReg.errcheck = get_last_error

msp_WriteReg = rtl2.msp_WriteReg
msp_WriteReg.argtypes = [msp_DEVHANDLE, msp_REGID, msp_WORD]
msp_WriteReg.restype = msp_ERROR
msp_WriteReg.errcheck = error_check

msp_ReadRamW = rtl2.msp_ReadRamW
msp_ReadRamW.argtypes = [msp_DEVHANDLE, msp_WORD]
msp_ReadRamW.restype = msp_WORD
msp_ReadRamW.errcheck = get_last_error

msp_ReadRamDW = rtl2.msp_ReadRamDW
msp_ReadRamDW.argtypes = [msp_DEVHANDLE, msp_WORD]
msp_ReadRamDW.restype = msp_DWORD
msp_ReadRamDW.errcheck = get_last_error

msp_ReadRam = msp_ReadRamW

msp_WriteRamW = rtl2.msp_WriteRamW
msp_WriteRamW.argtypes = [msp_DEVHANDLE, msp_WORD, msp_WORD]
msp_WriteRamW.restype = msp_ERROR
msp_WriteRamW.errcheck = error_check

msp_WriteRamDW = rtl2.msp_WriteRamDW
msp_WriteRamDW.argtypes = [msp_DEVHANDLE, msp_WORD, msp_DWORD]
msp_WriteRamDW.restype = msp_ERROR
msp_WriteRamDW.errcheck = error_check

msp_WriteRam = msp_WriteRamW

msp_CreateFrame = rtl2.msp_CreateFrame
msp_CreateFrame.argtypes = [msp_DEVHANDLE, msp_WORD, msp_WORD]
msp_CreateFrame.restype = msp_FRMHANDLE
msp_CreateFrame.errcheck = get_last_error

msp_DestroyHandle = rtl2.msp_DestroyHandle
msp_DestroyHandle.argtypes = [msp_HANDLE]
msp_DestroyHandle.restype = msp_ERROR
msp_DestroyHandle.errcheck = error_check

msp_DestroyFrame = msp_DestroyHandle


msp_AddMessage = rtl2.msp_AddMessage
msp_AddMessage.argtypes = [msp_FRMHANDLE, msp_MSGHANDLE, msp_WORD]
msp_AddMessage.restype = msp_ERROR
msp_AddMessage.errcheck = error_check

msp_AddMessages = rtl2.msp_AddMessages
msp_AddMessages.argtypes = [
    msp_FRMHANDLE, POINTER(msp_MSGHANDLE), POINTER(msp_WORD)
]
msp_AddMessages.restype = msp_ERROR
msp_AddMessages.errcheck = error_check

msp_AddMessagesIndirect = rtl2.msp_AddMessagesIndirect
msp_AddMessagesIndirect.argtypes = [
    msp_FRMHANDLE, POINTER(POINTER(msp_MSGHANDLE)), POINTER(msp_WORD)
]
msp_AddMessagesIndirect.restype = msp_ERROR
msp_AddMessagesIndirect.errcheck = error_check

msp_AddMessagesIndirect2 = rtl2.msp_AddMessagesIndirect2
msp_AddMessagesIndirect2.argtypes = [
    msp_FRMHANDLE, POINTER(msp_WORD), POINTER(msp_MSGHANDLE), POINTER(msp_WORD)
]
msp_AddMessagesIndirect2.restype = msp_ERROR
msp_AddMessagesIndirect2.errcheck = error_check

msp_VerifyFrameTime = rtl2.msp_VerifyFrameTime
msp_VerifyFrameTime.argtypes = [msp_FRMHANDLE, msp_BIT]
msp_VerifyFrameTime.restype = msp_BIT
msp_VerifyFrameTime.errcheck = get_last_error

msp_GetFrameMessage = rtl2.msp_GetFrameMessage
msp_GetFrameMessage.argtypes = [msp_FRMHANDLE, c_int]
msp_GetFrameMessage.restype = msp_MSGHANDLE
msp_GetFrameMessage.errcheck = get_last_error

msp_ReplaceFrameMessage = rtl2.msp_ReplaceFrameMessage
msp_ReplaceFrameMessage.argtypes = [msp_FRMHANDLE, c_int, msp_MSGHANDLE]
msp_ReplaceFrameMessage.restype = msp_FRMHANDLE
msp_ReplaceFrameMessage.errcheck = get_last_error

msp_GetFrameProp = rtl2.msp_GetFrameProp
msp_GetFrameProp.argtypes = [msp_FRMHANDLE, msp_BYTE]
msp_GetFrameProp.restype = msp_WORD
msp_GetFrameProp.errcheck = get_last_error

msp_SetFrameProp = rtl2.msp_SetFrameProp
msp_SetFrameProp.argtypes = [msp_FRMHANDLE, msp_BYTE, msp_WORD]
msp_SetFrameProp.restype = msp_ERROR
msp_SetFrameProp.errcheck = error_check

msp_LoadFrame = rtl2.msp_LoadFrame
msp_LoadFrame.argtypes = [msp_FRMHANDLE, c_int]
msp_LoadFrame.restype = msp_ERROR
msp_LoadFrame.errcheck = error_check

msp_ResetFrame = rtl2.msp_ResetFrame
msp_ResetFrame.argtypes = [msp_FRMHANDLE]
msp_ResetFrame.restype = msp_ERROR
msp_ResetFrame.errcheck = error_check

msp_BCRetrieveMessage = rtl2.msp_BCRetrieveMessage


msp_FormatMessage = rtl2.msp_FormatMessage
msp_FormatMessage.argtypes = [
    POINTER(msp_Message), msp_BYTE, msp_BYTE, msp_BYTE, msp_BYTE,
    msp_WORD, msp_BYTE, POINTER(msp_WORD), msp_DWORD
]
msp_FormatMessage.restype = POINTER(msp_Message)
msp_FormatMessage.errcheck = get_last_error


def mspi_mcsa(cw):
    return 31 if cw & 0x20000 else 0


def msp_BCtoRT(B, RT, SA, wcnt, data, cw):
    res = msp_FormatMessage(c.byref(B), mspM_BCtoRT, RT, SA, 0, 0, wcnt, data, cw)
    return res


def msp_RTtoBC(B, RT, SA, wcnt, cw):
    return msp_FormatMessage(c.byref(B), mspM_RTtoBC, RT, SA, 0, 0, wcnt, None, cw)


def msp_RTtoRT(B, RT, SA, RTR, SAR, wcnt, cw):
    return msp_FormatMessage(B, mspM_RTtoRT, RT, SA, RTR, SAR, wcnt, None, cw)


def msp_BCtoRT_bcst(B, SA, wcnt, data, cw):
    return msp_FormatMessage(B, mspM_BCtoRT_BROADCAST, 0, SA, 0, 0, wcnt, data, cw)


def msp_RTtoRT_bcst(B, RT, SA, SAR, wcnt, cw):
    return msp_FormatMessage(B, mspM_RTtoRT_BROADCAST, RT, SA, 0, SAR, wcnt, None, cw)


def msp_Modecode(B, RT, MC, cw):
    return msp_FormatMessage(B, mspM_MODECODE, RT, mspi_mcsa(cw), MC, 0, 0, None, cw)


def msp_Modecode_data_tx(B, RT, MC, cw):
    return msp_FormatMessage(B, mspM_MODECODE_DATA_TX, RT, mspi_mcsa(cw), MC, 0, 0, None, cw)


def msp_Modecode_data_rx(B, RT, MC, MCD, cw):
    return msp_FormatMessage(B, mspM_MODECODE_DATA_RX, RT, mspi_mcsa(cw), MC, MCD, 0, None, cw)


def msp_Modecode_bcst(B, MC, cw):
    return msp_FormatMessage(B, mspM_MODECODE_BROADCAST, 0, mspi_mcsa(cw), MC, 0, 0, None, cw)


def msp_Modecode_data_bcst(B, MC, MCD, cw):
    return msp_FormatMessage(B, mspM_MODECODE_DATA_BROADCAST, 0,  mspi_mcsa(cw), MC, MCD, 0, None, cw)


msp_CreateMessage = rtl2.msp_CreateMessage
msp_CreateMessage.argtypes = [msp_DEVHANDLE, POINTER(msp_Message)]
msp_CreateMessage.restype = msp_MSGHANDLE
msp_CreateMessage.errcheck = get_last_error

msp_DestroyMessage = msp_DestroyHandle

msp_ReadBCMessage = rtl2.msp_ReadBCMessage
msp_ReadBCMessage.argtypes = [msp_MSGHANDLE, POINTER(msp_Message)]
msp_ReadBCMessage.restype = msp_ERROR
msp_ReadBCMessage.errcheck = error_check

msp_ReadMessageData = rtl2.msp_ReadMessageData
msp_ReadMessageData.argtypes = [msp_MSGHANDLE, POINTER(msp_Message), msp_BYTE]
msp_ReadMessageData.restype = msp_BYTE
msp_ReadMessageData.errcheck = get_last_error

msp_WriteMessageData = rtl2.msp_WriteMessageData
msp_WriteMessageData.argtypes = [msp_MSGHANDLE, POINTER(msp_Message), msp_BYTE]
msp_WriteMessageData.restype = msp_BYTE
msp_WriteMessageData.errcheck = get_last_error

msp_ReadMessageWord = rtl2.msp_ReadMessageWord
msp_ReadMessageWord.argtypes = [msp_MSGHANDLE, msp_BYTE]
msp_ReadMessageWord.restype = msp_WORD
msp_ReadMessageWord.errcheck = get_last_error

msp_WriteMessageWord = rtl2.msp_WriteMessageWord
msp_WriteMessageWord.argtypes = [msp_MSGHANDLE, msp_BYTE, msp_WORD]
msp_WriteMessageWord.restype = msp_ERROR
msp_WriteMessageWord.errcheck = error_check

msp_GetMessageStatus = rtl2.msp_GetMessageStatus
msp_GetMessageStatus.argtypes = [msp_STKHANDLE, c_int]
msp_GetMessageStatus.restype = msp_MESSAGE_STATUS
msp_ReadMessageWord.errcheck = get_last_error

msp_RetrieveMessage = rtl2.msp_RetrieveMessage
msp_RetrieveMessage.argtypes = [msp_STKHANDLE, c_int, POINTER(msp_Message)]
msp_RetrieveMessage.restype = msp_ERROR
msp_RetrieveMessage.errcheck = error_check

msp_GetCurrentEntry = rtl2.msp_GetCurrentEntry
msp_GetCurrentEntry.argtypes = [msp_STKHANDLE, c_int]
msp_GetCurrentEntry.restype = msp_WORD
msp_GetCurrentEntry.errcheck = get_last_error

msp_Command = rtl2.msp_Command
msp_Command.argtypes = [msp_DEVHANDLE, msp_WORD]
msp_Command.restype = msp_ERROR
msp_Command.errcheck = error_check

def msp_Start(device):
    return msp_Command(device, mspC_START)

def msp_Reset(device):
    return msp_Command(device, mspC_RESET)

def msp_ResetInterrupt(device): 
    return msp_Command(device, mspC_INTERRUPT_RESET)

def msp_ResetTimeTag(device): 
    return msp_Command(device, mspC_TIME_TAG_RESET)

def msp_TimeTagTestClock(device): 
    return msp_Command(device, mspC_TIME_TAG_TEST_CLOCK)

def msp_StopOnFrame(device):
    return msp_Command(device, mspC_STOP_ON_FRAME)

def msp_StopOnMessage(device):
    return msp_Command(device, mspC_STOP_ON_MESSAGE)

msp_RamTotal = rtl2.msp_RamTotal
msp_RamTotal.argtypes = [msp_DEVHANDLE]
msp_RamTotal.restype = msp_DWORD
msp_RamTotal.errcheck = error_check

msp_RamFree = rtl2.msp_RamFree
msp_RamFree.argtypes = [msp_DEVHANDLE]
msp_RamFree.restype = msp_DWORD
msp_RamFree.errcheck = error_check

msp_ResetStack = rtl2.msp_ResetStack
msp_ResetStack.argtypes = [msp_STKHANDLE, c_int]
msp_ResetStack.restype = msp_ERROR
msp_ResetStack.errcheck = error_check

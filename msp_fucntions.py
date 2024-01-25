from ctypes import c_int, POINTER, CDLL
from msp_types import *
from msp_constants import *

rtl2 = CDLL("./drtl3.dll")

msp_Startup = rtl2.msp_Startup
msp_Startup.restype = msp_ERROR

msp_Open = rtl2.msp_Open
msp_Open.argtypes = [c_int]
msp_Open.restype = msp_DEVHANDLE

msp_Configure = rtl2.msp_Configure
msp_Configure.argtypes = [
    msp_DEVHANDLE, msp_MODE,POINTER(msp_FLAGID), POINTER(msp_REGVALUE)
]
msp_Configure.restype = msp_ERROR

msp_GetFlag = rtl2.msp_GetFlag
msp_GetFlag.argtypes = [msp_DEVHANDLE, msp_FLAGID]
msp_GetFlag.restype = msp_BIT

msp_SetFlag = rtl2.msp_SetFlag
msp_SetFlag.argtypes = [msp_DEVHANDLE, msp_FLAGID, msp_BIT]
msp_SetFlag.restype = msp_ERROR

msp_SetFlagsIndirect = rtl2.msp_SetFlagsIndirect
msp_SetFlagsIndirect.argtypes = [msp_DEVHANDLE, POINTER(msp_FLAGID), msp_BIT]

msp_ReadReg = rtl2.msp_ReadReg
msp_ReadReg.argtypes = [msp_DEVHANDLE, msp_REGID]
msp_ReadReg.restype = msp_WORD

msp_WriteReg = rtl2.msp_WriteReg
msp_WriteReg.argtypes = [msp_DEVHANDLE, msp_REGID, msp_WORD]
msp_WriteReg.restype = msp_ERROR

msp_ReadRamW = rtl2.msp_ReadRamW
msp_ReadRamW.argtypes = [msp_DEVHANDLE, msp_WORD]
msp_ReadRamW.restype = msp_WORD

msp_ReadRamDW = rtl2.msp_ReadRamDW
msp_ReadRamDW.argtypes = [msp_DEVHANDLE, msp_WORD]
msp_ReadRamDW.restype = msp_DWORD

msp_ReadRam = msp_ReadRamW

msp_WriteRamW = rtl2.msp_WriteRamW
msp_WriteRamW.argtypes = [msp_DEVHANDLE, msp_WORD, msp_WORD]
msp_WriteRamW.restype = msp_ERROR

msp_WriteRamDW = rtl2.msp_WriteRamDW
msp_WriteRamDW.argtypes = [msp_DEVHANDLE, msp_WORD, msp_DWORD]
msp_WriteRamDW.restype = msp_ERROR

msp_WriteRam = msp_WriteRamW

msp_CreateFrame = rtl2.msp_CreateFrame
msp_CreateFrame.argtypes = [msp_DEVHANDLE, msp_WORD, msp_WORD]
msp_CreateFrame.restype = msp_FRMHANDLE

msp_DestroyHandle = rtl2.msp_DestroyHandle
msp_DestroyHandle.argtypes = [msp_HANDLE]
msp_DestroyHandle.restype = msp_ERROR

msp_DestroyFrame = msp_DestroyHandle


msp_AddMessage = rtl2.msp_AddMessage
msp_AddMessage.argtypes = [msp_FRMHANDLE, msp_MSGHANDLE, msp_WORD]
msp_AddMessage.restype = msp_ERROR

msp_AddMessages = rtl2.msp_AddMessages
msp_AddMessages.argtypes = [
    msp_FRMHANDLE, POINTER(msp_MSGHANDLE), POINTER(msp_WORD)
]
msp_AddMessages.restype = msp_ERROR

msp_AddMessagesIndirect = rtl2.msp_AddMessagesIndirect
msp_AddMessagesIndirect.argtypes = [
    msp_FRMHANDLE, POINTER(POINTER(msp_MSGHANDLE)), POINTER(msp_WORD)
]
msp_AddMessagesIndirect.restype = msp_ERROR

msp_AddMessagesIndirect2 = rtl2.msp_AddMessagesIndirect2
msp_AddMessagesIndirect2.argtypes = [
    msp_FRMHANDLE, POINTER(msp_WORD), POINTER(msp_MSGHANDLE), POINTER(msp_WORD)
]
msp_AddMessagesIndirect2.restype = msp_ERROR

msp_VerifyFrameTime = rtl2.msp_VerifyFrameTime
msp_VerifyFrameTime.argtypes = [msp_FRMHANDLE, msp_BIT]
msp_VerifyFrameTime.restype = msp_BIT

msp_GetFrameMessage = rtl2.msp_GetFrameMessage
msp_GetFrameMessage.argtypes = [msp_FRMHANDLE, c_int]
msp_GetFrameMessage.restype = msp_MSGHANDLE

msp_ReplaceFrameMessage = rtl2.msp_ReplaceFrameMessage
msp_ReplaceFrameMessage.argtypes = [msp_FRMHANDLE, c_int, msp_MSGHANDLE]
msp_ReplaceFrameMessage.restype = msp_FRMHANDLE

msp_GetFrameProp = rtl2.msp_GetFrameProp
msp_GetFrameProp.argtypes = [msp_FRMHANDLE, msp_BYTE]
msp_GetFrameProp.restype = msp_WORD

msp_SetFrameProp = rtl2.msp_SetFrameProp
msp_SetFrameProp.argtypes = [msp_FRMHANDLE, msp_BYTE, msp_WORD]
msp_SetFrameProp.restype = msp_ERROR

msp_LoadFrame = rtl2.msp_LoadFrame
msp_LoadFrame.argtypes = [msp_FRMHANDLE, c_int]
msp_LoadFrame.restype = msp_ERROR

msp_ResetFrame = rtl2.msp_ResetFrame
msp_ResetFrame.argtypes = [msp_FRMHANDLE]
msp_ResetFrame.restype = msp_ERROR

msp_BCRetrieveMessage = rtl2.msp_BCRetrieveMessage


msp_FormatMessage = rtl2.msp_FormatMessage
msp_FormatMessage.argtypes = [
    POINTER(msp_Message), msp_BYTE, msp_BYTE, msp_BYTE, msp_BYTE, 
    msp_WORD, msp_BYTE, POINTER(msp_WORD), msp_DWORD
]
msp_FormatMessage.restype = POINTER(msp_Message)

def mspi_mcsa(cw):
    return 31 if cw & 0x20000 else 0

def msp_BCtoRT(B, RT, SA, wcnt, data, cw):
     return msp_FormatMessage(c.POINTER(B), mspM_BCtoRT, RT, SA, 0, 0, wcnt, c.POINTER(data), cw)
 
def msp_RTtoBC(B, RT, SA, wcnt, cw):
    return msp_FormatMessage(B, mspM_RTtoBC, RT, SA, 0, 0, wcnt, None, cw)

def msp_RTtoRT(B, RT, SA, RTR, SAR, wcnt, cw):
    return msp_FormatMessage(B, mspM_RTtoRT, RT, SA, RTR, SAR, wcnt, None, cw)

def msp_BCtoRT_bcst(B, SA, wcnt, data, cw):
    return msp_FormatMessage(B, mspM_BCtoRT_BROADCAST, 0, SA, 0, 0, wcnt, data, cw)

def msp_RTtoRT_bcst(B, RT, SA, SAR, wcnt, cw):
    return msp_FormatMessage(B, mspM_RTtoRT_BROADCAST, RT, SA, 0, SAR, wcnt, None, cw)

def msp_Modecode(B, RT, MC, cw):
    return msp_FormatMessage(B, mspM_MODECODE, RT, mspi_mcsa(cw),MC, 0, 0, None, cw) 

def msp_Modecode_data_tx(B, RT, MC, cw):
    return msp_FormatMessage(B, mspM_MODECODE_DATA_TX, RT, mspi_mcsa(cw),MC, 0, 0, None, cw)

def msp_Modecode_data_rx(B, RT, MC, MCD, cw):
    return msp_FormatMessage(B, mspM_MODECODE_DATA_RX, RT, mspi_mcsa(cw), MC, MCD, 0, None, cw)

def msp_Modecode_bcst(B, MC, cw):
    return msp_FormatMessage(B, mspM_MODECODE_BROADCAST, 0, mspi_mcsa(cw), MC, 0, 0, None, cw)

def msp_Modecode_data_bcst(B, MC, MCD, cw):
    return msp_FormatMessage(B, mspM_MODECODE_DATA_BROADCAST, 0,  mspi_mcsa(cw),MC, MCD, 0, None, cw)

msp_CreateMessage = rtl2.msp_CreateMessage
msp_CreateMessage.argtypes = [msp_DEVHANDLE, POINTER(msp_Message)]
msp_CreateMessage.restype = msp_MSGHANDLE

msp_DestroyMessage = msp_DestroyHandle

msp_ReadBCMessage = rtl2.msp_ReadBCMessage
msp_ReadBCMessage.argtypes = [msp_MSGHANDLE, POINTER(msp_Message)]
msp_ReadBCMessage.restype = msp_ERROR

msp_ReadMessageData = rtl2.msp_ReadMessageData
msp_ReadMessageData.argtypes = [msp_MSGHANDLE, POINTER(msp_Message), msp_BYTE]
msp_ReadMessageData.restype = msp_BYTE

msp_WriteMessageData = rtl2.msp_WriteMessageData
msp_WriteMessageData.argtypes = [msp_MSGHANDLE, POINTER(msp_Message), msp_BYTE]
msp_WriteMessageData.restype = msp_BYTE

msp_ReadMessageWord = rtl2.msp_ReadMessageWord
msp_ReadMessageWord.argtypes = [msp_MSGHANDLE, msp_BYTE]
msp_ReadMessageWord.restype = msp_WORD

msp_WriteMessageWord = rtl2.msp_WriteMessageWord
msp_WriteMessageWord.argtypes = [msp_MSGHANDLE, msp_BYTE, msp_WORD]
msp_WriteMessageWord.restype = msp_ERROR

msp_GetMessageStatus = rtl2.msp_GetMessageStatus
msp_GetMessageStatus.argtypes = [msp_STKHANDLE, c_int]
msp_GetMessageStatus.restype = msp_MESSAGE_STATUS

msp_Start = rtl2.msp_Start

msp_RetrieveMessage = rtl2.msp_RetrieveMessage
msp_RetrieveMessage.argtypes = [msp_STKHANDLE, c_int, POINTER(msp_Message)]
msp_RetrieveMessage.restype = msp_ERROR




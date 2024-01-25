from ctypes import c_int, POINTER, CDLL
from msp_types import *

rtl2 = CDLL("./drtl3.dll")

msp_Startup = rtl2.msp_Startup
msp_Startup.restype = msp_ERROR

msp_Open = rtl2.msp_Open
msp_Open.argtypes = [c_int]
msp_Open.restype = msp_DEVHANDLE

msp_Configure = rtl2.msp_Configure
msp_Configure.argtypes = [msp_DEVHANDLE, msp_MODE,
                          POINTER(msp_FLAGID), POINTER(msp_REGVALUE)]
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

# msp_DestroyFrame = rtl2.msp_DestroyFrame
# msp_DestroyFrame.argtypes = [msp_FRMHANDLE]
# msp_DestroyFrame.restype = msp_ERROR

msp_AddMessage = rtl2.msp_AddMessage
msp_AddMessage.argtypes = [msp_FRMHANDLE, msp_MSGHANDLE, msp_WORD]
msp_AddMessage.restype = msp_ERROR

msp_AddMessages = rtl2.msp_AddMessages
msp_AddMessages.argtypes = [msp_FRMHANDLE,
                            POINTER(msp_MSGHANDLE), POINTER(msp_WORD)]
msp_AddMessages.restype = msp_ERROR

msp_AddMessagesIndirect = rtl2.msp_AddMessagesIndirect
msp_AddMessagesIndirect.argtypes = [msp_FRMHANDLE, POINTER(
    POINTER(msp_MSGHANDLE)), POINTER(msp_WORD)]
msp_AddMessagesIndirect.restype = msp_ERROR

msp_AddMessagesIndirect2 = rtl2.msp_AddMessagesIndirect2
msp_AddMessagesIndirect2.argtypes = [msp_FRMHANDLE, POINTER(
    msp_WORD), POINTER(msp_MSGHANDLE), POINTER(msp_WORD)]
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

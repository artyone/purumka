from ctypes import c_int, POINTER, CDLL, c_short, c_wchar_p, Structure
from msp_types import *
from msp_constants import *
from msp_flags import *


class RTL:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lib = CDLL(f'{filepath}')

    @staticmethod
    def getError(result, func, args):
        error = ERROR_CODES.get(result, None)
        if error:
            raise RuntimeError(error, func.__name__, args)
        return result

    def lastErrorHandler(self, result, func, args):
        err = self.getLastError()
        if err != 0:
            self.getError(err, func, args)
        return result

    def getLastError(self) -> msp_ERROR:
        func = self.lib.msp_GetLastError
        func.restype = msp_ERROR
        return func()

    def getNumberOfDevices(self) -> int:
        return int(self.lib.msp_GetNumberOfDevices())

    def startUp(self) -> msp_ERROR:
        func = self.lib.msp_Startup
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func()

    def cleanup(self) -> msp_ERROR:
        func = self.lib.msp_Cleanup
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func()

    def open(self, dev_num: int) -> msp_DEVHANDLE:
        func = self.lib.msp_Open
        func.argtypes = [c_int]
        func.restype = msp_DEVHANDLE
        func.errcheck = self.lastErrorHandler
        return func(dev_num)

    def close(self, dev_handle: msp_DEVHANDLE) -> msp_ERROR:
        func = self.lib.msp_Close
        func.argtypes = [msp_DEVHANDLE]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle)

    def openEx(self, dev_num: int, flags: int):
        # flags msp_of64 | msp_ofBackDoor
        func = self.lib.msp_OpenEx
        func.argtypes = [c_int, c_int]
        func.restype = msp_DEVHANDLE
        func.errcheck = self.lastErrorHandler
        return func(dev_num, flags)

    def selectMode(self, dev_handle: msp_DEVHANDLE, mode: msp_MODE) -> msp_ERROR:
        # msp_MODE msp_MODE_XXXX & msp_SWITCH_XXXX
        func = self.lib.msp_SelectMode
        func.argtypes = [msp_DEVHANDLE, c_int]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, mode)

    def configure(self, dev_handle: msp_DEVHANDLE, mode: int, flags: list, vregval: list | None) -> msp_ERROR:
        c_flags = (msp_FLAGID * (len(flags) + 1))(*flags, 0) if flags else None
        c_vregval = (msp_REGVALUE * (len(vregval) + 1)
                     )(*vregval, 0) if vregval else None
        func = self.lib.msp_Configure
        func.argtypes = [
            msp_DEVHANDLE, msp_MODE, POINTER(msp_FLAGID), POINTER(msp_REGVALUE)
        ]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, mode, c_flags, c_vregval)

    def getFlag(self, dev_handle: msp_DEVHANDLE, flag: msp_FLAGID) -> msp_BIT:
        func = self.lib.msp_GetFlag
        func.argtypes = [msp_DEVHANDLE, msp_FLAGID]
        func.restype = msp_BIT
        func.errcheck = self.lastErrorHandler
        return func(dev_handle, flag)

    def setFlag(self, dev_handle: msp_DEVHANDLE, flag: msp_FLAGID, value: msp_BIT) -> msp_ERROR:
        func = self.lib.msp_SetFlag
        func.argtypes = [msp_DEVHANDLE, msp_FLAGID, msp_BIT]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, flag, value)

    def setFlagsIndirect(self, dev_handle: msp_DEVHANDLE, flags: list, value: msp_BIT) -> msp_ERROR:
        c_flags = (msp_FLAGID * (len(flags) + 1))(*flags, 0)
        func = self.lib.msp_SetFlagsIndirect
        func.argtypes = [msp_DEVHANDLE, POINTER(msp_FLAGID), msp_BIT]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, c_flags, value)

    def readReg(self, dev_handle: msp_DEVHANDLE, reg: msp_REGID) -> msp_WORD:
        func = self.lib.msp_ReadReg
        func.argtypes = [msp_DEVHANDLE, msp_REGID]
        func.restype = msp_WORD
        func.errcheck = self.lastErrorHandler
        return func(dev_handle, reg)

    def writeReg(self, dev_handle: msp_DEVHANDLE, reg: int, value: int) -> msp_ERROR:
        func = self.lib.msp_WriteReg
        func.argtypes = [msp_DEVHANDLE, msp_REGID, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, reg, value)

    def setVRegsIndirect(self, dev_handle: msp_DEVHANDLE, vreg: list, value: msp_WORD) -> msp_ERROR:
        c_vreg = (msp_REGID * (len(vreg) + 1))(*vreg, 0)
        func = self.lib.msp_SetVRegsIndirect
        func.argtypes = [msp_DEVHANDLE, POINTER(msp_REGID), msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, c_vreg, value)

    def readRamW(self, dev_handle: msp_DEVHANDLE, address: msp_WORD) -> msp_WORD:
        func = self.lib.msp_ReadRamW
        func.argtypes = [msp_DEVHANDLE, msp_WORD]
        func.restype = msp_WORD
        func.errcheck = self.lastErrorHandler
        return func(dev_handle, address)

    def readRamDW(self, dev_handle: msp_DEVHANDLE, address: msp_WORD) -> msp_DWORD:
        func = self.lib.msp_ReadRamDW
        func.argtypes = [msp_DEVHANDLE, msp_WORD]
        func.restype = msp_DWORD
        func.errcheck = self.lastErrorHandler
        return func(dev_handle, address)

    def readRam(self, dev_handle: msp_DEVHANDLE, address: msp_WORD) -> msp_WORD:
        return self.readRamW(dev_handle, address)

    def writeRamW(self, dev_handle: msp_DEVHANDLE, address: int, value: int) -> msp_ERROR:
        func = self.lib.msp_WriteRamW
        func.argtypes = [msp_DEVHANDLE, msp_WORD, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, address, value)

    def writeRamDW(self, dev_handle: msp_DEVHANDLE, address: int, value: int) -> msp_ERROR:
        func = self.lib.msp_WriteRamDW
        func.argtypes = [msp_DEVHANDLE, msp_WORD, msp_DWORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, address, value)

    def writeRam(self, dev_handle: msp_DEVHANDLE, address: int, value: int) -> msp_ERROR:
        return self.writeRamW(dev_handle, address, value)

    def createFrame(self, dev_handle: msp_DEVHANDLE, frame_time: int, message_count: int) -> msp_FRMHANDLE:
        func = self.lib.msp_CreateFrame
        func.argtypes = [msp_DEVHANDLE, msp_WORD, msp_WORD]
        func.restype = msp_FRMHANDLE
        func.errcheck = self.lastErrorHandler
        return func(dev_handle, frame_time, message_count)

    def destroyHandle(self, handle: msp_HANDLE) -> msp_ERROR:
        func = self.lib.msp_DestroyHandle
        func.argtypes = [msp_HANDLE]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(handle)

    def destroyFrame(self, frame_handle: msp_FRMHANDLE) -> msp_ERROR:
        return self.destroyHandle(frame_handle)

    def addMessage(self, frame_handle: msp_FRMHANDLE, message: msp_MSGHANDLE, msggap: int) -> msp_ERROR:
        func = self.lib.msp_AddMessage
        func.argtypes = [msp_FRMHANDLE, msp_RAMHANDLE, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(frame_handle, message, msggap)

    def addMessages(self, frame_handle: msp_FRMHANDLE, messages: list, msggaps: list | None) -> msp_ERROR:
        c_messages = (msp_MSGHANDLE * (len(messages) + 1)
                      )(*messages, msp_NOHANDLE)
        c_msggaps = (msp_WORD * (len(msggaps) + 1)
                     )(*msggaps) if msggaps else None
        func = self.lib.msp_AddMessages
        func.argtypes = [msp_FRMHANDLE, POINTER(
            msp_MSGHANDLE), POINTER(msp_WORD)]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(frame_handle, c_messages, c_msggaps)

    def addMessagesIndirect(self, frame_handle: msp_FRMHANDLE, messages: list[list], msggaps: list | None) -> msp_ERROR:
        c_messages = [(msp_MSGHANDLE * (len(message) + 1))(*message, msp_NOHANDLE) for message in messages]
        c_messages = ((msp_MSGHANDLE * (len(messages) + 1))(*c_messages, msp_NOHANDLE))
        c_msggaps = (msp_WORD * (len(msggaps) + 1))(*msggaps) if msggaps else None
        func = self.lib.msp_AddMessages
        func.argtypes = [msp_FRMHANDLE, POINTER(
            msp_MSGHANDLE), POINTER(msp_WORD)]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(frame_handle, c_messages, c_msggaps)
    
    def verifyFrameTime(self, frame_handle: msp_FRMHANDLE, ajust: msp_BIT) -> msp_BIT:
        func = self.lib.msp_VerifyFrameTime
        func.argtypes = [msp_FRMHANDLE, msp_BIT]
        func.restype = msp_BIT
        func.errcheck = self.lastErrorHandler
        return func(frame_handle, ajust)
    
    def getFrameMessage(self, frame_handle: msp_FRMHANDLE, entry: msp_WORD) -> msp_MSGHANDLE:
        func = self.lib.msp_GetFrameMessage
        func.argtypes = [msp_FRMHANDLE, msp_WORD]
        func.restype = msp_MSGHANDLE
        func.errcheck = self.lastErrorHandler
        return func(frame_handle, entry)
    
    def replaceFrameMessage(self, frame_handle: msp_FRMHANDLE, entry: msp_WORD, message: msp_MSGHANDLE) -> msp_ERROR:
        func = self.lib.msp_ReplaceFrameMessage
        func.argtypes = [msp_FRMHANDLE, msp_WORD, msp_MSGHANDLE]
        func.restype = msp_FRMHANDLE
        func.errcheck = self.lastErrorHandler
        return func(frame_handle, entry, message)
    
    def getFrameProp(self, frame_handle: msp_FRMHANDLE, property: msp_BYTE) -> msp_WORD:
        func = self.lib.msp_GetFrameProp
        func.argtypes = [msp_FRMHANDLE, msp_BYTE]
        func.restype = msp_WORD
        func.errcheck = self.lastErrorHandler
        return func(frame_handle, property)
    
    def setFrameProp(self, frame_handle: msp_FRMHANDLE, property: msp_BYTE, value: msp_WORD) -> msp_ERROR:
        func = self.lib.msp_SetFrameProp
        func.argtypes = [msp_FRMHANDLE, msp_BYTE, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(frame_handle, property, value)
    
    def loadFrame(self, frame_handle: msp_FRMHANDLE, flags: int) -> msp_ERROR:
        func = self.lib.msp_LoadFrame
        func.argtypes = [msp_FRMHANDLE, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(frame_handle, flags)
    
    def resetFrame(self, frame_handle: msp_FRMHANDLE) -> msp_ERROR:
        func = self.lib.msp_ResetFrame
        func.argtypes = [msp_FRMHANDLE]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(frame_handle)
    
    def BCRetrieveMessage(self, *args):
        return self.lib.BCRetrieveMessage(*args)
    
    def formatMessage(self, message, type, RT, SA, RTR_MS, SAR_MCD, dataWordCount, data, bccw) -> msp_Message:
        func = self.lib.msp_FormatMessage
        func.argtypes = [
            POINTER(msp_Message), msp_BYTE, msp_BYTE, msp_BYTE, msp_BYTE,
            msp_WORD, msp_BYTE, POINTER(msp_WORD), msp_DWORD
        ]
        func.restype = POINTER(msp_Message)
        func.errcheck = self.lastErrorHandler
        return func(message, type, RT, SA, RTR_MS, SAR_MCD, dataWordCount, data, bccw)
    
    def mspi_mcsa(self, cw):
        return 31 if cw & 0x20000 else 0


    def BCtoRT(self, B, RT, SA, wcnt, data, cw) -> msp_Message:
        c_data = (msp_WORD * wcnt)(*data)
        res = self.formatMessage(c.byref(B), mspM_BCtoRT, RT, SA, 0, 0, wcnt, c_data, cw)
        return res


    def RTtoBC(self, B, RT, SA, wcnt, cw) -> msp_Message:
        return self.formatMessage(c.byref(B), mspM_RTtoBC, RT, SA, 0, 0, wcnt, None, cw)


    def RTtoRT(self, B, RT, SA, RTR, SAR, wcnt, cw) -> msp_Message:
        return self.formatMessage(B, mspM_RTtoRT, RT, SA, RTR, SAR, wcnt, None, cw)


    def BCtoRT_bcst(self, B, SA, wcnt, data, cw) -> msp_Message:
        return self.formatMessage(B, mspM_BCtoRT_BROADCAST, 0, SA, 0, 0, wcnt, data, cw)


    def RTtoRT_bcst(self, B, RT, SA, SAR, wcnt, cw) -> msp_Message:
        return self.formatMessage(B, mspM_RTtoRT_BROADCAST, RT, SA, 0, SAR, wcnt, None, cw)


    def Modecode(self, B, RT, MC, cw) -> msp_Message:
        return self.formatMessage(B, mspM_MODECODE, RT, self.mspi_mcsa(cw), MC, 0, 0, None, cw)


    def Modecode_data_tx(self, B, RT, MC, cw) -> msp_Message:
        return self.formatMessage(B, mspM_MODECODE_DATA_TX, RT, self.mspi_mcsa(cw), MC, 0, 0, None, cw)


    def Modecode_data_rx(self, B, RT, MC, MCD, cw) -> msp_Message:
        return self.formatMessage(B, mspM_MODECODE_DATA_RX, RT, self.mspi_mcsa(cw), MC, MCD, 0, None, cw)


    def Modecode_bcst(self, B, MC, cw) -> msp_Message:
        return self.formatMessage(B, mspM_MODECODE_BROADCAST, 0, self.mspi_mcsa(cw), MC, 0, 0, None, cw)


    def Modecode_data_bcst(self, B, MC, MCD, cw) -> msp_Message:
        return self.formatMessage(B, mspM_MODECODE_DATA_BROADCAST, 0,  self.mspi_mcsa(cw), MC, MCD, 0, None, cw)

    def createMessage(self, dev_handle: msp_DEVHANDLE, message: msp_Message) -> msp_MSGHANDLE:
        func = self.lib.msp_CreateMessage
        func.argtypes = [msp_DEVHANDLE, POINTER(msp_Message)]
        func.restype = msp_MSGHANDLE
        func.errcheck = self.lastErrorHandler
        return func(dev_handle, message)
    
    def destroyMessage(self, msg_handle: msp_MSGHANDLE) -> msp_ERROR:
        return self.destroyHandle(msg_handle)
    
    def readBCMessage(self, msg_handle: msp_MSGHANDLE, message: msp_Message) -> msp_ERROR:
        func = self.lib.msp_ReadBCMessage
        func.argtypes = [msp_MSGHANDLE, POINTER(msp_Message)]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(msg_handle, message)
    
    def readMessageData(self, msg_handle: msp_MSGHANDLE, message: msp_Message, word_count: msp_BYTE) -> msp_BYTE:
        func = self.lib.msp_ReadMessageData
        func.argtypes = [msp_MSGHANDLE, POINTER(msp_Message), msp_BYTE]
        func.restype = msp_BYTE
        func.errcheck = self.lastErrorHandler
        return func(msg_handle, message, word_count)
    
    def writeMessageData(self, msg_handle: msp_MSGHANDLE, message: msp_Message, word_count: msp_BYTE) -> msp_BYTE:
        func = self.lib.msp_WriteMessageData
        func.argtypes = [msp_MSGHANDLE, POINTER(msp_Message), msp_BYTE]
        func.restype = msp_BYTE
        func.errcheck = self.lastErrorHandler
        return func(msg_handle, message, word_count)
    
    def readMessageWord(self, msg_handle: msp_MSGHANDLE, word: msp_BYTE) -> msp_WORD:
        func = self.lib.msp_ReadMessageWord
        func.argtypes = [msp_MSGHANDLE, msp_BYTE]
        func.restype = msp_WORD
        func.errcheck = self.lastErrorHandler
        return func(msg_handle, word)
    
    def writeMessageWord(self, msg_handle: msp_MSGHANDLE, word: msp_BYTE, value: msp_WORD) -> msp_ERROR:
        func = self.lib.msp_WriteMessageWord
        func.argtypes = [msp_MSGHANDLE, msp_BYTE, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(msg_handle, word, value)
    
    def getMessageStatus(self, stack: msp_STKHANDLE, entry: int) -> msp_MESSAGE_STATUS:
        func = self.lib.msp_GetMessageStatus
        func.argtypes = [msp_STKHANDLE, c_int]
        func.restype = msp_MESSAGE_STATUS
        func.errcheck = self.lastErrorHandler
        return func(stack, entry)
    
    def retrieveMessage(self, stack: msp_STKHANDLE, entry: int, message: msp_Message) -> msp_ERROR:
        func = self.lib.msp_RetrieveMessage
        func.argtypes = [msp_STKHANDLE, c_int, POINTER(msp_Message)]
        func.restype = msp_ERROR
        # func.errcheck = self.getError
        return func(stack, entry, message)
    
    def getCurrentEntry(self, stack: msp_STKHANDLE, option: int) -> c_int:
        func = self.lib.msp_GetCurrentEntry
        func.argtypes = [msp_STKHANDLE]
        func.restype = c_int
        func.errcheck = self.lastErrorHandler
        return func(stack)
    
    def command(self, dev_handle: msp_DEVHANDLE, command: int) -> msp_ERROR:
        func = self.lib.msp_Command
        func.argtypes = [msp_DEVHANDLE, msp_WORD]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_handle, command)
    
    def start(self, dev_handle: msp_DEVHANDLE):
        return self.command(dev_handle, mspC_START)

    def reset(self, dev_handle: msp_DEVHANDLE):
        return self.command(dev_handle, mspC_RESET)

    def resetInterrupt(self, dev_handle: msp_DEVHANDLE): 
        return self.command(dev_handle, mspC_INTERRUPT_RESET)

    def resetTimeTag(self, dev_handle: msp_DEVHANDLE): 
        return self.command(dev_handle, mspC_TIME_TAG_RESET)

    def timeTagTestClock(self, dev_handle: msp_DEVHANDLE): 
        return self.command(dev_handle, mspC_TIME_TAG_TEST_CLOCK)

    def stopOnFrame(self, dev_handle: msp_DEVHANDLE):
        return self.command(dev_handle, mspC_STOP_ON_FRAME)

    def stopOnMessage(self, dev_handle: msp_DEVHANDLE):
        return self.command(dev_handle, mspC_STOP_ON_MESSAGE)
    
    def ramTotal(self, dev_handle: msp_DEVHANDLE) -> msp_DWORD:
        func = self.lib.msp_RamTotal
        func.argtypes = [msp_DEVHANDLE]
        func.restype = msp_DWORD
        func.errcheck = self.lastErrorHandler
        return func(dev_handle)
    
    def ramFree(self, dev_handle: msp_DEVHANDLE) -> msp_DWORD:
        func = self.lib.msp_RamFree
        func.argtypes = [msp_DEVHANDLE]
        func.restype = msp_DWORD
        func.errcheck = self.lastErrorHandler
        return func(dev_handle)
    
    def resetStack(self, stack: msp_STKHANDLE, msgindex: int):
        func = self.lib.msp_ResetStack
        func.argtypes = [msp_STKHANDLE, c_int]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(stack, msgindex)
    
    def getDeviceInfo(self, dev_num: int, dev_info: msp_DeviceInfo):
        func = self.lib.msp_GetDeviceInfo
        func.argtypes = [c_int, POINTER(msp_DeviceInfo)]
        func.restype = msp_ERROR
        func.errcheck = self.getError
        return func(dev_num, dev_info)


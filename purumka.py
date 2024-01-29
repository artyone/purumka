import ctypes
from msp_constants import *
from msp_types import *
from msp_fucntions import *
from msp_flags import *
from icecream import ic
from time import sleep
import numpy as np


class ClassWrapper:
    def __init__(self, device_info: msp_DeviceInfo):
        self.fields = [name[0]
                       for name in getattr(type(device_info), '_fields_')]
        for field in self.fields:
            setattr(self, field, getattr(device_info, field))

    def __str__(self):
        res = [f'{field}: {getattr(self, field)}' for field in self.fields]
        return ' '.join(res)


msgctr = 0
val = 25
buf = (msp_WORD * 32)(*([25] * 32))


msp_Startup()
ic(msp_GetNumberOfDevices())


bc = msp_Open(0)
if not bc:
    print("Failed open bc")


# raw_device_info = msp_DeviceInfo()
# result = rtl2.msp_GetDeviceInfo(0, ctypes.byref(raw_device_info))

# device_info = ClassWrapper(raw_device_info)
# ic(f"Device Information - {device_info}")

bcflags = (msp_FLAGID * 6)(
    mspF_ENHANCED_MODE,
    mspF_256WORD_BOUNDARY_DISABLE,
    mspF_MESSAGE_GAP_TIMER_ENABLED,
    mspF_INTERNAL_TRIGGER_ENABLED,
    mspF_EXPANDED_BC_CONTROL_WORD,
    0
)

msp_Configure(bc, msp_MODE_BC + msp_MODE_ENHANCED, bcflags, None)


fr = msp_CreateFrame(bc, 1000, 2)
if not fr:
    print("Failed create frame")

message_one = msp_Message()


msp_AddMessage(fr,
               msp_CreateMessage(bc,
                                 msp_RTtoBC(message_one, 4, 1, 2, msp_BCCW_CHANNEL_A)),
               1000)


msp_LoadFrame(fr, msp_AUTOREPEAT)

msp_Start(bc)


E = msp_RetrieveMessage(fr, msp_NEXT_MESSAGE, message_one)

print(*message_one.Data)
ic(f'0x{message_one.type:04x}')
ic(f'0x{message_one.dataWordCount:04x}')
ic(f'0x{message_one.bccw:04x}')
ic(f'0x{message_one.CmdWord1:04x}')
ic(f'0x{message_one.CmdWord2:04x}')
ic(f'0x{message_one.StatusWord1:04x}')
ic(f'0x{message_one.StatusWord2:04x}')
ic(f'0x{message_one.loopback:04x}')
ic(f'0x{message_one.bsw:04x}')
ic(f'0x{message_one.timetag:04x}')

# reg = msp_ReadReg(dev_handle, mspRR_CONFIG3)
# ic(f'0b{reg:016b}')
msp_Reset(bc)
msp_Close(bc)
msp_Cleanup(bc)

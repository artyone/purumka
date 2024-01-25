import ctypes
from msp_constants import *
from msp_types import *
from msp_fucntions import *
from msp_flags import *
from icecream import ic


# Подгрузим библиотеку RTL2 (предполагается, что она доступна в системе)
rtl2 = ctypes.CDLL("./drtl3.dll")


class ClassWrapper:
    def __init__(self, device_info: msp_DeviceInfo):
        self.fields = [name[0]
                       for name in getattr(type(device_info), '_fields_')]
        for field in self.fields:
            setattr(self, field, getattr(device_info, field))

    def __str__(self):
        res = [f'{field}: {getattr(self, field)}' for field in self.fields]
        return ' '.join(res)


def open_rtl2_device(device_index):
    """
    Открывает устройство RTL2.

    :param device_index: Индекс устройства
    :return: Дескриптор устройства
    """
    msp_Startup()
    dev_handle = msp_Open(device_index)

    if not dev_handle:
        raise RuntimeError("Ошибка открытия устройства")
    return dev_handle


def close_rtl2_device(dev_handle):
    """
    Закрывает устройство RTL2.

    :param dev_handle: Дескриптор устройства
    """
    res = rtl2.msp_Close(dev_handle)
    if res == 0:
        return
    if res == msp_ERROR_INVALID_DEVICE_HANDLE:
        raise RuntimeError(
            "Недействительный или неинициализированный дескриптор модуля")
    if res == msp_ERROR_INTERNAL_ACCESS_ERROR:
        raise RuntimeError("Внутренняя ошибка")


# Пример использования функций
device_handle = open_rtl2_device(0)
print(device_handle)

raw_device_info = msp_DeviceInfo()
result = rtl2.msp_GetDeviceInfo(0, ctypes.byref(raw_device_info))

device_info = ClassWrapper(raw_device_info)
print(f"Device Information - {device_info}")

bcflags = (msp_FLAGID * 6)(
    mspF_ENHANCED_MODE,
    mspF_256WORD_BOUNDARY_DISABLE,
    mspF_MESSAGE_GAP_TIMER_ENABLED,
    mspF_INTERNAL_TRIGGER_ENABLED,
    mspF_EXPANDED_BC_CONTROL_WORD,
    0
)

msp_Configure(device_handle, msp_MODE_BC + msp_MODE_ENHANCED, bcflags, None)

msp_SetFlagsIndirect(device_handle, bcflags, 0)

enhanced_mode_flag = msp_GetFlag(device_handle, mspF_ENHANCED_MODE)
ic(enhanced_mode_flag)

enhanced_mode_flag = msp_GetFlag(device_handle, mspF_256WORD_BOUNDARY_DISABLE)
ic(enhanced_mode_flag)

enhanced_mode_flag = msp_GetFlag(device_handle, mspF_MESSAGE_GAP_TIMER_ENABLED)
ic(enhanced_mode_flag)

msp_SetFlag(device_handle, mspF_ENHANCED_MODE, 1)


reg = msp_ReadReg(device_handle, 0x07)
ic(bin(reg))

close_rtl2_device(device_handle)

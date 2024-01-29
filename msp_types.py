import ctypes as c

msp_DWORD = c.c_uint32
msp_WORD = c.c_uint16
msp_BYTE = c.c_uint8
msp_BIT = msp_BYTE
msp_SIGNED_DWORD = c.c_int32
msp_SIGNED_WORD = c.c_int16
msp_SIGNED_BYTE = c.c_int8
msp_ERROR = c.c_long

msp_HANDLE = c.c_void_p
msp_NOHANDLE = msp_HANDLE(None)
msp_DEVHANDLE = msp_HANDLE
msp_RAMHANDLE = msp_HANDLE
msp_STKHANDLE = msp_RAMHANDLE
msp_DSTKHANDLE = msp_RAMHANDLE
msp_MODE = msp_DWORD
msp_DIR = msp_BYTE
msp_BOOL = msp_BYTE

class msp_MESSAGE_STATUS(c.c_int):
    _fields_ = [
        ("msp_MESSAGE_WAITING", c.c_int),
        ("msp_MESSAGE_IN_PROGRESS", c.c_int),
        ("msp_MESSAGE_COMPLETED", c.c_int)
    ]


msp_FRMHANDLE = msp_STKHANDLE
msp_MSGHANDLE = msp_RAMHANDLE
msp_BUFHANDLE = msp_HANDLE
msp_SUBADDRESS = msp_BYTE
msp_WG_MSGHANDLE = msp_HANDLE
msp_WG_FRMHANDLE = msp_HANDLE

msp_FALSE = c.c_uint(0)
msp_TRUE = c.c_uint(1)
msp_FIND_FIRST = c.c_uint(0)
msp_FIND_NEXT = c.c_uint(1)

msp_FLAGID = msp_DWORD
msp_REGID = msp_DWORD


class msp_DeviceInfo(c.Structure):
    _fields_ = [
        ("VendorId", c.c_short),
        ("DeviceId", c.c_short),
        ("SubsystemVendorId", c.c_short),
        ("SubsystemId", c.c_short),
        ("InstanceId", c.c_int),
        ("ProcessId", c.c_int),
        ("LType", c.c_int),
        ("BusType", c.c_int),
        ("DriverType", c.c_int),
        ("Busy", c.c_short),
        ("SerialNumber", c.c_wchar_p)
    ]

class msp_REGVALUE(c.Structure):
    _fields_ = [
        ('reg', msp_REGID),
        ('value', msp_WORD)
    ]
    
class msp_Message(c.Structure):
        _fields_ = [
        ("type", msp_WORD),
        ("dataWordCount", msp_WORD),
        ("bccw", msp_WORD),
        ("CmdWord1", msp_WORD),
        ("CmdWord2", msp_WORD),
        ("Data", msp_WORD * 32),
        ("StatusWord1", msp_WORD),
        ("StatusWord2", msp_WORD),
        ("loopback", msp_WORD),
        ("bsw", msp_WORD),
        ("timetag", msp_WORD),
    ]
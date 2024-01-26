msp_NOERROR = 0
msp_ERROR_INVALID_DEVICE_HANDLE = 1
msp_ERROR_INVALID_PARAMETER = 2
msp_ERROR_NOT_INITIALIZED = 3
msp_ERROR_SYSTEM_ERROR = 4
msp_ERROR_DEVICE_BUSY = 5
msp_ERROR_INTERNAL_ACCESS_ERROR = 6
msp_ERROR_NO_HOST_MEMORY = 7
msp_ERROR_ADDRESS_OUT_OF_RAM = 8
msp_IRQ_BUSY = 9
msp_ERROR_IRQ_CANCELLED = 10
msp_ERROR_INTERNAL_INTEGRITY_ERROR  = 11
msp_ERROR_MISSING_DELAY_FUNC = 12
msp_ERROR_UNSUPPORTED_FUNCTION  = 13
msp_ERROR_UNKNOWN_DEVICE_TYPE = 14
msp_ERROR_UNSUPPORTED_DRIVER_TYPE = 15
msp_ERROR_UNSUPPORTED_BUS_TYPE = 16
msp_ERROR_DRIVER_NOT_FOUND = 17
msp_ERROR_NO_FREE_RAM = 20
msp_ERROR_INVALID_RAM_HANDLE = 21
msp_ERROR_ILLEGAL_HANDLE_TYPE = 22
msp_ERROR_HANDLE_OUT_OF_SCOPE = 23
msp_ERROR_HANDLE_IN_USE = 24
msp_ERROR_ADDRESS_OUT_OF_OBJECT  = 25
msp_ERROR_INVALID_FLAG = 30
msp_ERROR_INVALID_VREG = 31
msp_ERROR_UNSUPPORTED_MODE = 32
msp_ERROR_MODE_NOT_SELECTED = 33
msp_ERROR_INCOMPATIBLE_MODE = 34
msp_ERROR_INCOMPATIBLE_CONFIGURATION = 35
msp_ERROR_FRAM_NOT_RESERVED = 36
msp_ERROR_INCOMPATIBLE_STACK = 40
msp_ERROR_INCOMPATIBLE_FRAME = 40
msp_ERROR_NOT_LOADED = 41
msp_ERROR_INDEX_OUT_OF_RANGE = 42
msp_ERROR_NO_NEXT_MESSAGE = 43
msp_ERROR_MESSAGE_IN_PROGRESS = 44
msp_ERROR_INVALID_MESSAGE_FORMAT = 50
msp_ERROR_MESSAGE_FIELD_NOT_EXISTS = 51
msp_ERROR_FRAME_EXCEEDS_SIZE_LIMIT = 52
msp_ERROR_INCOMPATIBLE_BUFFER = 60
msp_ERROR_BUFFER_NOT_CONNECTED = 61
msp_ERROR_BUFFER_BUSY_SAFE = 62
msp_ERROR_BUFFER_BUSY_UNSAFE = 63
msp_ERROR_STREAM_DISABLED = 64
msp_ERROR_STREAM_IN_USED = 65
msp_ERROR_STREAM_CORRUPTED  = 66
msp_ERROR_ILLEGAL_COMMAND_WORD = 67
msp_ERROR_NOT_MODE_CODE = 68
msp_ERROR_TOO_MANY_FRAMES = 70
msp_ERROR_INVALID_MESSAGE_HANDLE = 71
msp_ERROR_INVALID_FRAME_HANDLE = 72
msp_ERROR_ANSWER_NOT_MATCH = 80
msp_ERROR_ANSWER_MISSING_WORDS = 81
msp_ERROR_ANSWER_EXTRA_WORDS  = 82
msp_ERROR_INVALID_MESSAGE  = 83
msp_ERROR_ANSWER_ERROR = 84
msp_ERROR_ANSWER_ANOTHER_CHANNEL = 85
msp_ERROR_ANSWER_RT_BUSY = 86
msp_ERROR_INTERNAL_ALGORITHM  = 90
msp_ERROR_EMPTY_FRAME = 100
msp_ERROR_OVERLOAD_BUFFERS = 101
msp_ERROR_INVALID_REQUEST = 102
msp_ERROR_USB_EXCHANGE = 200
msp_ERROR_USB_NOT_SUPPORT = 201
msp_ERROR_USB_ACCESS = 202
msp_ERROR_USB_FTDI_ERROR = 203
msp_ERROR_USB_RESPONSE_TIMEOUT = 204
msp_ERROR_USB_RESPONSE_FAILURE = 205
msp_ERROR_DEVICES_NOT_FOUND = 210
msp_ERROR_IMPOSING_IS_IMPOSSIBLE = 220
msp_ERROR_CASH_DEVICE_TABLE_OVERLOAD = 301
msp_ERROR_DEVICE_NOT_INTO_CASH = 302
msp_ERROR_CASH_INCORRECT_CALL_FUNCTION = 303
msp_ERROR_VXI_ERROR = 320


msp_MODE_NOT_DEFINED = 0x0000
msp_MODE_BC = 0x0001
msp_MODE_RT = 0x0002
msp_MODE_MM = 0x0004
msp_MODE_WM = 0x0008
msp_MODE_IDLE = 0x0010
msp_MODE_ENHANCED = 0x8000
msp_MODE_WG = 0x0020

msp_SWITCH_WITHOUT_RESET = 0x0100
msp_SWITCH_KEEP_RAM = 0x0200
msp_WG_FIRST = 0
msp_WM_FIRST = 0x4000
msp_MODE_MRT = 0x0040

mspRR_INTERRUPT_MASK = 0x00
mspRR_CONFIG1 = 0x01
mspRR_CONFIG2 = 0x02
mspRR_COMMAND = 0x03
mspRR_COMMAND_STACK_POINTER = 0x03
mspRR_CONTROL_WORD = 0x04
mspRR_TIME_TAG = 0x05
mspRR_INTERRUPT_STATUS = 0x06
mspRR_CONFIG3 = 0x07
mspRR_CONFIG4 = 0x08
mspRR_CONFIG5 = 0x09
mspRR_DATA_STACK_ADDRESS = 0x0A
mspRR_FRAME_TIME_REMAINING = 0x0B
mspRR_MESSAGE_TIME_REMAINING = 0x0C
mspRR_BC_FRAME_TIME = 0x0D
mspRR_RT_LAST_COMMAND = 0x0D
mspRR_MT_TRIGGER = 0x0D
mspRR_RT_STATUS_WORD = 0x0E
mspRR_RT_BIT_WORD = 0x0F
mspRR_MRT_ADDRESS = 0x10
mspRR_MRT_CONFIG1 = 0x11
mspRR_MRT_STATUS = 0x15
mspRR_MRT_INTERRUPT_STATUS = 0x16
mspRR_CONFIG6 = 0x18
mspRR_MRT_COMMAND_WORD = 0x1D
mspRR_MRT_STATUS_WORD = 0x1E

mspRR_EXTERNAL_CONFIG = 0x20
mspRR_EXTERNAL_RT_ADDRESS = 0x21
mspRR_EXTERNAL_CDIVIDER = 0x22
mspRR_EXTERNAL_FLOG_ID = 0x23

mspRR_EXTERNAL_USB_POWER = 0x24
mspRR_EXTERNAL_USB_FIRMWARE_VERSION = 0x25
mspRR_EXTERNAL_USB_COMMAND = 0x26

mspRR_SOFTWARE1 = 0xFF
mspRR_SOFTWARE2_MRT_ISR = 0xFE

mspRR_SOFTWARE_LOW = mspRR_SOFTWARE2_MRT_ISR


mspRR_WG_DATA_STACK_POINTER = 0x03
mspRR_WG_INITIAL_DATA_STACK_POINTER = 0x04

msp_CLOCK_12MHz = 1
msp_CLOCK_16MHz = 0
msp_CLOCK_24MHz = 2
msp_CLOCK_48MHz = 3


LPCI_LAS0RR = 0x00
LPCI_LAS1RR = 0x01
LPCI_LAS2RR = 0x02
LPCI_LAS3RR = 0x03
LPCI_EROMRR = 0x04
LPCI_LAS0BA = 0x05
LPCI_LAS1BA = 0x06
LPCI_LAS2BA = 0x07
LPCI_LAS3BA = 0x08
LPCI_EROMBA = 0x09
LPCI_LAS0BRD = 0x0A
LPCI_LAS1BRD = 0x0B
LPCI_LAS2BRD = 0x0C
LPCI_LAS3BRD = 0x0D
LPCI_EROMBRD = 0x0E
LPCI_CS0BASE = 0x0F
LPCI_CS1BASE = 0x10
LPCI_CS2BASE = 0x11
LPCI_CS3BASE = 0x12
LPCI_INTCSR = 0x13
LPCI_CNTRL = 0x14

msp_BCCW_RT_TO_RT_FORMAT = 0x0001
msp_BCCW_BROADCAST_FORMAT = 0x0002
msp_BCCW_MODE_CODE_FORMAT = 0x0004
msp_BCCW_1553A = 0x0008
msp_BCCW_1553B = 0x0000
msp_BCCW_EOM_INTR_ENABLE = 0x0010
msp_BCCW_MASK_BROADCAST = 0x0020
msp_BCCW_SELFTEST = 0x0040
msp_BCCW_CHANNEL_A = 0x0080
msp_BCCW_CHANNEL_B = 0x0000
msp_BCCW_RETRY_ENABLED = 0x0100
msp_BCCW_RESERVED_MASK = 0x0200
msp_BCCW_TERMINAL_FLAG_MASK = 0x0400
msp_BCCW_SUBSYSTEM_FLAG_MASK = 0x0800
msp_BCCW_BUSY_MASK = 0x1000
msp_BCCW_SERVICE_REQUEST_MASK = 0x2000
msp_BCCW_MESSAGE_ERROR_MASK = 0x4000
msp_BCCW_EX_BROADCAST_DISABLED = 0x10000
msp_BCCW_EX_MODECODE_SA_0 = 0x00000
msp_BCCW_EX_MODECODE_SA_31 = 0x20000

msp_FD_FrameTime = 0
msp_FD_MessageCount = 1
msp_FD_MaxMessgeCount = 2

msp_STK_A = 0
msp_STK_B = 1
msp_STK_mask = 1

mspM_fRECEIVE = 1
mspM_fTRANSMIT = 2
mspM_fMODECODE = 4
mspM_fBROADCAST = 8

mspM_EXTENDED = 0x10

mspM_EXTENDED_TERM = 0x30

mspM_BCtoRT = mspM_fRECEIVE
mspM_RTtoBC	= mspM_fTRANSMIT
mspM_RTtoRT	= mspM_fRECEIVE | mspM_fTRANSMIT
mspM_BCtoRT_BROADCAST = mspM_fRECEIVE | mspM_fBROADCAST
mspM_RTtoRT_BROADCAST = mspM_fRECEIVE | mspM_fTRANSMIT | mspM_fBROADCAST
mspM_MODECODE = mspM_fMODECODE
mspM_MODECODE_DATA_TX = mspM_fMODECODE | mspM_fTRANSMIT
mspM_MODECODE_DATA_RX = mspM_fMODECODE | mspM_fRECEIVE
mspM_MODECODE_BROADCAST = mspM_fMODECODE | mspM_fBROADCAST
mspM_MODECODE_DATA_BROADCAST = mspM_fMODECODE | mspM_fRECEIVE | mspM_fBROADCAST

mspM_UNDEFINED = 0

mspMC_DYNAMIC_BUS_CONTROL = 0x00
mspMC_SYNCHRONIZE = 0x01
mspMC_TRANSMIT_STATUS_WORD = 0x02
mspMC_INITIATE_SELF_TEST = 0x03
mspMC_TRANSMITTER_SHUTDOWN = 0x04
mspMC_OVERRIDE_TRANSMITTER_SHUTDOWN = 0x05
mspMC_INHIBIT_TFLAG = 0x06
mspMC_OVERRIDE_INHIBIT_TFLAG = 0x07
mspMC_RESET_REMOTE_TERMINAL = 0x08
mspMC_RESET_RT = mspMC_RESET_REMOTE_TERMINAL
mspMC_TRANSMIT_VECTOR_WORD = 0x10
mspMC_SYNCHRONIZE_WITH_DATA = 0x11
mspMC_TRANSMIT_LAST_COMMAND = 0x12
mspMC_TRANSMIT_BIT_WORD = 0x13
mspMC_SELECTED_TRANSMITTER_SHUTDOWN = 0x14
mspMC_OVERRIDE_SELECTED_TRANSMITTER_SHUTDOWN = 0x15


msp_STATUS_RTADD_MASK = 0xF800
msp_STATUS_MESSAGE_ERROR = 0x0400
msp_STATUS_INSTRUMENTATION = 0x0200
msp_STATUS_SERVICE_REQUEST = 0x0100
msp_STATUS_RESERVED_12 = 0x0080
msp_STATUS_RESERVED_13 = 0x0040
msp_STATUS_RESERVED_14 = 0x0020
msp_STATUS_BROADCAST_COMMAND_RECEIVED = 0x0010
msp_STATUS_BUSY = 0x0008
msp_STATUS_SUBSYSTEM_FLAG = 0x0004
msp_STATUS_DYNAMIC_BUS_CONTROL_ACCEPTED = 0x0002
msp_STATUS_TERMINAL_FLAG = 0x0001

msp_MW_BCCW = 32
msp_MW_CMD1 = 33
msp_MW_CMD2 = 34
msp_MW_STATUS1 = 35
msp_MW_STATUS2 = 36
msp_MW_LOOPBACK = 37
msp_MW_WORDCOUNT = 38
msp_MW_MODECODE = 39

msp_LAST_RECEIVED = 0xFFFF
msp_NEXT_MESSAGE = 0xFFFE
msp_SAME_MESSAGE = 0xFFFD

mspC_RESET = 0x0001
mspC_START = 0x0002
mspC_INTERRUPT_RESET = 0x0004
mspC_TIME_TAG_RESET = 0x0008
mspC_TIME_TAG_TEST_CLOCK = 0x0010
mspC_STOP_ON_FRAME = 0x0020
mspC_STOP_ON_MESSAGE = 0x0040

msp_of64 = 1 << 0
msp_ofZEROWAIT = 1 << 1
msp_ofBackDoor = 1 << 2
msp_ofShrinkRam	= 1 << 3

msp_FW_BSW = 0
msp_FW_TIMETAG = 1
msp_FW_MSGGAP = 2
msp_FW_MSGADDR = 3
msp_SW_BSW = 0
msp_SW_TIMETAG = 1
msp_SW_DBP = 2
msp_SW_CMD = 3


msp_LAST_RECEIVED = 0xFFFF
msp_NEXT_MESSAGE = 0xFFFE
msp_SAME_MESSAGE = 0xFFFD


msp_BSW_EOM = (1<<15)
msp_BSW_SOM = (1<<14)
msp_BSW_CHANNEL_B = (1<<13)
msp_BSW_ERROR_FLAG = (1<<12)
msp_BSW_FORMAT_ERROR = (1<<10)
msp_BSW_NO_RESPONSE_TIMEOUT = (1<<9)

msp_BSW_BC_EOM = (1<<15)
msp_BSW_BC_SOM = (1<<14)
msp_BSW_BC_CHANNEL_B = (1<<13)
msp_BSW_BC_ERROR_FLAG = (1<<12)
msp_BSW_BC_STATUS_SET = (1<<11)
msp_BSW_BC_FORMAT_ERROR = (1<<10)
msp_BSW_BC_NO_RESPONSE_TIMEOUT = (1<<9)
msp_BSW_BC_LOOP_TEST_FAIL = (1<<8)
msp_BSW_BC_MASKED_STATUS_SET = (1<<7)
msp_BSW_BC_DOUBLE_RETRY = (1<<6)
msp_BSW_BC_SINGLE_RETRY = (1<<5)
msp_BSW_BC_GOOD_DATA_BLOCK_TRANSFER = (1<<4)
msp_BSW_BC_STATUS_RESPONSE_ERROR = (1<<3)
msp_BSW_BC_WORD_COUNT_ERROR = (1<<2)
msp_BSW_BC_INCORRECT_SYNC_TYPE = (1<<1)
msp_BSW_BC_INVALID_WORD = 1

msp_BSW_RT_EOM = (1<<15)
msp_BSW_RT_SOM = (1<<14)
msp_BSW_RT_CHANNEL_B = (1<<13)
msp_BSW_RT_ERROR_FLAG = (1<<12)
msp_BSW_RT_RT_TO_RT = (1<<11)
msp_BSW_RT_FORMAT_ERROR = (1<<10)
msp_BSW_RT_NO_RESPONSE_TIMEOUT = (1<<9)
msp_BSW_RT_LOOP_TEST_FAIL = (1<<8)
msp_BSW_RT_CIRCULAR_BUFFER_ROLLOVER = (1<<7)
msp_BSW_RT_DATA_STACK_ROLLOVER = msp_BSW_RT_CIRCULAR_BUFFER_ROLLOVER

msp_BSW_RT_ILLEGAL_COMMAND_WORD = (1<<6)
msp_BSW_RT_WORD_COUNT_ERROR = (1<<5)
msp_BSW_RT_INCORRECT_DATA_SYNC = (1<<4)
msp_BSW_RT_INVALID_WORD = (1<<3)
msp_BSW_RT_STATUS_RESPONSE_ERROR = (1<<2)
msp_BSW_RT_SECOND_COMMAND_ERROR = (1<<1)
msp_BSW_RT_COMMAND_WORD_ERROR = 1

msp_BSW_MM_EOM = (1<<15)
msp_BSW_MM_SOM = (1<<14)
msp_BSW_MM_CHANNEL_B = (1<<13)
msp_BSW_MM_ERROR_FLAG = (1<<12)
msp_BSW_MM_RT_TO_RT = (1<<11)
msp_BSW_MM_FORMAT_ERROR = (1<<10)
msp_BSW_MM_NO_RESPONSE_TIMEOUT = (1<<9)
msp_BSW_MM_GOOD_DATA_BLOCK_TRANSFER = (1<<8)
msp_BSW_MM_DATA_STACK_ROLLOVER = (1<<7)

msp_BSW_MM_WORD_COUNT_ERROR = (1<<5)
msp_BSW_MM_INCORRECT_DATA_SYNC = (1<<4)
msp_BSW_MM_INVALID_WORD = (1<<3)
msp_BSW_MM_STATUS_RESPONSE_ERROR = (1<<2)
msp_BSW_MM_SECOND_COMMAND_ERROR = (1<<1)
msp_BSW_MM_COMMAND_WORD_ERROR = 1

msp_AUTOREPEAT = 0x0002

ERROR_CODES = {
    1: 'msp_ERROR_INVALID_DEVICE_HANDLE',
    2: 'msp_ERROR_INVALID_PARAMETER',
    3: 'msp_ERROR_NOT_INITIALIZED',
    4: 'msp_ERROR_SYSTEM_ERROR',
    5: 'msp_ERROR_DEVICE_BUSY',
    6: 'msp_ERROR_INTERNAL_ACCESS_ERROR',
    7: 'msp_ERROR_NO_HOST_MEMORY',
    8: 'msp_ERROR_ADDRESS_OUT_OF_RAM',
    9: 'msp_IRQ_BUSY',
    10: 'msp_ERROR_IRQ_CANCELLED',
    11: 'msp_ERROR_INTERNAL_INTEGRITY_ERROR',
    12: 'msp_ERROR_MISSING_DELAY_FUNC',
    13: 'msp_ERROR_UNSUPPORTED_FUNCTION',
    14: 'msp_ERROR_UNKNOWN_DEVICE_TYPE',
    15: 'msp_ERROR_UNSUPPORTED_DRIVER_TYPE',
    16: 'msp_ERROR_UNSUPPORTED_BUS_TYPE',
    17: 'msp_ERROR_DRIVER_NOT_FOUND',
    20: 'msp_ERROR_NO_FREE_RAM',
    21: 'msp_ERROR_INVALID_RAM_HANDLE',
    22: 'msp_ERROR_ILLEGAL_HANDLE_TYPE',
    23: 'msp_ERROR_HANDLE_OUT_OF_SCOPE',
    24: 'msp_ERROR_HANDLE_IN_USE',
    25: 'msp_ERROR_ADDRESS_OUT_OF_OBJECT',
    30: 'msp_ERROR_INVALID_FLAG',
    31: 'msp_ERROR_INVALID_VREG',
    32: 'msp_ERROR_UNSUPPORTED_MODE',
    33: 'msp_ERROR_MODE_NOT_SELECTED',
    34: 'msp_ERROR_INCOMPATIBLE_MODE',
    35: 'msp_ERROR_INCOMPATIBLE_CONFIGURATION',
    36: 'msp_ERROR_FRAM_NOT_RESERVED',
    40: 'msp_ERROR_INCOMPATIBLE_STACK',
    41: 'msp_ERROR_NOT_LOADED',
    42: 'msp_ERROR_INDEX_OUT_OF_RANGE',
    43: 'msp_ERROR_NO_NEXT_MESSAGE',
    44: 'msp_ERROR_MESSAGE_IN_PROGRESS',
    50: 'msp_ERROR_INVALID_MESSAGE_FORMAT',
    51: 'msp_ERROR_MESSAGE_FIELD_NOT_EXISTS',
    52: 'msp_ERROR_FRAME_EXCEEDS_SIZE_LIMIT',
    60: 'msp_ERROR_INCOMPATIBLE_BUFFER',
    61: 'msp_ERROR_BUFFER_NOT_CONNECTED',
    62: 'msp_ERROR_BUFFER_BUSY_SAFE',
    63: 'msp_ERROR_BUFFER_BUSY_UNSAFE',
    64: 'msp_ERROR_STREAM_DISABLED',
    65: 'msp_ERROR_STREAM_IN_USED',
    66: 'msp_ERROR_STREAM_CORRUPTED',
    67: 'msp_ERROR_ILLEGAL_COMMAND_WORD',
    68: 'msp_ERROR_NOT_MODE_CODE',
    70: 'msp_ERROR_TOO_MANY_FRAMES',
    71: 'msp_ERROR_INVALID_MESSAGE_HANDLE',
    72: 'msp_ERROR_INVALID_FRAME_HANDLE',
    80: 'msp_ERROR_ANSWER_NOT_MATCH',
    81: 'msp_ERROR_ANSWER_MISSING_WORDS',
    82: 'msp_ERROR_ANSWER_EXTRA_WORDS',
    83: 'msp_ERROR_INVALID_MESSAGE',
    84: 'msp_ERROR_ANSWER_ERROR',
    85: 'msp_ERROR_ANSWER_ANOTHER_CHANNEL',
    86: 'msp_ERROR_ANSWER_RT_BUSY',
    90: 'msp_ERROR_INTERNAL_ALGORITHM',
    100: 'msp_ERROR_EMPTY_FRAME',
    101: 'msp_ERROR_OVERLOAD_BUFFERS',
    102: 'msp_ERROR_INVALID_REQUEST',
    200: 'msp_ERROR_USB_EXCHANGE',
    201: 'msp_ERROR_USB_NOT_SUPPORT',
    202: 'msp_ERROR_USB_ACCESS',
    203: 'msp_ERROR_USB_FTDI_ERROR',
    204: 'msp_ERROR_USB_RESPONSE_TIMEOUT',
    205: 'msp_ERROR_USB_RESPONSE_FAILURE',
    210: 'msp_ERROR_DEVICES_NOT_FOUND',
    220: 'msp_ERROR_IMPOSING_IS_IMPOSSIBLE',
    301: 'msp_ERROR_CASH_DEVICE_TABLE_OVERLOAD',
    302: 'msp_ERROR_DEVICE_NOT_INTO_CASH',
    303: 'msp_ERROR_CASH_INCORRECT_CALL_FUNCTION',
    320: 'msp_ERROR_VXI_ERROR'
}

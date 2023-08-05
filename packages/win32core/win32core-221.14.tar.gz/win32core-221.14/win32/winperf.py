# Generated by h2py from winperf.h
PERF_DATA_VERSION = 1
PERF_DATA_REVISION = 1
PERF_NO_INSTANCES = -1
PERF_SIZE_DWORD = 0x00000000
PERF_SIZE_LARGE = 0x00000100
PERF_SIZE_ZERO = 0x00000200
PERF_SIZE_VARIABLE_LEN = 0x00000300
PERF_TYPE_NUMBER = 0x00000000
PERF_TYPE_COUNTER = 0x00000400
PERF_TYPE_TEXT = 0x00000800
PERF_TYPE_ZERO = 0x00000C00
PERF_NUMBER_HEX = 0x00000000
PERF_NUMBER_DECIMAL = 0x00010000
PERF_NUMBER_DEC_1000 = 0x00020000
PERF_COUNTER_VALUE = 0x00000000
PERF_COUNTER_RATE = 0x00010000
PERF_COUNTER_FRACTION = 0x00020000
PERF_COUNTER_BASE = 0x00030000
PERF_COUNTER_ELAPSED = 0x00040000
PERF_COUNTER_QUEUELEN = 0x00050000
PERF_COUNTER_HISTOGRAM = 0x00060000
PERF_TEXT_UNICODE = 0x00000000
PERF_TEXT_ASCII = 0x00010000
PERF_TIMER_TICK = 0x00000000
PERF_TIMER_100NS = 0x00100000
PERF_OBJECT_TIMER = 0x00200000
PERF_DELTA_COUNTER = 0x00400000
PERF_DELTA_BASE = 0x00800000
PERF_INVERSE_COUNTER = 0x01000000
PERF_MULTI_COUNTER = 0x02000000
PERF_DISPLAY_NO_SUFFIX = 0x00000000
PERF_DISPLAY_PER_SEC = 0x10000000
PERF_DISPLAY_PERCENT = 0x20000000
PERF_DISPLAY_SECONDS = 0x30000000
PERF_DISPLAY_NOSHOW = 0x40000000
PERF_COUNTER_COUNTER = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_DISPLAY_PER_SEC)
PERF_COUNTER_TIMER = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_DISPLAY_PERCENT)
PERF_COUNTER_QUEUELEN_TYPE = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_QUEUELEN |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_LARGE_QUEUELEN_TYPE = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_QUEUELEN |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_BULK_COUNT = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_DISPLAY_PER_SEC)
PERF_COUNTER_TEXT = \
    (PERF_SIZE_VARIABLE_LEN | PERF_TYPE_TEXT | PERF_TEXT_UNICODE |
     PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_RAWCOUNT = \
    (PERF_SIZE_DWORD | PERF_TYPE_NUMBER | PERF_NUMBER_DECIMAL |
     PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_LARGE_RAWCOUNT = \
    (PERF_SIZE_LARGE | PERF_TYPE_NUMBER | PERF_NUMBER_DECIMAL |
     PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_RAWCOUNT_HEX = \
    (PERF_SIZE_DWORD | PERF_TYPE_NUMBER | PERF_NUMBER_HEX |
     PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_LARGE_RAWCOUNT_HEX = \
    (PERF_SIZE_LARGE | PERF_TYPE_NUMBER | PERF_NUMBER_HEX |
     PERF_DISPLAY_NO_SUFFIX)
PERF_SAMPLE_FRACTION = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_FRACTION |
     PERF_DELTA_COUNTER | PERF_DELTA_BASE | PERF_DISPLAY_PERCENT)
PERF_SAMPLE_COUNTER = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_NODATA = \
    (PERF_SIZE_ZERO | PERF_DISPLAY_NOSHOW)
PERF_COUNTER_TIMER_INV = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_TICK | PERF_DELTA_COUNTER | PERF_INVERSE_COUNTER |
     PERF_DISPLAY_PERCENT)
PERF_SAMPLE_BASE = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_BASE |
     PERF_DISPLAY_NOSHOW |
     0x00000001)
PERF_AVERAGE_TIMER = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_FRACTION |
     PERF_DISPLAY_SECONDS)
PERF_AVERAGE_BASE = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_BASE |
     PERF_DISPLAY_NOSHOW |
     0x00000002)
PERF_AVERAGE_BULK = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_FRACTION |
     PERF_DISPLAY_NOSHOW)
PERF_100NSEC_TIMER = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_100NS | PERF_DELTA_COUNTER | PERF_DISPLAY_PERCENT)
PERF_100NSEC_TIMER_INV = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_TIMER_100NS | PERF_DELTA_COUNTER | PERF_INVERSE_COUNTER |
     PERF_DISPLAY_PERCENT)
PERF_COUNTER_MULTI_TIMER = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_DELTA_COUNTER | PERF_TIMER_TICK | PERF_MULTI_COUNTER |
     PERF_DISPLAY_PERCENT)
PERF_COUNTER_MULTI_TIMER_INV = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_RATE |
     PERF_DELTA_COUNTER | PERF_MULTI_COUNTER | PERF_TIMER_TICK |
     PERF_INVERSE_COUNTER | PERF_DISPLAY_PERCENT)
PERF_COUNTER_MULTI_BASE = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_BASE |
     PERF_MULTI_COUNTER | PERF_DISPLAY_NOSHOW)
PERF_100NSEC_MULTI_TIMER = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_DELTA_COUNTER |
     PERF_COUNTER_RATE | PERF_TIMER_100NS | PERF_MULTI_COUNTER |
     PERF_DISPLAY_PERCENT)
PERF_100NSEC_MULTI_TIMER_INV = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_DELTA_COUNTER |
     PERF_COUNTER_RATE | PERF_TIMER_100NS | PERF_MULTI_COUNTER |
     PERF_INVERSE_COUNTER | PERF_DISPLAY_PERCENT)
PERF_RAW_FRACTION = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_FRACTION |
     PERF_DISPLAY_PERCENT)
PERF_RAW_BASE = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_BASE |
     PERF_DISPLAY_NOSHOW |
     0x00000003)
PERF_ELAPSED_TIME = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_ELAPSED |
     PERF_OBJECT_TIMER | PERF_DISPLAY_SECONDS)
PERF_COUNTER_HISTOGRAM_TYPE = -2147483648  # 0x80000000
PERF_COUNTER_DELTA = \
    (PERF_SIZE_DWORD | PERF_TYPE_COUNTER | PERF_COUNTER_VALUE |
     PERF_DELTA_COUNTER | PERF_DISPLAY_NO_SUFFIX)
PERF_COUNTER_LARGE_DELTA = \
    (PERF_SIZE_LARGE | PERF_TYPE_COUNTER | PERF_COUNTER_VALUE |
     PERF_DELTA_COUNTER | PERF_DISPLAY_NO_SUFFIX)
PERF_DETAIL_NOVICE = 100
PERF_DETAIL_ADVANCED = 200
PERF_DETAIL_EXPERT = 300
PERF_DETAIL_WIZARD = 400
PERF_NO_UNIQUE_ID = -1

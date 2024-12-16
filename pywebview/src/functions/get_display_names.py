import ctypes
from ctypes import wintypes

class DISPLAY_DEVICE(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("DeviceName", wintypes.WCHAR * 32),
        ("DeviceString", wintypes.WCHAR * 128),
        ("StateFlags", wintypes.DWORD),
        ("DeviceID", wintypes.WCHAR * 128),
        ("DeviceKey", wintypes.WCHAR * 128),
    ]

DISPLAY_DEVICE_ACTIVE = 0x00000001  # Флаг активного дисплея

def get_display_names():
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    EnumDisplayDevicesW = user32.EnumDisplayDevicesW
    EnumDisplayDevicesW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(DISPLAY_DEVICE), wintypes.DWORD]
    EnumDisplayDevicesW.restype = wintypes.BOOL

    active_displays = []
    i = 0
    while True:
        device = DISPLAY_DEVICE()
        device.cb = ctypes.sizeof(DISPLAY_DEVICE)
        if not EnumDisplayDevicesW(None, i, ctypes.byref(device), 0):
            break

        # Проверяем флаг активности дисплея
        if device.StateFlags & DISPLAY_DEVICE_ACTIVE:
            active_displays.append(device.DeviceName)
        i += 1

    return active_displays

# Пример использования
# active_display_names = get_active_display_names()
# print("Active Display Names:", active_display_names)

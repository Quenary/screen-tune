import ctypes
from ctypes import wintypes
import psutil

# Определяем необходимые функции Windows API
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = wintypes.HWND

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
GetWindowThreadProcessId.restype = wintypes.DWORD

def get_active_window_process_name() -> str:
    """
    Get process name of active window, e.g. code.exe
    """
    hwnd = GetForegroundWindow()  # Получаем дескриптор активного окна
    if not hwnd:
        return None
    pid = wintypes.DWORD()
    thread_id = GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if not thread_id:
        return None
    try:
        process = psutil.Process(pid.value)
        return process.name()
    except psutil.NoSuchProcess:
        return None

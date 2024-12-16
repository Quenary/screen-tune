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

def get_active_window_process():
    """Получает имя процесса активного окна."""
    hwnd = GetForegroundWindow()  # Получаем дескриптор активного окна
    if not hwnd:
        return None

    pid = wintypes.DWORD()
    thread_id = GetWindowThreadProcessId(hwnd, ctypes.byref(pid))  # Получаем PID процесса
    if not thread_id:
        return None

    # Используем библиотеку psutil для получения информации о процессе
    try:
        process = psutil.Process(pid.value)
        return process.name()  # Возвращаем имя процесса
    except psutil.NoSuchProcess:
        return None

# # Пример отслеживания изменения активного окна
# import time

# last_window = None

# try:
#     while True:
#         current_window = get_active_window_process()
#         if current_window != last_window:
#             print(f"Активное окно изменилось, процесс: {current_window}")
#             last_window = current_window
#         time.sleep(0.5)  # Периодическое обновление
# except KeyboardInterrupt:
#     print("Завершение отслеживания.")

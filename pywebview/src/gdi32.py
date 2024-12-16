import ctypes
from ctypes import wintypes
import numpy as np

# Определение структуры для RAMP
class RAMP(ctypes.Structure):
    _fields_ = [
        ("Red", ctypes.c_uint16 * 256),
        ("Green", ctypes.c_uint16 * 256),
        ("Blue", ctypes.c_uint16 * 256),
    ]

# Загрузка gdi32.dll
gdi32 = ctypes.WinDLL('gdi32')

# Определение функций из gdi32.dll
gdi32.DeleteDC.argtypes = [wintypes.HDC]
gdi32.DeleteDC.restype = wintypes.BOOL

gdi32.CreateDCW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPVOID]
gdi32.CreateDCW.restype = wintypes.HDC

gdi32.GetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.POINTER(RAMP)]
gdi32.GetDeviceGammaRamp.restype = wintypes.BOOL

gdi32.SetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.POINTER(RAMP)]
gdi32.SetDeviceGammaRamp.restype = wintypes.BOOL

class GammaController:
    @staticmethod
    def normalize_display_name(name: str) -> str:
        return name.replace('\\\\.', '\\.')

    def create_dc(self, display_name: str) -> wintypes.HDC:
        normalized_name = self.normalize_display_name(display_name)
        hdc = gdi32.CreateDCW(None, normalized_name, None, None)
        if hdc == 0:
            raise RuntimeError("Failed to create device context")
        return hdc

    def delete_dc(self, hdc: wintypes.HDC) -> bool:
        return bool(gdi32.DeleteDC(hdc))

    def get_device_gamma_ramp(self, display_name: str):
        hdc = self.create_dc(display_name)
        ramp = RAMP()
        if not gdi32.GetDeviceGammaRamp(hdc, ctypes.byref(ramp)):
            self.delete_dc(hdc)
            raise RuntimeError("Failed to get device gamma ramp")
        self.delete_dc(hdc)
        return {
            "Red": list(ramp.Red),
            "Green": list(ramp.Green),
            "Blue": list(ramp.Blue),
        }

    def set_device_gamma_ramp(self, display_name: str, ramp_values: dict) -> bool:
        hdc = self.create_dc(display_name)
        ramp = RAMP(
            Red=(ctypes.c_uint16 * 256)(*ramp_values["Red"]),
            Green=(ctypes.c_uint16 * 256)(*ramp_values["Green"]),
            Blue=(ctypes.c_uint16 * 256)(*ramp_values["Blue"]),
        )
        result = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
        self.delete_dc(hdc)
        return bool(result)

    def calculate_ramp_values(self, brightness=0.5, contrast=0.5, gamma=1.0) -> list:
        uint_max = 65535
        data_points = 256

        gamma = max(0.4, min(gamma, 2.8))
        contrast = (max(0, min(contrast, 1)) - 0.5) * 2
        brightness = (max(0, min(brightness, 1)) - 0.5) * 2

        offset = contrast * -25.4 if contrast > 0 else contrast * -32
        range_curve = (data_points - 1) + offset * 2
        offset += brightness * (range_curve / 5)

        values = []
        for i in range(data_points):
            factor = (i + offset) / range_curve
            factor = pow(factor, 1 / gamma)
            factor = min(max(factor, 0), 1)
            values.append(round(factor * uint_max))

        return values

# Пример использования
# gamma_controller = GammaController()

# # Получение текущего gamma ramp
# current_ramp = gamma_controller.get_device_gamma_ramp("\\\\.\\DISPLAY1")
# print("Current Ramp:", current_ramp)

# # Установка нового gamma ramp
# new_ramp = {
#     "Red": gamma_controller.calculate_ramp_values(brightness=0.7, contrast=0.6, gamma=1.2),
#     "Green": gamma_controller.calculate_ramp_values(brightness=0.7, contrast=0.6, gamma=1.2),
#     "Blue": gamma_controller.calculate_ramp_values(brightness=0.7, contrast=0.6, gamma=1.2),
# }
# gamma_controller.set_device_gamma_ramp("\\\\.\\DISPLAY1", new_ramp)
# print("Gamma ramp updated.")

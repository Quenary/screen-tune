import ctypes
from ctypes import wintypes

class RAMP(ctypes.Structure):
    """C type for display's gamma ramp."""
    _fields_ = [
        ("Red", ctypes.c_uint16 * 256),
        ("Green", ctypes.c_uint16 * 256),
        ("Blue", ctypes.c_uint16 * 256),
    ]

# Load gdi32.dll
gdi32 = ctypes.WinDLL('gdi32')

# Define gdi32.dll functions
gdi32.DeleteDC.argtypes = [wintypes.HDC]
gdi32.DeleteDC.restype = wintypes.BOOL

gdi32.CreateDCW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPVOID]
gdi32.CreateDCW.restype = wintypes.HDC

gdi32.GetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.POINTER(RAMP)]
gdi32.GetDeviceGammaRamp.restype = wintypes.BOOL

gdi32.SetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.POINTER(RAMP)]
gdi32.SetDeviceGammaRamp.restype = wintypes.BOOL

class Gdi32Wrapper:
    """Wrapper for gdi32.dll nessary functions."""
    def create_dc(self, display_name: str) -> wintypes.HDC:
        try:
            device = "DISPLAY"
            hdc = gdi32.CreateDCW(device, display_name, None, None)
            if not hdc:
                error_code = ctypes.GetLastError()
                raise RuntimeError(f"Error code: {error_code}")
            return hdc
        except Exception as e:
            print(f"Error creating device context for display: {display_name}; {e}")
            return None

    def delete_dc(self, hdc: wintypes.HDC) -> bool:
        try:
            return bool(gdi32.DeleteDC(hdc))
        except Exception as e:
            print(f"Error deleting device context: {e}")
            return False

    def get_device_gamma_ramp(self, display_name: str):
        try:
            hdc = self.create_dc(display_name)
            ramp = RAMP()
            gdi32.GetDeviceGammaRamp(hdc, ctypes.byref(ramp))
            self.delete_dc(hdc)
            return {
                "Red": list(ramp.Red),
                "Green": list(ramp.Green),
                "Blue": list(ramp.Blue),
            }
        except Exception as e:
            print(f"Error getting gamma ramp for display: {display_name}; {e}")
            return None

    def set_device_gamma_ramp(self, display_name: str, ramp_values: dict) -> bool:
        try:
            hdc = self.create_dc(display_name)
            ramp = RAMP(
                Red=(ctypes.c_uint16 * 256)(*ramp_values["Red"]),
                Green=(ctypes.c_uint16 * 256)(*ramp_values["Green"]),
                Blue=(ctypes.c_uint16 * 256)(*ramp_values["Blue"]),
            )
            result = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
            self.delete_dc(hdc)
            return bool(result)
        except Exception as e:
            print(f"Error setting gamma ramp for display: {display_name}; {e}")
            return False

    def calculate_ramp_values(self, brightness=0.5, contrast=0.5, gamma=1.0) -> list:
        """
        Calculate gamma ramp array based on listed parameters.
        :param brightness: (float): Brightness value between 0 and 1.
        :param contrast: (float): Contrast value between 0 and 1.
        :param gamma: (float): Gamma value between 0.4 and 2.8.
        :returns: Gamma ramp list with 256 values.
        """
        try:
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
        except Exception as e:
            print(f"Error calculating gamma ramp values: {e}")
            return None
    
    def get_flat_ramp(self, values: list) -> dict:
        """
        Creates ramp with equal values for each color.
        :param values: list of values
        """
        return {
            "Red": values,
            "Green": values,
            "Blue": values,
        }
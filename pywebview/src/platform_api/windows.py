import ctypes
from ctypes import wintypes
import psutil
from . import PlatformApi


class RAMP(ctypes.Structure):
    """C type for display's gamma ramp."""

    _fields_ = [
        ("Red", ctypes.c_uint16 * 256),
        ("Green", ctypes.c_uint16 * 256),
        ("Blue", ctypes.c_uint16 * 256),
    ]


class DISPLAY_DEVICE(ctypes.Structure):
    """C type for display device."""

    _fields_ = [
        ("cb", wintypes.DWORD),
        ("DeviceName", wintypes.WCHAR * 32),
        ("DeviceString", wintypes.WCHAR * 128),
        ("StateFlags", wintypes.DWORD),
        ("DeviceID", wintypes.WCHAR * 128),
        ("DeviceKey", wintypes.WCHAR * 128),
    ]


# Load user32.dll
user32 = ctypes.WinDLL("user32", use_last_error=True)
EnumDisplayDevicesW = user32.EnumDisplayDevicesW
EnumDisplayDevicesW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.POINTER(DISPLAY_DEVICE),
    wintypes.DWORD,
]
EnumDisplayDevicesW.restype = wintypes.BOOL
GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = wintypes.HWND
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
GetWindowThreadProcessId.restype = wintypes.DWORD
DISPLAY_DEVICE_ACTIVE = 0x00000001  # Active display flag

# Load gdi32.dll
gdi32 = ctypes.WinDLL("gdi32")
gdi32.DeleteDC.argtypes = [wintypes.HDC]
gdi32.DeleteDC.restype = wintypes.BOOL
gdi32.CreateDCW.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPVOID,
]
gdi32.CreateDCW.restype = wintypes.HDC
gdi32.GetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.POINTER(RAMP)]
gdi32.GetDeviceGammaRamp.restype = wintypes.BOOL
gdi32.SetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.POINTER(RAMP)]
gdi32.SetDeviceGammaRamp.restype = wintypes.BOOL


class WindowsApi(PlatformApi):
    """Wrapper for Windows apis as gdi32.dll or user32.dll nessary functions."""

    def set_display_settings(
        self, display_name: str, brightness: float, contrast: float, gamma: float
    ) -> bool:
        ramp = self._calculate_ramp_values(brightness, contrast, gamma)
        flat_ramp = self._get_flat_ramp(ramp)
        return self._set_device_gamma_ramp(display_name, flat_ramp)

    def get_display_names(self) -> list:
        active_displays = []
        i = 0
        while True:
            device = DISPLAY_DEVICE()
            device.cb = ctypes.sizeof(DISPLAY_DEVICE)
            if not EnumDisplayDevicesW(None, i, ctypes.byref(device), 0):
                break

            # Check if the display is active
            if device.StateFlags & DISPLAY_DEVICE_ACTIVE:
                active_displays.append(device.DeviceName)
            i += 1

        return active_displays

    def get_active_window_process_name(self) -> str:
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

    def _create_dc(self, display_name: str) -> wintypes.HDC:
        """Create device context."""
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

    def _delete_dc(self, hdc: wintypes.HDC) -> bool:
        """Delete device context."""
        try:
            return bool(gdi32.DeleteDC(hdc))
        except Exception as e:
            print(f"Error deleting device context: {e}")
            return False

    def _get_device_gamma_ramp(self, display_name: str):
        """Get gamma ramp of a specific display."""
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

    def _set_device_gamma_ramp(self, display_name: str, ramp_values: dict) -> bool:
        """Set gamma ramp for a specific display."""
        try:
            hdc = self._create_dc(display_name)
            ramp = RAMP(
                Red=(ctypes.c_uint16 * 256)(*ramp_values["Red"]),
                Green=(ctypes.c_uint16 * 256)(*ramp_values["Green"]),
                Blue=(ctypes.c_uint16 * 256)(*ramp_values["Blue"]),
            )
            result = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
            self._delete_dc(hdc)
            return bool(result)
        except Exception as e:
            print(f"Error setting gamma ramp for display: {display_name}; {e}")
            return False

    def _calculate_ramp_values(self, brightness=0.5, contrast=0.5, gamma=1.0) -> list:
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

    def _get_flat_ramp(self, values: list) -> dict:
        """
        Creates ramp with equal values for each color.
        :param values: list of values
        """
        return {
            "Red": values,
            "Green": values,
            "Blue": values,
        }

import subprocess
from Xlib import display
from Xlib.ext import record
from Xlib.protocol import rq
import psutil
from . import PlatformApi


class LinuxApi(PlatformApi):
    """Wrapper for Linux functionality using xrandr and Xlib."""
    
    def set_display_settings(self, display_name: str, gamma: float, *args, **kwargs):
        try:
            gamma = max(0.4, min(gamma, 2.8))  # Clamp gamma to safe range
            subprocess.run(["xrandr", "--output", display_name, "--gamma", f"{gamma}:{gamma}:{gamma}"])
            return True
        except Exception as e:
            print(f"Error setting gamma ramp for display {display_name}: {e}")
            return False

    def get_display_names(self) -> list:
        try:
            result = subprocess.run(["xrandr", "--listmonitors"], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            displays = []
            for line in lines:
                if "+" in line and " " in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        displays.append(parts[-1])
            return displays
        except Exception as e:
            print(f"Error retrieving display names: {e}")
            return []

    def get_active_window_process_name(self) -> str:
        try:
            d = display.Display()
            root = d.screen().root
            window_id = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), rq.AnyPropertyType).value[0]
            window = d.create_resource_object('window', window_id)
            pid = window.get_full_property(d.intern_atom('_NET_WM_PID'), rq.AnyPropertyType).value[0]
            process = psutil.Process(pid)
            return process.name()
        except Exception as e:
            print(f"Error getting active window process name: {e}")
            return None
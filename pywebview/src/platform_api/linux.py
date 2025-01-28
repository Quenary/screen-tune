import subprocess
from Xlib import display
from Xlib.ext import record
from Xlib.protocol import rq
import psutil
from . import PlatformApi
from env import Env
import os


class LinuxApi(PlatformApi):
    """Wrapper for Linux functionality using xrandr and Xlib."""
    
    def __init__(self, env: Env):
        self._env = env
        self.desktop_file_path = os.path.expanduser(f"~/.config/autostart/{self._env.APP_NAME}.desktop")
    
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
        
    def _get_executable_path(self) -> str:
        return os.path.abspath(self._env.APP_EXECUTABLE or os.sys.executable)

    def _generate_desktop_entry(self) -> str:
        executable_path = self._get_executable_path()
        return f"""[Desktop Entry]
Type=Application
Name={self._env.APP_NAME}
Exec={executable_path}
X-GNOME-Autostart-enabled=true
"""

    def _update_autorun_path(self) -> None:
        if os.path.exists(self.desktop_file_path):
            with open(self.desktop_file_path, "r") as file:
                content = file.read()
                if f"Exec={self._get_executable_path()}" not in content:
                    print("Updating autorun path...")
                    self.enable_autorun()

    def enable_autorun(self) -> None:
        os.makedirs(os.path.dirname(self.desktop_file_path), exist_ok=True)
        with open(self.desktop_file_path, "w") as file:
            file.write(self._generate_desktop_entry())
        print(f"Autorun enabled: {self.desktop_file_path}")

    def disable_autorun(self) -> None:
        try:
            os.remove(self.desktop_file_path)
            print("Autorun disabled.")
        except FileNotFoundError:
            print("Autorun file not found while disabling.")

    def is_autorun_enabled(self) -> bool:
        if not os.path.exists(self.desktop_file_path):
            return False

        with open(self.desktop_file_path, "r") as file:
            content = file.read()
            return f"Exec={self._get_executable_path()}" in content

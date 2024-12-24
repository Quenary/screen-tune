import subprocess
import re
import psutil
from . import PlatformApi

class LinuxApi(PlatformApi):
    """Wrapper for Linux APIs using xrandr, xdotool, and xprop."""

    def set_display_settings(self, display_name: str, brightness: float, contrast: float, gamma: float) -> bool:
        try:
            gamma_value = max(0.4, min(gamma, 2.8))
            command = ["xrandr", "--output", display_name, "--gamma", f"{gamma_value}:{gamma_value}:{gamma_value}"]
            subprocess.run(command, check=True)
            return True
        except subprocess.SubprocessError as e:
            print(f"Error setting display settings for {display_name}: {e}")
            return False

    def get_display_names(self) -> list:
        try:
            result = subprocess.run(["xrandr", "--listmonitors"], check=True, stdout=subprocess.PIPE, text=True)
            lines = result.stdout.splitlines()
            displays = []
            for line in lines[1:]:  # Skip the first line as it's header
                match = re.search(r"\s+\d+:\s+\+\*?([\w-]+)", line)
                if match:
                    displays.append(match.group(1))
            return displays
        except subprocess.SubprocessError as e:
            print(f"Error fetching display names: {e}")
            return []

    def get_active_window_process_name(self) -> str:
        try:
            # Get the window ID of the currently active window
            window_id = subprocess.run(["xdotool", "getactivewindow"], check=True, stdout=subprocess.PIPE, text=True).stdout.strip()

            # Get the PID of the process that owns the window
            process_info = subprocess.run(["xprop", "-id", window_id], check=True, stdout=subprocess.PIPE, text=True).stdout
            match = re.search(r"_NET_WM_PID\(CARDINAL\) = (\d+)", process_info)
            if match:
                pid = int(match.group(1))
                process = psutil.Process(pid)
                return process.name()
            else:
                print("Could not find PID for the active window.")
                return None
        except (subprocess.SubprocessError, psutil.NoSuchProcess) as e:
            print(f"Error fetching active window process name: {e}")
            return None

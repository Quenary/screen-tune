import sys
import winreg
from env import Env


class AutorunManager:
    def __init__(self, env: Env):
        self._env = env
        self.registry_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    def _update_autorun_path(self) -> None:
        current_path = self._get_executable_path()
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_SET_VALUE
            ) as key:
                value, _ = winreg.QueryValueEx(key, self._env.APP_NAME)
                if value != current_path:
                    print(f"Updating autorun path: {value} -> {current_path}")
                    winreg.SetValueEx(
                        key, self._env.APP_NAME, 0, winreg.REG_SZ, current_path
                    )
        except FileNotFoundError:
            print("Autorun key not found. Enabling autorun...")
            self.enable_autorun()

    def _get_executable_path(self) -> str:
        return sys.executable

    def enable_autorun(self) -> None:
        executable_path = self._get_executable_path()
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(
                key, self._env.APP_NAME, 0, winreg.REG_SZ, executable_path
            )

    def disable_autorun(self) -> None:
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_SET_VALUE
            ) as key:
                winreg.DeleteValue(key, self._env.APP_NAME)
        except FileNotFoundError:
            print("Autorun key not found while disabling autorun.")
            pass

    def is_autorun_enabled(self) -> bool:
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, self.registry_path, 0, winreg.KEY_QUERY_VALUE
            ) as key:
                value, _ = winreg.QueryValueEx(key, self._env.APP_NAME)
                return value == self._get_executable_path()
        except FileNotFoundError:
            return False

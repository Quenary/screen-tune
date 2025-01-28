import sys
from abc import ABC, abstractmethod
from env import Env


class PlatformApi(ABC):
    @abstractmethod
    def __init__(self, env: Env):
        pass
    
    @abstractmethod
    def set_display_settings(
        self, display_name: str, brightness: float, contrast: float, gamma: float
    ):
        """Set display color settings"""
        pass

    @abstractmethod
    def get_display_names(self) -> list:
        """Get names of connected displays"""
        pass

    @abstractmethod
    def get_active_window_process_name(self) -> str:
        """Get process name of active window"""
        pass
    
    @abstractmethod
    def enable_autorun(self):
        """Enable autorun on system startup"""
        pass
    
    @abstractmethod
    def disable_autorun(self):
        """Disable autorun on system startup"""
        pass
    
    @abstractmethod
    def is_autorun_enabled(self) -> bool:
        """Check if autorun is enabled"""
        pass


def platform():
    if sys.platform == "win32":
        from .windows import WindowsApi

        return WindowsApi
    elif sys.platform == "linux2":
        from .linux import LinuxApi

        return LinuxApi
    raise NotImplementedError("platform not supported")


PLATFORM_API: PlatformApi = platform()
del platform

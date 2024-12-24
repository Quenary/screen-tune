from config import Config, ConfigDict
from autorun_manager import AutorunManager
from event_handler import EventHandler
import webbrowser
from functions.get_process_names import get_process_names
from functions.check_latest_release import check_latest_release
from env import Env
from platform_api import PlatformApi


class Api:
    def __init__(
        self,
        env: Env,
        config: Config,
        autorun_manager: AutorunManager,
        platform_api: PlatformApi,
        event_handler: EventHandler,
        on_exit: callable,
    ):
        self._env = env
        self._config = config
        self._autorun_manager = autorun_manager
        self._platform_api = platform_api
        self._event_handler = event_handler
        self._on_exit = on_exit

    def get_display_names(self) -> list:
        return self._platform_api.get_display_names()

    def get_process_names(self) -> list:
        return get_process_names()

    def open_external_url(self, url: str) -> bool:
        return webbrowser.open(url)

    def exit(self) -> None:
        self._on_exit()
        return None

    def get_active_window_process(self) -> str:
        return self._platform_api.get_active_window_process_name()

    def get_config(self) -> ConfigDict:
        return self._config.get_config()

    def set_config(self, config: ConfigDict) -> None:
        return self._config.set_config(config)

    def update_config(self, config: ConfigDict) -> None:
        return self._config.update_config(config)

    def set_autorun(self, flag: bool) -> None:
        if flag:
            self._autorun_manager.enable_autorun()
        else:
            self._autorun_manager.disable_autorun()

    def get_autorun(self) -> bool:
        return self._autorun_manager.is_autorun_enabled()

    def get_app_version(self) -> str:
        return self._env.VERSION

    def check_latest_release(self) -> dict:
        repo_url = self._env.HOME_PAGE
        version = self._env.VERSION
        return check_latest_release(repo_url, version)

    def set_live_preview_active(self, active: bool) -> None:
        return self._event_handler.set_live_preview_active(active)

    def set_live_preview_values(self, values: ConfigDict) -> None:
        return self._event_handler.set_live_preview_values(values)
    
    def is_worker_active(self) -> bool:
        return self._event_handler.is_running()
    
    def toggle_worker(self) -> None:
        is_running = self._event_handler.is_running()
        if is_running:
            self._event_handler.stop()
        else:
            self._event_handler.stop()

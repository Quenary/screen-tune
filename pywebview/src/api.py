from config import Config, ConfigDict
from autorun_manager import AutorunManager
from event_handler import EventHandler
import webbrowser
from functions.get_active_window_process_name import get_active_window_process_name
from functions.get_display_names import get_display_names
from functions.get_process_names import get_process_names
from functions.check_latest_release import check_latest_release
from env import Env
import webview


class Api:
    def __init__(
        self,
        env: Env,
        config: Config,
        autorun_manager: AutorunManager,
        event_handler: EventHandler,
    ):
        self._env = env
        self._config = config
        self._autorun_manager = autorun_manager
        self._event_handler = event_handler

    def get_display_names(self) -> list:
        return get_display_names()

    def get_process_names(self) -> list:
        return get_process_names()

    def open_external_url(self, url: str) -> bool:
        return webbrowser.open(url)

    def exit(self) -> None:
        return webview.active_window().destroy()

    def get_active_window_process(self) -> str:
        return get_active_window_process_name()

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

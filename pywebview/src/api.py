from gdi32 import GammaController
from config import Config, ConfigDict
from autorun import Autorun
import webbrowser
from functions.get_active_window_process import get_active_window_process
from functions.get_display_names import get_display_names
from functions.get_process_names import get_process_names
from functions.check_latest_release import check_latest_release
from functions.get_app_version import get_app_version
import webview

__repo_url = "https://github.com/Quenary/screen-tune"

class Api:
    def __init__(
        self,
        config: Config,
        autorun: Autorun,
    ):
        self.__config = config
        self.__autorun = autorun

    def get_display_names(self):
        return get_display_names()
    
    def get_process_names(self):
        return get_process_names()

    def open_external_url(self, url: str):
        webbrowser.open(url)

    def exit(self):
        webview.active_window().destroy()

    def get_active_window_process(self) -> str:
        return get_active_window_process()

    def get_config(self) -> ConfigDict:
        return self.__config.get_config()

    def set_config(self, config: ConfigDict):
        self.__config.set_config(config)

    def update_config(self, config: ConfigDict):
        self.__config.update_config(config)

    def set_autorun(self, flag: bool):
        self.__autorun.set_autorun(flag)

    def get_autorun(self) -> bool:
        return self.__autorun.get_autorrun()

    def get_app_version(self) -> str:
        return get_app_version()
    
    def check_latest_release(self):
        return check_latest_release()

import tomllib
import os
import sys


class Env:
    def __init__(self):
        self._displayed_app_name = "Screen Tune"
        if hasattr(sys, "_MEIPASS"):
            self._working_dir = sys._MEIPASS
            self._index_path = os.path.join(self._working_dir, "frontend", "index.html")
            self._toml_path = os.path.join(self._working_dir, "pyproject.toml")
        else:
            self._working_dir = os.path.dirname(__file__)
            self._index_path = "http://localhost:4200/"
            self._toml_path = os.path.join(self._working_dir, "..", "pyproject.toml")

        self._icon_path = os.path.join(self._working_dir, "assets", "icon.png")
        self._config_path = os.path.join(self._working_dir, "config.json")
        self._app_log_path = os.path.join(self._working_dir, "app.log")
        self._window_log_path = os.path.join(self._working_dir, "window.log")

        with open(self._toml_path, "rb") as f:
            self._pyproject_data = tomllib.load(f)
        self._app_name = self._pyproject_data["project"]["name"]
        self._version = self._pyproject_data["project"]["version"]
        self._home_page = self._pyproject_data["project"]["urls"]["Homepage"]

    @property
    def WORKING_DIR(self) -> str:
        return self._working_dir

    @property
    def CONFIG_PATH(self) -> str:
        return self._config_path

    @property
    def APP_LOG_PATH(self) -> str:
        return self._app_log_path

    @property
    def WINDOW_LOG_PATH(self) -> str:
        return self._window_log_path

    @property
    def INDEX_PATH(self) -> str:
        return self._index_path

    @property
    def ICON_PATH(self) -> str:
        return self._icon_path

    @property
    def DISPLAYED_APP_NAME(self) -> str:
        return self._displayed_app_name

    @property
    def APP_NAME(self) -> str:
        return self._app_name

    @property
    def VERSION(self) -> str:
        return self._version

    @property
    def HOME_PAGE(self) -> str:
        return self._home_page

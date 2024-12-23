import tomllib
import os
import sys


class Env:
    def __init__(self):
        self._displayed_app_name = "Screen Tune"
        self._config_path = "./config.json"
        if hasattr(sys, "_MEIPASS"):
            self._toml_path = os.path.join(sys._MEIPASS, "pyproject.toml")
            self._index_path = os.path.join(sys._MEIPASS, "frontend", "index.html")
            self._icon_path = os.path.join(sys._MEIPASS, "icon.png")
        else:
            dirname = os.path.dirname(__file__)
            self._index_path = "http://localhost:4200/"
            self._toml_path = os.path.join(dirname, "../pyproject.toml")
            self._icon_path = os.path.join(dirname, "assets", "icon.png")
        with open(self._toml_path, "rb") as f:
            self._pyproject_data = tomllib.load(f)
        self._app_name = self._pyproject_data["project"]["name"]
        self._version = self._pyproject_data["project"]["version"]
        self._home_page = self._pyproject_data["project"]["urls"]["Homepage"]
        
    @property
    def CONFIG_PATH(self) -> str:
        return self._config_path
    
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
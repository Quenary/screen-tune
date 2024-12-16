import json
import os.path
import copy
from rx.subject.behaviorsubject import BehaviorSubject
from rx.operators import map, skip, debounce
from rx.core import Observable
from typing import TypedDict, List

class ConfigDict(TypedDict):
    checkUpdates:bool
    launchMinimized: bool
    displays: List[str]
    applications: dict

class Config:
    def __init__(self):
        self.__configPath: str = "./config.json"
        self.__defaultConfig: ConfigDict = {
            "checkUpdates": True,
            "launchMinimized": False,
            "displays": [],
            "applications": {},
        }
        config = copy.deepcopy(self.__defaultConfig)
        if os.path.isfile(self.__configPath):
            data = self.__read_config()
            for key in config:
                config[key] = data.get(key, config[key])
        else:
            self.__write_config(config)

        self.__config_subject: BehaviorSubject[ConfigDict] = BehaviorSubject(config)
        self.__config_save_subscription = self.__config_subject.pipe(
            skip(1), debounce(1)
        ).subscribe(lambda cfg: self.__write_config(cfg))

    def __del__(self):
        self.__config_save_subscription.dispose()

    def __read_config(self) -> ConfigDict:
        try:
            with open(self.__configPath, "r") as file:
                return json.load(file)
        except:
            return {}

    def __write_config(self, config: ConfigDict):
        with open(self.__configPath, "w+") as file:
            data = json.dumps(config)
            file.write(data)
            file.flush()

    def get_config(self) -> ConfigDict:
        """Get app configuration dictionary. Immutable."""
        return copy.deepcopy(self.__config_subject.value)

    def set_config(self, config: ConfigDict):
        """Set app configuration dictionary"""
        self.__config_subject.on_next(config)

    def update_config(self, partial_config: ConfigDict):
        """Partial update of app configuration"""
        config = copy.deepcopy(self.__config_subject.value)
        for key in partial_config:
            if key in config:
                config[key] = partial_config[key]
        self.__config_subject.on_next(config)

    def observe_config(self) -> Observable:
        """Obsere app configuration. Immutable."""
        return self.__config_subject.pipe(map(lambda v: copy.deepcopy(v)))

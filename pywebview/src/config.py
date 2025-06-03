import json
import copy
from rx.subject.behaviorsubject import BehaviorSubject
from rx.operators import map, skip, debounce
from rx.core import Observable
from typing import TypedDict, List


class ConfigDict(TypedDict):
    """Configuration dictionary"""

    checkUpdates: bool
    launchMinimized: bool
    displays: List[str]
    applications: dict
    isWorkerActive: bool
    logLevel: int


class Config:
    def __init__(self, config_path):
        self._config_path = config_path
        config = self._default_config
        try:
            data = self._read_config()
            for key in config:
                config[key] = data.get(key, config[key])
        except Exception as e:
            print(f"Error reading config file: {e}")
            self._write_config(config)

        self._config_subject: BehaviorSubject[ConfigDict] = BehaviorSubject(config)
        self._config_save_subscription = self._config_subject.pipe(
            skip(1), debounce(1)
        ).subscribe(lambda cfg: self._write_config(cfg))

    @property
    def _default_config(self) -> ConfigDict:
        return {
            "checkUpdates": True,
            "launchMinimized": False,
            "displays": [],
            "applications": {},
            "isWorkerActive": True,
            "logLevel": 30
        }

    def __del__(self):
        self._config_save_subscription.dispose()

    def _read_config(self) -> ConfigDict:
        with open(self._config_path, "r") as file:
            return json.load(file)

    def _write_config(self, config: ConfigDict):
        with open(self._config_path, "w+") as file:
            data = json.dumps(config)
            file.write(data)
            file.flush()

    def get_config(self) -> ConfigDict:
        """Get app configuration dictionary. Immutable."""
        return copy.deepcopy(self._config_subject.value)

    def set_config(self, config: ConfigDict):
        """Set app configuration dictionary"""
        self._config_subject.on_next(config)

    def update_config(self, partial_config: ConfigDict):
        """Partial update of app configuration"""
        config = copy.deepcopy(self._config_subject.value)
        for key in partial_config:
            if key in config:
                config[key] = partial_config[key]
        self._config_subject.on_next(config)

    def observe_config(self) -> Observable:
        """Obsere app configuration. Immutable."""
        return self._config_subject.pipe(map(lambda v: copy.deepcopy(v)))

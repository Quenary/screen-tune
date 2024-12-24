from platform_api import PlatformApi
from config import Config, ConfigDict
from rx import interval, combine_latest
from rx.operators import throttle_first
from rx.disposable.disposable import Disposable
from rx.subject.behaviorsubject import BehaviorSubject


class EventHandler:
    def __init__(self, platform_api: PlatformApi, config: Config):
        self._platform_api = platform_api
        self._config = config
        self._interval = 1
        self._default_brightness: float = 0.5
        self._default_contrast: float = 0.5
        self._default_gamma: float = 1.0
        self._active_window_process = None
        self._interval_subscription: Disposable = None
        self._live_preview_subscription: Disposable = None
        self._config_subscription: Disposable = None
        self._live_preview_active = BehaviorSubject(False)
        self._live_preview_values = BehaviorSubject(None)
        self._running = BehaviorSubject(False)

    def stop(self):
        if self._interval_subscription is not None:
            self._interval_subscription.dispose()
        if self._live_preview_subscription is not None:
            self._live_preview_subscription.dispose()
        if self._config_subscription is not None:
            self._config_subscription.dispose()
        self._running.on_next(False)

    def start(self):
        self.stop()
        self._interval_subscription = interval(self._interval).subscribe(
            lambda x: self._on_next_interval()
        )
        self._live_preview_subscription = (
            combine_latest(self._live_preview_active, self._live_preview_values)
            .pipe(throttle_first(0.1))
            .subscribe(lambda x: self._on_next_live_preview(x[0], x[1]))
        )
        self._config_subscription = self._config.observe_config().subscribe(
            lambda x: self._on_next_config()
        )
        self._running.on_next(True)

    def _on_next_interval(self):
        live_preview_active = self._live_preview_active.value
        if live_preview_active is True:
            return
        config: ConfigDict = self._config.get_config()
        if config is None:
            return
        active_window_process = self._platform_api.get_active_window_process_name()
        if self._active_window_process == active_window_process:
            return
        self._active_window_process = active_window_process
        displays = config["displays"]
        config_applications: dict = config.get("applications", {})
        config_applications_entry: dict = config_applications.get(
            self._active_window_process, {}
        )
        self._set_values(
            displays,
            config_applications_entry.get("brightness"),
            config_applications_entry.get("contrast"),
            config_applications_entry.get("gamma"),
        )

    def _on_next_live_preview(self, active: bool, values: dict):
        if active is not True:
            return
        config = self._config.get_config()
        displays = config.get("displays")
        values = values if values is not None else {}
        self._set_values(
            displays,
            values.get("brightness"),
            values.get("contrast"),
            values.get("gamma"),
        )

    def _on_next_config(self):
        self._active_window_process = None

    def _set_values(
        self,
        displays: list,
        brightness: float = None,
        contrast: float = None,
        gamma: float = None,
    ):
        if displays is None or len(displays) == 0:
            return
        try:
            brightness = (
                brightness if brightness is not None else self._default_brightness
            )
            contrast = contrast if contrast is not None else self._default_contrast
            gamma = gamma if gamma is not None else self._default_gamma
            for display in displays:
                self._platform_api.set_display_settings(
                    display, brightness, contrast, gamma
                )
        except:
            pass

    def set_live_preview_active(self, active: bool):
        self._live_preview_active.on_next(active)
        self._active_window_process = None
        if active is False:
            displays = self._config.get_config()["displays"]
            self._set_values(displays)

    def set_live_preview_values(self, values: dict):
        self._live_preview_values.on_next(values)
        
    def is_running(self):
        return self._running.value
    
    def is_running_observer(self):
        return self._running.as_observer()

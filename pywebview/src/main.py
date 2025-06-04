from PIL import Image
from pystray import Icon, Menu, MenuItem
from api import Api
import webbrowser
from platform_api import PLATFORM_API
from config import Config
from env import Env
from event_handler import EventHandler
from multiprocessing import Process, Queue, freeze_support
from main_window import run_webview, InvokeParams
import atexit
import time
import json
from threading import Thread, Event
import logging
import traceback
from multiprocessing import Queue
import json
import logging
import traceback
from translate import TRANSLATIONS

window_request_queue = Queue()
window_response_queue = Queue()
webview_process: Process = None

if __name__ == "__main__":
    freeze_support()

    _env = Env()
    _config = Config(_env.CONFIG_PATH)

    logging.basicConfig(
        level=_config.get_config().get("logLevel"),
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=_env.APP_LOG_PATH,
        encoding="utf-8",
    )
    logging.info("Starting application...")

    clean_up_event = Event()

    _platform_api = PLATFORM_API(_env)
    _event_handler = EventHandler(_platform_api, _config)
    _api = Api(_env, _config, _platform_api, _event_handler, lambda: clean_up())

    def open_main_window():
        """Check if main window is presented and open it if not"""
        try:
            global webview_process
            if webview_process is None or not webview_process.is_alive():
                logging.info(f"Open main window")
                webview_process = Process(
                    target=run_webview,
                    args=(
                        window_request_queue,
                        window_response_queue,
                        _env.DISPLAYED_APP_NAME,
                        _env.WINDOW_LOG_PATH,
                        _env.INDEX_PATH,
                        _env.ICON_PATH,
                        _config.get_config().get("logLevel"),
                    ),
                    name="__window__",
                )
                webview_process.start()
            else:
                logging.debug(f"Main window is already opened")
        except Exception as e:
            logging.error(f"Error opening main window: {e}")
            logging.error(traceback.format_exc())
            pass

    def clean_up():
        """Exit program clean-up"""
        try:
            global clean_up_event
            clean_up_event.set()

            _event_handler.stop()

            global webview_process
            if webview_process is not None and webview_process.is_alive():
                webview_process.terminate()

            icon.stop()
        except Exception as e:
            logging.error(f"Error in clean_up: {e}")
            logging.error(traceback.format_exc())
            pass

    def listen_invokes(stop_event: Event):
        """Listen window invokes and call api methods"""
        while stop_event.is_set() is False:
            if not window_request_queue.empty():
                try:
                    message: InvokeParams = json.loads(window_request_queue.get())
                    result = None
                    if hasattr(_api, message["method"]):
                        method = getattr(_api, message["method"])
                        result = method(*message["args"])
                    window_response_queue.put(json.dumps(result))
                except Exception as e:
                    logging.error(f"Error in listen_invokes: {e}")
                    logging.error(traceback.format_exc())
                    pass
            time.sleep(0.1)

    def check_updates():
        time.sleep(1)
        LATEST_RELEASE = _api.check_latest_release()
        if LATEST_RELEASE.get("update_available", False):
            icon.notify(
                f"{TRANSLATIONS['UPDATE_MESSAGE']}",
                f"{TRANSLATIONS['UPDATE_TITLE']} - {LATEST_RELEASE['latest_version']}",
            )

    atexit.register(clean_up)

    image = Image.open(_env.ICON_PATH)
    menu = Menu(
        MenuItem(_env.DISPLAYED_APP_NAME, None, enabled=False),
        Menu.SEPARATOR,
        MenuItem(TRANSLATIONS["OPEN"], lambda: open_main_window(), default=True),
        MenuItem(
            TRANSLATIONS["PROJECT_PAGE"],
            lambda: webbrowser.open("https://github.com/Quenary/screen-tune"),
        ),
        MenuItem(TRANSLATIONS["EXIT"], lambda: clean_up()),
    )
    icon = Icon(
        _env.DISPLAYED_APP_NAME, image, title=_env.DISPLAYED_APP_NAME, menu=menu
    )

    config = _config.get_config()
    if not config["launchMinimized"]:
        open_main_window()

    if config["isWorkerActive"]:
        _event_handler.start()

    invokes_thread = Thread(target=listen_invokes, args=(clean_up_event,))
    invokes_thread.start()

    if config["checkUpdates"] and icon.HAS_NOTIFICATION:
        check_updates_thread = Thread(target=check_updates)
        check_updates_thread.start()

    icon.run()
    invokes_thread.join()
    if check_updates_thread:
        check_updates_thread.join()

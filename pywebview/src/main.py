from PIL import Image
from pystray import Icon, Menu, MenuItem
from api import Api
import webbrowser
from autorun_manager import AutorunManager
from platform_api import PLATFORM_API
from config import Config
from env import Env
from event_handler import EventHandler
from multiprocessing import Process, Queue
import atexit
import time
import json
from threading import Thread, Event
from main_window import create_main_window, InvokeParams

_env = Env()
_config = Config(_env)
_autorun_manager = AutorunManager(_env)
_platform_api = PLATFORM_API()
_event_handler = EventHandler(_platform_api, _config)
_api = Api(
    _env, _config, _autorun_manager, _platform_api, _event_handler, lambda: clean_up()
)

window_request_queue = Queue()
window_response_queue = Queue()
webview_process: Process = None

clean_up_event = Event()


def open_main_window():
    """Check if main window is presented and open it if not"""
    global webview_process
    if webview_process is None or not webview_process.is_alive():
        webview_process = Process(
            target=create_main_window,
            args=(
                window_request_queue,
                window_response_queue,
                _env.DISPLAYED_APP_NAME,
                _env.INDEX_PATH,
                _env.ICON_PATH,
            ),
        )
        webview_process.start()


def clean_up():
    """Exit program clean-up"""
    global clean_up_event
    clean_up_event.set()
    _event_handler.stop()
    try:
        global webview_process
        if webview_process is not None and webview_process.is_alive():
            webview_process.terminate()
    except Exception as e:
        print(e)
        pass
    icon.stop()


image = Image.open(_env.ICON_PATH)
menu = Menu(
    MenuItem(_env.DISPLAYED_APP_NAME, None, enabled=False),
    Menu.SEPARATOR,
    MenuItem("Open", lambda: open_main_window()),
    MenuItem(
        "Learn more",
        lambda: webbrowser.open("https://github.com/Quenary/screen-tune"),
    ),
    MenuItem("Exit", lambda: clean_up()),
)
icon = Icon(_env.DISPLAYED_APP_NAME, image, menu=menu)


def listen_invokes(stop_event: Event):
    """Listen window invokes and call api methods"""
    while stop_event.is_set() is False:
        if not window_request_queue.empty():
            message: InvokeParams = json.loads(window_request_queue.get())
            result = None
            if hasattr(_api, message["method"]):
                method = getattr(_api, message["method"])
                result = method(*message["args"])
            window_response_queue.put(json.dumps(result))
        time.sleep(0.1)


if __name__ == "__main__":
    config = _config.get_config()
    if not config["launchMinimized"]:
        open_main_window()

    if config["isWorkerActive"]:
        _event_handler.start()

    invokes_thread = Thread(target=listen_invokes, args=(clean_up_event,))
    invokes_thread.start()

    atexit.register(clean_up)
    icon.run()

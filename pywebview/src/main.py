from PIL import Image
from pystray import Icon, Menu, MenuItem
import webview
from api import Api
import webbrowser
from autorun_manager import AutorunManager
from gdi32_wrapper import Gdi32Wrapper
from config import Config
from env import Env
from event_handler import EventHandler
from multiprocessing import Process
import atexit
from darkdetect import isDark

_env = Env()
_config = Config(_env)
_autorun_manager = AutorunManager(_env)
_gdi32_wrapper = Gdi32Wrapper()
_event_handler = EventHandler(_gdi32_wrapper, _config)
_event_handler.start()
_api = Api(_env, _config, _autorun_manager, _event_handler, lambda: clean_up())


def start_webview():
    """Create and open main window"""
    webview.create_window(
        _env.DISPLAYED_APP_NAME,
        _env.INDEX_PATH,
        js_api=_api,
        width=960,
        height=720,
        min_size=(640, 480),
        background_color="#000000" if isDark() else "#ffffff",
    )
    webview.start(icon=_env.ICON_PATH, debug=True)


def icon_on_open(icon, item):
    global webview_process
    if webview_process is None or not webview_process.is_alive():
        webview_process = Process(target=start_webview)
        webview_process.start()


def icon_on_exit(icon, item):
    clean_up()


image = Image.open(_env.ICON_PATH)
menu = Menu(
    MenuItem(_env.DISPLAYED_APP_NAME, None, enabled=False),
    MenuItem("Open", icon_on_open),
    MenuItem(
        "Learn more",
        lambda: webbrowser.open("https://github.com/Quenary/screen-tune"),
    ),
    MenuItem("Exit", icon_on_exit),
)
icon = Icon(_env.DISPLAYED_APP_NAME, image, menu=menu)


def clean_up():
    """Exit program clean-up"""
    _event_handler.stop()
    try:
        global webview_process
        if webview_process is not None and webview_process.is_alive():
            webview_process.terminate()
    except Exception as e:
        print(e)
        pass
    icon.stop()


if __name__ == "__main__":
    global webview_process
    if not _config.get_config()["launchMinimized"]:
        webview_process = Process(target=start_webview)
        webview_process.start()

    atexit.register(clean_up)
    try:
        icon.run()
    except KeyboardInterrupt:
        clean_up()

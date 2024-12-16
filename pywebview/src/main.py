from PIL import Image
from pystray import Icon, Menu, MenuItem
import webview
from api import Api
import webbrowser
from autorun import Autorun
from config import Config
from multiprocessing import Process
import atexit

icon_path = "../screen-tune.png"
app_name = "Screen Tune"
debug = True

_config = Config()
_autorun = Autorun()
_api = Api(_config, _autorun)

def start_webview():
    """Create and open main window"""
    webview.create_window(app_name, "http://localhost:4200/", js_api=_api)
    webview.start()

def on_open(icon, item):
    global webview_process
    if webview_process is None or not webview_process.is_alive():
        webview_process = Process(target=start_webview)
        webview_process.start()

def on_exit(icon, item):
    clean_up()

image = Image.open(icon_path)
menu = Menu(
    MenuItem(app_name, None, enabled=False),
    MenuItem("Open", on_open),
    MenuItem(
        "Learn more",
        lambda: webbrowser.open("https://github.com/Quenary/screen-tune"),
    ),
    MenuItem("Exit", on_exit),
)
icon = Icon(app_name, image, menu=menu)
        
def clean_up():
    """Exit program clean-up"""
    try:
        global webview_process
        if webview_process is not None and webview_process.is_alive():
            webview_process.terminate()
    except:
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

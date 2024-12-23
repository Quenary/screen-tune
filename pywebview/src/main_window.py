from multiprocessing import Queue
from typing import TypedDict
import json
import webview
from darkdetect import isDark


class InvokeParams(TypedDict):
    name: str
    args: list


def create_main_window(
    request_queue: Queue,
    response_queue: Queue,
    displayed_app_name: str,
    index_path: str,
    icon_path: str,
):
    """Create and open main window"""

    def invoke(method, *args):
        message: InvokeParams = {"method": method, "args": args}
        request_queue.put(json.dumps(message))
        response = response_queue.get()
        return json.loads(response)

    window = webview.create_window(
        displayed_app_name,
        index_path,
        width=960,
        height=720,
        min_size=(640, 480),
        background_color="#000000" if isDark() else "#ffffff",
    )
    window.expose(invoke)
    webview.start(icon=icon_path, debug=True)

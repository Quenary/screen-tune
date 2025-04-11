from multiprocessing import Queue
from typing import TypedDict
import json
import webview
from darkdetect import isDark
import logging
import traceback

class InvokeParams(TypedDict):
    name: str
    args: list

def run_webview(
    request_queue: Queue,
    response_queue: Queue,
    displayed_app_name: str,
    index_path: str,
    icon_path: str,
):
    """Create and open main window"""
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="window.log",
            encoding="utf-8",
        )
        logging.info("Creating main window")

        logging.debug("run_webview. define invoke function.")
        def invoke(method, *args):
            message: InvokeParams = {"method": method, "args": args}
            request_queue.put(json.dumps(message))
            response = response_queue.get()
            return json.loads(response)

        logging.debug("run_webview. webview.create_window.")
        logging.debug(f"parameters: displayed_app_name: {displayed_app_name}")
        logging.debug(f"parameters: index_path: {index_path}")
        logging.debug(f"parameters: icon_path: {icon_path}")
        window = webview.create_window(
            displayed_app_name,
            index_path,
            width=960,
            height=720,
            min_size=(640, 480),
            background_color="#000000" if isDark() else "#ffffff",
            # frameless=True # not resizable
        )

        logging.debug("run_webview. window.expose(invoke).")
        window.expose(invoke)

        logging.debug("run_webview. webview.start.")
        webview.start(icon=icon_path, debug=False)
    except Exception as e:
        logging.error(f"run_webview. Exception: {e}")
        logging.error(traceback.format_exc())
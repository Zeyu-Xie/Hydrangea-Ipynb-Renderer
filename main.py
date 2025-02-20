import os
from Menu import main_menu
from Windows import Window, main_windows
from Config import main_config
import webview
import sys
import threading


def terminate():
    for window in webview.windows:
        window.destroy()


def main(hook):

    Window.terminate_hook = hook

    ipynb_path_list = sys.argv[1:]
    for ipynb_path in ipynb_path_list:
        main_windows.append(
            Window(
                title=os.path.basename(ipynb_path),
                ipynb_path=ipynb_path,
            )
        )


if __name__ == "__main__":

    webview.create_window(
        "Blank Page",
        html="about:blank",
        hidden=True,
    )
    threading.Thread(target=main, daemon=True, args=(terminate,)).start()
    webview.start(
        menu=main_menu.menu_items(), debug=main_config.config["develop"]["debug"]
    )

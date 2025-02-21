import os
from Menu import main_menu
from Windows import Window, main_windows
from Config import main_config
import webview
import sys
import threading


def main():

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
    threading.Thread(target=main).start()
    webview.start(menu=main_menu.menu_items(), debug=main_config.config["develop"]["debug"])

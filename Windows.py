import webview

from Ipynb_Converter import main_ipynb_converter
from Config import main_config

class Window:

    instances = {}

    def __init__(self, title, ipynb_path):
        self.title = title
        self.ipynb_path = ipynb_path
        self.window = webview.create_window(
            title,
            html=main_ipynb_converter.convert(ipynb_path),
            width=main_config.config["window"]["width"],
            height=main_config.config["window"]["height"],
            fullscreen=main_config.config["window"]["full_screen"],
        )
        Window.instances[self.window] = self
        self.window.show()

    def refresh(self):
        self.window.destroy()
        self.window = webview.create_window(
            self.title,
            html=main_ipynb_converter.convert(self.ipynb_path),
            width=main_config.config["window"]["width"],
            height=main_config.config["window"]["height"],
            fullscreen=main_config.config["window"]["full_screen"],
        )
        Window.instances[self.window] = self
        self.window.show()
    
    def close(self):
        if self.window in Window.instances:
            del Window.instances[self.window]
        self.window.destroy()


class Windows:

    def __init__(self):
        self.windows = []

    def append(self, window):
        self.windows.append(window)

    def refresh(self):
        for window in self.windows:
            window.refresh()
    
    def close_current(self):
        webview.active_window().destroy()

    def close(self):
        for window in self.windows:
            window.close()

main_windows = Windows()

__all__ = ["Window", "Windows", "main_windows"]

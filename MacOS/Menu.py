from Config import main_config
from Ipynb_Converter import main_ipynb_converter
from Windows import Window, main_windows
import webview
import webview.menu as wm
import os


class Menu:

    # File - Open
    def __menu_file_open(self):
        window = webview.windows[0]
        file_types = ("Jupyter Notebook (*.ipynb)",)
        result = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        if result:
            for ipynb_path in result:
                main_windows.append(
                    Window(
                        title=os.path.basename(ipynb_path),
                        content=main_ipynb_converter.convert(ipynb_path),
                    )
                )

    # File - Save As...
    def __menu_file_saveAs(self):
        window = Window.instances[webview.active_window()]
        file_types = ("Jupyter Notebook (*.ipynb)",)
        result = window.window.create_file_dialog(
            webview.SAVE_DIALOG,
            file_types=file_types,
            save_filename=os.path.basename(window.ipynb_path),
        )
        if result:
            ipynb_content = open(window.ipynb_path, "r", encoding="utf-8").read()
            with open(result, "w") as file:
                file.write(ipynb_content)

    # File - Export - HTML
    def __menu_file_export_html(self):
        window = Window.instances[webview.active_window()]
        file_types = ("HTML (*.html)",)
        result = window.window.create_file_dialog(
            webview.SAVE_DIALOG,
            file_types=file_types,
            save_filename=f"{os.path.basename(window.ipynb_path)}.html",
        )
        if result:
            with open(result, "w") as file:
                file.write(window.window.html)

    # File - Close Current
    def __menu_file_closeCurrent(self):
        main_windows.close_current()

    # File - Close All
    def __menu_file_closeAll(self):
        main_windows.close()
    
    # File - Print
    def __menu_file_print(self):
        webview.active_window().evaluate_js("window.print()")

    # Style - Content Width
    def __menu_style_contentWidth_(self, percent):
        main_config.config["style"]["content_width"] = percent
        main_config.save()
        main_windows.refresh()

    # Style - Page Space
    def __menu_style_pageSpace_(self, pixel):
        main_config.config["style"]["page_space"] = pixel
        main_config.save()
        main_windows.refresh()

    # Style - Code Wrap
    def __menu_style_codeWrap(self):
        main_config.config["style"]["code_wrap"] = not main_config.config["style"]["code_wrap"]
        main_config.save()
        main_windows.refresh()

    # Style - Allow Text Select
    def __menu_style_allowTextSelect(self):
        main_config.config["style"]["allow_text_select"] = not main_config.config["style"]["allow_text_select"]
        main_config.save()
        main_windows.refresh()

    # Style - Show Scrollbar
    def __menu_style_showScrollbar(self):
        main_config.config["style"]["show_scrollbar"] = not main_config.config["style"]["show_scrollbar"]
        main_config.save()
        main_windows.refresh()

    # Themes
    def __set_themes_as_current(self, theme):
        main_config.config["theme"]["current_theme"] = theme
        main_config.save()
        main_windows.refresh()

    def __menu_themes(self):
        theme_items = []
        for theme in main_config.config["theme"]["theme_list"]:
            theme_items.append(
                wm.MenuAction(
                    os.path.basename(theme).replace(".css", "").capitalize(),
                    lambda theme=theme: self.__set_themes_as_current(theme),
                )
            )
        return theme_items

    # Window - Default Size
    def __menu_window_defaultSize_(self, width, height):
        main_config.config["window"]["width"] = width
        main_config.config["window"]["height"] = height
        main_config.save()
        main_windows.refresh()
    
    # Window - Lock Window Size
    def __menu_window_lockWindowSize(self):
        main_config.config["window"]["lock_window_size"] = not main_config.config["window"]["lock_window_size"]
        main_config.save()
        main_windows.refresh()

    # Window - Minimize
    def __menu_window_minimize(self):
        webview.active_window().minimize()

    # Window - Full Screen
    def __menu_window_fullScreen(self):
        main_config.config["window"]["full_screen"] = not main_config.config["window"]["full_screen"]
        main_config.save()
        main_windows.refresh()

    # Develop - Debug
    def __menu_develop_debug(self):
        main_config.config["develop"]["debug"] = not main_config.config["develop"]["debug"]
        main_config.save()

    # Help - Welcome
    def __menu_about_welcome(self):
        print("Menu: About - Welcome")

    # Help - Version
    def __menu_about_version(self):
        print("Menu: About - Version")

    # Help - License
    def __menu_about_license(self):
        print("Menu: About - License")

    # Help - Source Code
    def __menu_about_source_code(self):
        print("Menu: About - Source Code")

    # Help - Report Issue
    def __menu_about_report_issue(self):
        print("Menu: About - Report Issue")

    # Help - Sponsor
    def __menu_about_sponsor(self):
        print("Menu: About - Sponsor")

    # Help - Contact Us
    def __menu_about_contact(self):
        print("Menu: About - Contact Us")

    # Help - Help
    def __menu_about_help(self):
        print("Menu: About - Help")

    # Help - Feedback
    def __menu_about_feedback(self):
        print("Menu: About - Feedback")


    def menu_items(self):

        return [
            wm.Menu(
                "File",
                [
                    wm.MenuAction("Open", lambda: self.__menu_file_open()),
                    wm.MenuSeparator(),
                    wm.MenuAction("Save As", lambda: self.__menu_file_saveAs()),
                    wm.Menu(
                        "Export As",
                        [
                            wm.MenuAction("Export as HTML", lambda: self.__menu_file_export_html())
                        ],
                    ),
                    wm.MenuSeparator(),
                    wm.MenuAction(
                        "Close File", lambda: self.__menu_file_closeCurrent()
                    ),
                    wm.MenuAction("Close All", lambda: self.__menu_file_closeAll()),
                    wm.MenuSeparator(),
                    wm.MenuAction("Print", lambda: self.__menu_file_print()),
                ],
            ),
            wm.Menu(
                "Style",
                [
                    wm.Menu(
                        "Set Content Width",
                        [
                            wm.MenuAction("60%", lambda: self.__menu_style_contentWidth_(60)),
                            wm.MenuAction("70%", lambda: self.__menu_style_contentWidth_(70)),
                            wm.MenuAction("80%", lambda: self.__menu_style_contentWidth_(80)),
                            wm.MenuAction("90%", lambda: self.__menu_style_contentWidth_(90)),
                            wm.MenuAction("100%", lambda: self.__menu_style_contentWidth_(100)),
                        ],
                    ),
                    wm.Menu(
                        "Set Page Spacing",
                        [
                            wm.MenuAction("Extra Small", lambda: self.__menu_style_pageSpace_(2)),
                            wm.MenuAction("Small", lambda: self.__menu_style_pageSpace_(6)),
                            wm.MenuAction("Medium", lambda: self.__menu_style_pageSpace_(10)),
                            wm.MenuAction("Large", lambda: self.__menu_style_pageSpace_(20)),
                            wm.MenuAction("Extra Large", lambda: self.__menu_style_pageSpace_(36)),
                        ],
                    ),
                    wm.MenuAction("Toggle Code Wrapping", lambda: self.__menu_style_codeWrap()),
                    wm.MenuAction(
                        "Toggle Text Selection",
                        lambda: self.__menu_style_allowTextSelect(),
                    ),
                    wm.MenuAction(
                        "Show Scrollbars",
                        lambda: self.__menu_style_showScrollbar(),
                    ),
                ],
            ),
            wm.Menu("Themes", self.__menu_themes()),
            wm.Menu(
                "Window",
                [
                    wm.Menu(
                        "Set Default Size",
                        [
                            wm.MenuAction("800x600", lambda: self.__menu_window_defaultSize_(800, 600)),
                            wm.MenuAction("1024x768", lambda: self.__menu_window_defaultSize_(1024, 768)),
                            wm.MenuAction("1280x720", lambda: self.__menu_window_defaultSize_(1280, 720)),
                            wm.MenuAction("1366x768", lambda: self.__menu_window_defaultSize_(1366, 768)),
                            wm.MenuAction("1920x1080", lambda: self.__menu_window_defaultSize_(1920, 1080)),
                        ],
                    ),
                    wm.MenuAction("Lock Resize", lambda: self.__menu_window_lockWindowSize()),
                    wm.MenuAction("Minimize", lambda: self.__menu_window_minimize()),
                    wm.MenuAction("Toogle Full Screen", lambda: self.__menu_window_fullScreen())
                ],
            ),
            wm.Menu(
                "Develop",
                [
                    wm.MenuAction("Toggle Debug Mode", lambda: self.__menu_develop_debug())
                ],
            ),
            wm.Menu(
                "Help", 
                [
                    wm.MenuAction("Welcome", lambda: self.__menu_about_welcome()),
                    wm.MenuAction("About Version", lambda: self.__menu_about_version()),
                    wm.MenuAction("View License", lambda: self.__menu_about_license()),
                    wm.MenuAction("View Source Code", lambda: self.__menu_about_source_code()),
                    wm.MenuAction("Report an Issue", lambda: self.__menu_about_report_issue()),
                    wm.MenuAction("Become a Sponsor", lambda: self.__menu_about_sponsor()),
                    wm.MenuAction("Contact Us", lambda: self.__menu_about_contact()),
                    wm.MenuSeparator(),
                    wm.MenuAction("Help", lambda: self.__menu_about_help()),
                    wm.MenuAction("Send Feedback", lambda: self.__menu_about_feedback()),
                ]
            )
        ]


main_menu = Menu()

__all__ = ["main_menu"]

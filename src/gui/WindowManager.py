from pathlib import Path
from tkinter import *

# from gui.modules import ImageLabel, center

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)
IMGS = Path("assets") / "imgs"


class WindowManager:
    """Manages the windows for encryption/decryption."""

    def __init__(self):
        """Initialize the current window."""
        from gui.windows.Window import Window
        from gui.windows.DecryptWindow import DecryptWindow

        self.root = Tk()
        Window(self.root)
        self.win = DecryptWindow(self.root)
        self.win.initialize()

        print(self.win)

        self.splash_screen()
        self.root.mainloop()
        # self.switch(self.mode)

    def splash_screen(self):
        """Construct Splash Screen"""
        # self.title("Pixel Studios")
        # self.geometry(f"{WIN_W}x{WIN_H}")
        # center(self, WIN_W, WIN_H)

        # gif = ImageLabel(self)
        # gif.configure(bd=0, highlightbackground=None)
        # gif.place(relx=0.5, rely=0.43, anchor="center")

        # def loading_animation(root):
        #     """Loading animation circle for the application"""
        #     loading = ImageLabel(root)
        #     loading.configure(bd=0, highlightbackground=None)
        #     loading.place(relx=0.5, rely=0.57, anchor="center")
        #     loading.load(
        #         IMGS / "loading.gif",
        #         False,
        #         lambda: callback(self.create_main_window, [loading, gif]),
        #     )

        # gif.load(IMGS / "title.gif", False, lambda: loading_animation(self))
        # self.configure(background=DARK_GRAY)
        # self.mainloop()

    def switch(self, new):
        """Switches the window to a new window."""
        # self = DecryptWindow

        # self = WindowManager (og)
        self.win.main.destroy()
        # static win

        self.win = new(self)
        self.win.initialize()


# key = 10; -> self.key = set_key(10)

# self.key
# def get_key()
# def set_key()

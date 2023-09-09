# from pathlib import Path
from abc import abstractmethod
from random import choices
from tkinter import *

from backend.typingcolors import TypingColors
from gui.WindowManager import WindowManager
from gui.windows.modules import *


class Window:
    """Blueprint for all windows in the Application"""

    def __init__(self, root: Tk):
        """Initializes variables and window"""
        self.root = root
        self.key = "MUDITH"
        # Creates the window
        pass

    @property
    def key(self):
        """Getter for the Key"""
        return self._key

    @key.setter
    def key(self, k):
        """Setter for the Key"""
        self._key = k
        self.on_key_change(k)

    def initialize(self) -> None:
        """Performs Initialization Action when the window is created"""
        self.menu_bar()

    def status_bar(self) -> None:
        """Bottom Bar"""
        self.key_name = StringVar()
        self.key.set(f"Secret Key: {self.key}")
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        Label(self.root, textvariable=self.key, bg=DARK_GRAY, fg="white").grid(
            row=1, column=0, sticky="w"
        )
        Label(self.root, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )

    def on_key_change(self, key: str) -> None:
        pass

    def menu_bar(self) -> None:
        """Packs the menubar for the application"""
        """
            self = Tk self object
            win = The class method to be called
        """

        layouts = {
            "Import": {"command": self.open, "state": "normal"},
            "Export": {"command": self.export, "state": "normal"},
            "-": "",
            "Set Key": {
                "command": lambda: self.construct_key_editor(self.root),
                "state": "normal",
            },
            "--": "",
            "Encrypt": {
                "dropdown": {
                    "Typing Colors": {
                        "command": self.call_tc,
                        "state": "normal",
                    },
                    "Steganograpy": {"command": self.call_steg, "state": "normal"},
                }
            },
            "Decrypt": {"command": self.call_dc, "state": "disabled"},
        }

        # Main Menu Bar
        menubar = Menu(self.root, tearoff=0, font=("Consolas", 12))

        # Add to menu bars
        for name, data in layouts.items():
            menu = Menu(
                self.root,
                tearoff=0,
                cursor="hand1",
                font=("Consolas", 10),
            )
            if "-" in name:
                menubar.add_separator()
            else:
                if "dropdown" in data.keys():
                    dropdown = data["dropdown"]
                    for label, layout in dropdown.items():
                        menu.add_command(
                            label=label,
                            command=layout["command"],
                            state=layout["state"],
                            activeforeground=WHITE
                            if layout["state"] == "normal"
                            else GRAY,
                            activebackground=GRAY
                            if layout["state"] == "normal"
                            else WHITE,
                        )
                    menubar.add_cascade(
                        label=name,
                        menu=menu,
                        compound="left",
                        activeforeground=WHITE,
                        activebackground=GRAY,
                    )
                else:
                    menubar.add_command(
                        label=name,
                        command=data["command"],
                        state=data["state"],
                        activeforeground=WHITE,
                        activebackground=GRAY,
                    )

        self.root.configure(background=DARK_GRAY, menu=menubar)

    def destroy(self):
        """Performs Cleanup Action when the window exits"""
        self.main.destroy()

    # All Menu Bar Actions
    @abstractmethod
    def open(self):
        """Open method depends on current window context"""
        pass

    @abstractmethod
    def export(self):
        """Export method on current window context"""
        pass

    def construct_key_editor(self, root: Tk):
        """Makes Popup for the user to enter key"""
        self.popup = Toplevel(root, bg=DARK_GRAY)
        self.popup.geometry("350x200")
        self.title = Label(self.popup, bg=DARK_GRAY, fg=WHITE, text="Enter Secret Key")
        self.title.pack()
        self.key_method = Text(
            self.popup, height=1, width=25, padx=2, pady=2, font=("Consolas", 12), bd=0
        )
        self.key_method.pack(pady=30)

        self.error = Label(
            self.popup,
            text="",
            font=("Consolas", 10, "bold"),
            bg=DARK_GRAY,
            fg=BRIGHT_RED,
            pady=2,
        )
        self.error.pack()
        submit = Button(
            self.popup,
            text="Edit Key",
            font=("Consolas", 12, "bold"),
            bg=GREEN,
            fg=WHITE,
            padx=5,
            pady=3,
            cursor="hand2",
            bd=0,
            command=lambda: self.process_key(),
        )
        submit.pack()

    def process_key(self):
        """Handles Key insertion"""
        key = self.key_method.get("1.0", "end-1c")
        if response := valid_key(key):
            # Error Handling in GUI
            self.key_method.config(bg=RED, fg=WHITE)
            self.error.config(fg=RED, text=response)
        else:
            if len(key) == 0:
                key = "".join(choices(PRINTABLE, k=16))
            self.key = key
            self.popup.destroy()

    def call_tc(self):
        """Switches to Typing Colors"""
        from gui.windows.TypingColorsWindow import TypingColorsWindow

        switch(self, TypingColorsWindow)

    def call_steg(self):
        """Switches to Steganography"""
        from gui.windows.SteganographyWindow import SteganographyWindow

        switch(self, SteganographyWindow)

    def call_dc(self):
        """Switches to Decrypt"""
        from windows.DecryptWindow import DecryptWindow

        switch(self, DecryptWindow)

    def switch(self, new):
        """Switches the window to a new window."""
        # self = DecryptWindow

        # self = WindowManager (og)
        self.destroy()

        self.win = new(self)
        self.win.initialize()


def switch(old: object, new: object):
    """Makes new window"""
    root = old.root
    old.main.destroy()

    temp = new(root)
    temp.initialize()

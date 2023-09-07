from tkinter import *
from tkinter import filedialog as fd

from backend.typingcolors import TypingColors
from backend.typingcolors_utils import typingcolors_load
from gui.modules import ImageLabel
from gui.win_steganography import SteganographyWin
# from gui.win_typingcolors import TypingColorsWin

WIN_W, WIN_H = (800, 600)
POP_W, POP_H = (400, 300)
DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"


class GUI(Tk):
    """Main GUI class to interact with the backend"""

    def __init__(self):
        """Initializes variables and window"""
        # Creates the window
        super().__init__()

    def center(self, root: Tk):
        """Centers a tkinter window"""
        root.update_idletasks()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        x = int((width - WIN_W) / 2)
        y = int(
            (height - WIN_H) / 3
        )  # A bit off center to align it well with the taskbar
        root.geometry(f"+{x}+{y}")

    def callback(self, callback: callable, destroy: list[Widget] = None, *args):
        """Callback a function while destroying existing widgets"""
        if (
            len(destroy) > 0
        ):  # Destroy the previous image labels for a fresh home screen application.
            for i in destroy:
                i.destroy()
        callback(*args)

    # function to create the place to write text to create image

    def loading_screen(self):
        """The starting page for the application"""
        self.title("Pixel Studios")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.center(self)

        gif = ImageLabel(self)
        gif.configure(bd=0, highlightbackground=None)
        gif.place(relx=0.5, rely=0.43, anchor="center")

        def loading_animation(root):
            """Loading animation circle for the application"""
            loading = ImageLabel(root)
            loading.configure(bd=0, highlightbackground=None)
            loading.place(relx=0.5, rely=0.57, anchor="center")
            loading.load(
                "assets\\imgs\\loading.gif",
                False,
                lambda: self.callback(self.create_main_window, [loading, gif]),
            )

        gif.load("assets\\imgs\\title.gif", False, lambda: loading_animation(self))
        self.configure(background=DARK_GRAY)
        self.mainloop()

    def create_main_window(self):
        """Creates The Main Window Page for the application"""
        # The Main Input Frame:
        self.main = Frame(self, bg=DARK_GRAY)
        self.main.place(relx=0.5, rely=0.5, anchor="center")
        input = Frame(self.main, bg=DARK_GRAY)
        input.pack()

        label = Label(
            input,
            text="Enter Secret Key:",
            font=("Consolas", 12),
            bg=DARK_GRAY,
            fg=WHITE,
            pady=5,
        )
        label.pack()

        self.key = Text(
            input, height=1, width=25, padx=2, pady=2, font=("Consolas", 12), bd=0
        )
        self.key.pack()

        self.error = Label(
            input,
            text="",
            font=("Consolas", 10, "bold"),
            bg=DARK_GRAY,
            fg=BRIGHT_RED,
            pady=2,
        )
        self.error.pack()

        # Encrypt / Decrypt Buttons Frame:
        buttons = Frame(self.main, background=DARK_GRAY, pady=15)

        # Encrypt OptionMenu
        method = StringVar()
        method.set("Encrypt ▼")
        opts = ["Typing Colors", "Use Masked Image"]
        encrypt = OptionMenu(
            buttons,
            method,
            *opts,
        )
        encrypt.configure(
            font=("Consolas", 12, "bold"),
            bg=RED,
            fg=WHITE,
            padx=5,
            pady=5,
            cursor="hand2",
            indicatoron=0,
            bd=0,
            highlightbackground=RED,
            activeforeground=WHITE,
            activebackground=RED,
        )
        encrypt["menu"].configure(
            font=("Consolas", 10),
            cursor="hand2",
            activebackground=RED,
            activeforeground=WHITE,
            foreground=DARK_GRAY,
        )
        encrypt.grid(row=0, column=0, padx=10, pady=10)
        method.trace("w", lambda *args: self.check_key(True, opts.index(method.get())))

        # Decrypt Button
        decrypt = Button(
            buttons,
            text="Decrypt",
            font=("Consolas", 12, "bold"),
            bg=GREEN,
            fg=WHITE,
            padx=5,
            pady=3,
            cursor="hand2",
            bd=0,
            command=lambda: self.check_key(False),
        )
        decrypt.grid(row=0, column=10, padx=10, pady=10)
        buttons.pack()
        # buttons.place(relx=0.5, rely=0.5, anchor="center")
        self.mainloop()

    def check_key(self, encrypt: bool, mode: int = 0):
        """Checks if key length is between 4 and 24, and then opens the encrypt/decrypt page"""
        key = self.key.get(1.0, "end-1c")
        if 4 <= len(key) <= 24 or len(key) == 0:
            if encrypt:
                self.encrypt(key, mode)
            else:
                self.decrypt(key)
        else:
            self.key.configure(bg=RED, fg=WHITE)
            self.error.configure(text="Key must be between 4 and 24 characters long")

    def encrypt(self, key: str = None, mode: int = 0):
        """Opens the encryption page with the secret key"""
        # Mode 0 is for Typing Colors
        # Mode 1 is for Masked Image
        if mode == 0:
            self.typingColors = TypingColors()
            self.typingColors.set_encryption(key)
            self.callback(TypingColorsWin, [self.main])
            # self.typingColorsWin = TypingColorsWin(self.typingColors)
        else:
            self.steganographyWin = SteganographyWin()

    def decrypt(self, key: str = None):
        """Opens the decryption page with the secret key"""
        # TODO: find out what method used to encrypt here
        method = 0
        if method == 0:  # decrypting typingcolors image
            filename = fd.askopenfilename(
                title="Select Image", filetypes=[("PNG", "*.png")]
            )
            try:
                self.typingColors, decoded_text = typingcolors_load(filename, key)
            except KeyError:  # invalid decryption key
                self.key.configure(bg=RED, fg=WHITE)
                self.error.configure(text="Invalid secret key")
                return
            self.typingColorsWin = TypingColorsWin(self.typingColors)
            self.typingColorsWin.text.delete(1.0, "end")
            self.typingColorsWin.text.insert("end", decoded_text)

# win_typingcolors.py


DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"


class TypingColorsWin(GUI):
    """Window for typingcolors"""

    def __init__(self):
        """Creates the layout"""
        # super().__init__()
        self.create_menu_bar()
        self.typingColors = TypingColors()  # the main backend
        self.file = None  # open files
        self.title("New File - Typing Colors")
        # split layout
        self.text = Text(
            self,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.canvas = Label(self, image=self.typingColors.img_scaled(), bg=DARK_GRAY)
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.text.grid(row=0, column=0, sticky="nsew", rowspan=2)
        self.canvas.grid(row=0, column=1, sticky="ne")
        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        # start the loop
        self._typingcolors_update("")

    def _typingcolors_update(self, prev_txt):
        """Update loop for typingcolours"""
        txt = self.text.get("1.0", "end")
        if txt != prev_txt:  # only update if text changed
            self.typingColors.update(txt)
            img = self.typingColors.img_scaled()
            self.canvas.configure(image=img)
            self.canvas.image = img
            self.info.set(
                f"{len(txt) - 1} characters   |   {self.typingColors.width}px x {self.typingColors.height}px"
            )
        self.after(50, lambda: self._typingcolors_update(txt))

    def new(self):
        """Resets the canvas and text"""
        self.file = None
        self.title("New File - Typing Colors")
        self.text.delete(1.0, "end")
        self.typingColors.update("")

    def open(self):
        """Opens and loads a selected text file"""
        filename = fd.askopenfilename(title="Open", filetypes=[("All", "*.*")])
        if filename:
            content = open(filename, "r").read()
            self.file = filename
            self.title(f"{filename} - Typing Colors")
            self.text.delete(1.0, "end")
            self.text.insert("end", content)
            self.typingColors.update(content)

    def save(self):
        """Saves the current text"""
        if not self.file:  # no file to save to yet
            self.saveas()  # open a file selector then save
        else:
            open(self.file, "w").write(self.text.get(1.0, "end"))

    def saveas(self):
        """Opens a file dialog and saves text to selected file"""
        filename = fd.asksaveasfilename(title="Save As", filetypes=[("All", "*.*")])
        if filename:
            self.file = filename
            self.title(f"{filename} - Typing Colors")
            open(self.file, "w").write(self.text.get(1.0, "end"))

    def export(self):
        """Exports the canvas to a PNG"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("PNG", "*.png")])
        if filename:
            self.typingColors.canvas.save(filename, format="PNG")

    def create_menu_bar(self):
        """Packs the menu bar for the application"""
        layouts = {
            "File": {
                "New": {
                    "command": self.new,
                    "image": "assets\\imgs\\new.png",
                    "accelerator": "Ctrl+N",
                },
                "Open": {
                    "command": self.open,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+O",
                },
                "Save": {
                    "command": self.save,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+S",
                },
                "Save As": {
                    "command": self.saveas,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+Shift+S",
                },
                "Export": {
                    "command": self.export,
                    "image": "assets\\imgs\\save.png",
                    "accelerator": "Ctrl+I",
                },
                "---": "",
                "Exit": {
                    "command": self.destroy,
                    "image": "assets\\imgs\\exit.png",
                    "accelerator": "Alt+F4",
                },
            }
        }

        # Main Menu Bar
        menubar = Menu(self, tearoff=0, font=("Consolas", 12))

        # Add to menu bars
        for label, layout in layouts.items():
            menu = Menu(self, tearoff=0, cursor="hand1", font=("Consolas", 10))
            menubar.add_cascade(label=label, menu=menu)
            for name, data in layout.items():
                if "-" in name:
                    menu.add_separator()
                else:
                    menu.add_command(
                        label=name,
                        compound="left",
                        command=data["command"],
                        accelerator=data["accelerator"],
                        activeforeground=WHITE,
                        activebackground=GRAY,
                    )
        self.configure(background=DARK_GRAY, menu=menubar)

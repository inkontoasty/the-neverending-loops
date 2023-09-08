from tkinter import *
from itertools import count, cycle
from tkinter import filedialog as fd
from gui.win_decrypt import DecryptWin
import backend

from PIL import Image, ImageTk

DARK_GRAY, GRAY = "#222831", "#393E46"
AQUA, WHITE = "#00ADB5", "#EEEEEE"
RED, GREEN = "#cd0000", "#1BAA4A"
BRIGHT_RED = "#ff0000"

KEY = ""

PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t"


class ImageLabel(Label):
    """
    A Label that displays images, and plays them if they are gifs

    Source: https://pythonprogramming.altervista.org/animate-gif-in-tkinter/
    The code was modified to fit the needs of this application
    """

    def load(self, im: str, repeat: bool = False, after_exec=None):
        """Loads an image"""
        self.im = im
        self.after_exec = after_exec
        im = Image.open(im)
        self.og_frames = []
        try:
            for i in count(1):
                self.og_frames.append(ImageTk.PhotoImage(im))
                im.seek(i)
        except EOFError:
            pass
        self.frames = (
            cycle(self.og_frames) if repeat else iter(self.og_frames)
        )  # If img needs to be cycled
        try:
            self.delay = im.info["duration"]
        except Exception:
            self.delay = 100
        if len(self.og_frames) == 1:  # If image is not a gif
            self.config(image=next(self.frames))
        else:  # If image is gif
            self.next_frame()

    def unload(self):
        """Unloads the iamge"""
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        """Updates the image frame (if gif)"""
        if self.frames:
            try:
                self.config(image=next(self.frames))
                self.after(self.delay, self.next_frame)
            except StopIteration:
                if self.after_exec:
                    self.after_exec()


def center(root: Tk, WIN_W: int, WIN_H: int):
    """Centers a tkinter window"""
    root.update_idletasks()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x = int((width - WIN_W) / 2)
    y = int(
        (height - WIN_H) / 3
    )  # A bit off center to align it well with the taskbar
    root.geometry(f"+{x}+{y}")


def dynamic_menu_bar(root: Tk, win: classmethod):
    """Packs the menubar for the application"""
    """
        root = Tk root object
        win = The class method to be called
    """
    from gui.win_steganography import SteganographyWin
    from gui.win_typingcolors import TypingColorsWin

    layouts = {
        "Import": {
            "command": win.open,
            "accelerator": "Ctrl+O",
            "state": "normal"
        },
        "Export": {
            "command": win.export,
            "accelerator": "Ctrl+I",
            "state": "normal"
        },
        "Set Key": {
            "command": edit_key,
            "accelerator": "Ctrl+K",
            "state": "normal"
        },
        "--": "",
        "Encrypt": {
            "dropdown": {
                "Typing Colors": {
                    "command": lambda: TypingColorsWin.__init__(TypingColorsWin),
                    "accelerator": "Ctrl+T",
                    "state": "disabled" if win.__class__.__name__ == "TypingColorsWin" else "active"
                },
                "Steganograpy": {
                    "command": lambda: SteganographyWin.__init__(SteganographyWin),
                    "accelerator": "Ctrl+S",
                    "state": "disabled" if win.__class__.__name__ == "SteganographyWin" else "active"
                }
            }
        },
        "Decrypt": {
            "command": lambda: switch_to_decrypt(win),
            "accelerator": "Ctrl+D",
            "state": "disabled" if win.__class__.__name__ == "DecryptWin" else "active"
        }
    }

    # Main Menu Bar
    menubar = Menu(root, tearoff=0, font=("Consolas", 12))

    # Add to menu bars
    for name, data in layouts.items():
        menu = Menu(
            root,
            tearoff=0,
            cursor="hand1",
            font=("Consolas", 10),
        )
        if "-" in name:
            menubar.add_separator()
        else:
            try:
                if dropdown := data["dropdown"]:
                    for label, layout in dropdown.items():
                        menu.add_command(
                            label=label,
                            command=layout["command"],
                            accelerator=layout["accelerator"],
                            state=layout["state"],
                            activeforeground=WHITE if layout["state"] == "active" else GRAY,
                            activebackground=GRAY if layout["state"] == "active" else WHITE,
                        )
                    menubar.add_cascade(
                        label=name,
                        menu=menu,
                        compound="left",
                        activeforeground=WHITE,
                        activebackground=GRAY,
                    )
            except KeyError:
                menubar.add_command(
                    label=name,
                    command=data["command"],
                    accelerator=data["accelerator"],
                    state=data["state"],
                    activeforeground=WHITE,
                    activebackground=GRAY,
                )
    root.configure(background=DARK_GRAY, menu=menubar)


def callback(callback: callable, destroy: list[Widget] = None, *args):
    """Callback a function while destroying existing widgets"""
    if (
        len(destroy) > 0
    ):  # Destroy the previous image labels for a fresh home screen application.
        for i in destroy:
            i.destroy()
    callback(*args)


def edit_key(root: Tk, after_exec: callable = None):
    """Opens up an edit key window"""
    print(after_exec)
    root.popup = Toplevel(root, bg=DARK_GRAY)
    root.popup.geometry("350x200")
    root.key_method = Text(
        root.popup, height=1, width=25, padx=2, pady=2, font=("Consolas", 12), bd=0
    )
    root.key_method.pack(pady=30)

    root.error = Label(
        root.popup,
        text="",
        font=("Consolas", 10, "bold"),
        bg=DARK_GRAY,
        fg=BRIGHT_RED,
        pady=2,
    )
    root.error.pack()
    ok = Button(
        root.popup,
        text="Edit Key",
        font=("Consolas", 12, "bold"),
        bg=GREEN,
        fg=WHITE,
        padx=5,
        pady=3,
        cursor="hand2",
        bd=0,
        command=lambda: _valid_key(root, root.key_method.get("1.0", "end-1c"),
                                   root.key_method, root.error, True, after_exec)
    )
    print(after_exec)
    ok.pack()


def _valid_key(root: Tk, key: str, key_method: Text, error: Label,
               switch_to_decrypt: bool = False, after_exec: callable = None):
    """Checks if key is valid"""
    global KEY
    status = False
    if not (4 <= len(key) <= 24 or len(key) == 0):
        key_method.configure(bg=RED, fg=WHITE)
        error.configure(text="Key must be between 4 and 24 characters long")
    elif " " in key:
        key_method.configure(bg=RED, fg=WHITE)
        error.configure(text="Key can't contain whitespaces")
    else:
        status = True
    KEY = key
    if after_exec:
        if switch_to_decrypt:  # checks if the decrypt window needs to open
            after_exec(root, key_method, error)
        else:
            after_exec()
    return status


def switch_to_decrypt(win):
    """Switches the window to the decrypt window"""
    filename = fd.askopenfilename(
        title="Select Image", filetypes=[("PNG", "*.png")]
    )

    edit_key(win, lambda: decrypt(filename, KEY))


def decrypt(filename, key: str, root: Tk = None, key_method: Text = None, error: Label = None):
    """Opens the decryption page with the secret key"""
    # TODO: find out what method used to encrypt here
    # decrypting typingcolors image
    try:
        typingColors, decoded_text = backend.utils.decrypt(filename, key)
    except KeyError:  # invalid decryption key
        key_method.configure(bg=RED, fg=WHITE)
        error.configure(text="Invalid secret key")
        return

    callback(
        lambda: DecryptWin(root, typingColors, decoded_text, key).pack(expand=True, fill='both'), []
    )

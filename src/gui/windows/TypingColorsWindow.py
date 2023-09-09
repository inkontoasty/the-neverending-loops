from tkinter import *
from tkinter import filedialog as fd

from backend.typingcolors import TypingColors
from gui.modules import DARK_GRAY
from gui.windows.Window import Window


class TypingColorsWindow(Window):
    """Window for the Typing Colors Game"""

    def __init__(self, root: Tk):
        self.root = root
        self.main = Frame(self.root, bg=DARK_GRAY)
        self.typingColors = TypingColors()  # the main backend
        self.key_name = StringVar()
        super().__init__(self.root)
        super().initialize()

    def initialize(self):
        """Creates the window and all of its widgets"""
        self.root.title("New File - Typing Colors")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1, minsize=280)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0, minsize=25)
        self.root.bind("<Configure>", self.updatecanvas)

        self.typingColors.set_key(self.key)
        self.file = None  # open files
        # split layout
        self.text = Text(
            self.main,
            width=30,
            height=16,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        self.canvas = Label(
            self.main, image=self.typingColors.img_scaled(), bg=DARK_GRAY
        )
        self.key_name.set(f"Secret Key: {self.key}")
        self.info = StringVar()
        self.info.set("0 characters   |   8px x 9px")
        self.text.pack(side="left", expand=True, fill="both", anchor="w")
        self.canvas.pack(side="right", fill="both", anchor="e")
        self.main.grid(row=0, column=0, columnspan=2, sticky="nsew")
        Label(self.root, textvariable=self.key_name, bg=DARK_GRAY, fg="white").grid(
            row=1, column=0, sticky="w"
        )
        Label(self.root, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        self._typingcolors_update("")

    def _typingcolors_update(self, prev_txt: str):
        """Update loop for typingcolours"""
        txt = self.text.get("1.0", "end")
        if txt != prev_txt:  # only update if text changed
            self.typingColors.update(txt)
            self.updatecanvas()
            self.info.set(
                f"{len(txt) - 1} characters   |   {self.typingColors.width}px x {self.typingColors.height}px"
            )
        self.root.after(50, lambda: self._typingcolors_update(txt))

        # def updatecanvas(self, event=None):
        #     """Updates the canvas to fill the screen"""
        #     sf = max(1, (self.grid_bbox(0, 0)[3]) // self.typingColors.ar_height)
        #     img = self.typingColors.img_scaled(int(sf))
        #     self.canvas.configure(
        #         image=img,
        #         width=self.typingColors.ar_width * sf,
        #         height=self.typingColors.ar_height * sf,
        #     )
        #     self.canvas.image = img

    def updatecanvas(self, event=None):
        """Updates the canvas to fill the screen"""
        sf = max(1, (self.root.grid_bbox(0, 0)[3]) // self.typingColors.ar_height)
        img = self.typingColors.img_scaled(int(sf))
        self.canvas.configure(image=img, width=self.typingColors.ar_width*sf, height=self.typingColors.ar_height*sf)
        self.canvas.image = img

    def on_key_change(self, key: str) -> None:
        """Called when the key is changed"""
        self.typingColors.set_key(key)
        self.key_name.set(f"Secret Key: {key}")

    def open(self):
        """Opens and loads a selected text file"""
        filename = fd.askopenfilename(title="Open", filetypes=[("All", "*.*")])
        if filename:
            content = open(filename, "r").read()
            self.file = filename
            self.winfo_toplevel().title(f"{filename} - Typing Colors")
            self.text.delete(1.0, "end")
            self.text.insert("end", content)
            self.typingColors.update(content)

    def export(self):
        """Exports the canvas to a PNG"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("PNG", "*.png")])
        if filename:
            self.typingColors.save_as(filename + ".png")


TypingColors
from tkinter import *
from tkinter import filedialog as fd

from PIL import ImageTk
from PIL.Image import BOX, fromarray

from backend.typingcolors import TypingColors
from backend.utils import get_img_mode, try_decrypt
from gui.modules import *


class DecryptWin(Frame):
    """Window for decryption"""

    def __init__(self, root, filename):
        """Creates the layout"""
        # identify mode and set image

        decoded_text = ""
        self.filename = filename
        self.root = root
        img, mode = get_img_mode(filename)

        if mode == "Typing Colors":
            self.mode = "Typing Colors"
            self.image = (
                img.convert("RGBA")
                if img
                else Image.new("RGBA", self.size, (0, 0, 0, 0))
            )
            self.ar_width, self.ar_height = (8, 9)
        else:
            self.mode = "Steganography"
            self.image = img
            # self.image = fromarray(object.input_image)

        # create window
        super().__init__(root, bg=DARK_GRAY)
        dynamic_menu_bar(root, self)
        root.title(f"Decrypted - {self.mode}")
        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, minsize=280)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=25)

        self.file = None  # open files
        # split layout
        self.mainframe = Frame(self, bg=DARK_GRAY)
        self.text = Text(
            self.mainframe,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg="white",
            font=("Consolas", 14),
        )
        # self.text.insert("end", decoded_text)
        # self.text.configure(state="disabled")

        # TODO: ADD ERROR INFO HERE
        self.canvas = Label(
            self.mainframe, image=ImageTk.PhotoImage(self.image), bg=DARK_GRAY
        )
        self.key = StringVar()
        self.key.set(f"Secret Key: {root.key} | (Click to Copy)")

        self.info = StringVar()
        self.info.set(
            f"{len(decoded_text)} characters   |   {self.image.width}px x {self.image.height}px"
        )
        self.text.pack(side="right", expand=True, fill="both", anchor="ne")
        self.canvas.pack(side="left", anchor="w")
        self.mainframe.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.key_status = Label(self, textvariable=self.key, bg=DARK_GRAY, fg="white")
        self.key_status.grid(row=1, column=0, sticky="w")
        self.key_status.bind("<Button-1>", self.copy_key_to_clipboard)

        Label(self, textvariable=self.info, bg=DARK_GRAY, fg="white").grid(
            row=1, column=1, sticky="e"
        )
        root.bind("<Configure>", self.updatecanvas)
        # PACK
        self.pack(expand=True, fill="both")

        # TODO: START DECODING IMG HERE....
        # DECODING CODE STARTS
        object, decoded_text, decoded_successfully = try_decrypt(filename, root.key)
        print(f"{decoded_text=}")
        self.object = object
        self.success = decoded_successfully

        if not decoded_successfully:
            decoded_text = "FAILED TO DECODE WITH KEY !\nTRY ANOTHER KEY !"
            self.text.insert("end", decoded_text)
            self.text.config(state="disabled", bg=RED, fg="#000")
        else:
            self.text.insert("end", decoded_text)
            self.text.configure(state="disabled")

        self.ar_width, self.ar_height = object.ar_width, object.ar_height = (8, 9)

    def copy_key_to_clipboard(self, _event):
        """Copies key used to encrypt images to the clipboard"""
        # Copying to clipboard
        self.clipboard_clear()
        self.clipboard_append(self.root.key)
        # Updating UI
        self.key.set(f"Secret Key: {self.root.key} | (Copied)")
        self.root.after(
            2000, lambda: self.key.set(f"Secret Key: {self.root.key} | (Click to Copy)")
        )

    def updatecanvas(self, event=None):
        """Updates the canvas to fill the screen"""
        w, h = self.mainframe.winfo_width() // 2, self.mainframe.winfo_height()
        if w * h < 100:  # not rendered yet
            w, h = 100, 100
        if self.mode == "Steganography":
            new = self.image.copy()
            new.thumbnail((w, h), BOX)
            img = ImageTk.PhotoImage(new)
        else:  # image smaller than win
            sf = max(1, (self.grid_bbox(0, 0)[3]) // self.object.ar_height)
            img = self.object.img_scaled(int(sf), self.root.winfo_width())
        self.canvas.configure(image=img, width=w, height=h)
        self.canvas.image = img

    def open(self):
        """Opens and loads a selected image file"""
        self.root.decrypt(self.root.key)

    def export(self):
        """Exports the decrypted text to a file"""
        filename = fd.asksaveasfilename(title="Export As", filetypes=[("TXT", "*.txt")])
        if filename:
            open(filename, "w").write(self.text.get(1.0, "end"))

    def idk(self, key):
        object, decoded_text, decoded_successfully = try_decrypt(self.filename, key)
        print(f"{decoded_text=}")
        self.object = object
        self.success = decoded_successfully

        self.text.config(state="enabled")
        if not decoded_successfully:
            decoded_text = "FAILED TO DECODE WITH KEY !\nTRY ANOTHER KEY !"
            self.text.insert("end", decoded_text)
            self.text.config(state="disabled", bg=RED, fg="#000")
        else:
            self.text.insert("end", decoded_text)
            self.text.configure(state="disabled")

        self.ar_width, self.ar_height = object.ar_width, object.ar_height = (8, 9)

    def edit_key(self):
        """Edits decryption key"""
        key_popup(self.root, lambda: self.idk(self.root.key))
        # TODO: RECODE here...

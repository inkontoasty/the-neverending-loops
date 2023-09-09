import tkinter.filedialog as fd
from tkinter import *

from backend import utils
from gui.windows.modules import *
from gui.windows.Window import Window

# from tkinter import ttk


class DecryptWindow(Window):
    """Window for the Decrypt Game"""

    def __init__(self, root: Tk):
        """Initialize the window"""
        self.root = root
        self.main = Frame(self.root, bg=DARK_GRAY)
        super().__init__(self.root)
        super().initialize()

    def initialize(self):
        """Creates the window and all of its widgets"""
        self.root.title("Decrypt - Pixel Studios")
        self.root.geometry("800x600")
        frame1 = Frame(self.main, bg=DARK_GRAY)
        frame2 = Frame(self.main, bg=DARK_GRAY)
        self.text = Text(
            frame2,
            width=30,
            height=15,
            bg=DARK_GRAY,
            fg=WHITE,
            padx=3,
            pady=3,
            font=("Consolas", 12),
        )
        self.text.insert("1.0", "Edit your key from the Set Key Option")
        self.text.config(state=DISABLED)
        # separator = ttk.Separator(self.main, orient="vertical")
        # separator.place(relx=0.47, rely=0, relwidth=0.2, relheight=1)

        self.canvas = Label(
            frame1,
            bg=DARK_GRAY,
            fg=WHITE,
            text="No image selected\nSelect an image from the Import Option",
        )
        self.canvas.pack()
        self.text.pack()

        # self.canvas.grid(row=0, column=0, sticky="nsew")
        # self.text.grid(row=0, column=1, sticky="nsew")

        frame1.grid(row=0, column=0, sticky="nsew")
        frame2.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1, uniform="group1")
        self.main.grid_columnconfigure(1, weight=1, uniform="group1")
        self.main.grid_rowconfigure(0, weight=1)

        self.main.pack()

    def open(self):
        """Open an image file to decrypt"""
        filename = fd.askopenfilename(
            title="Select Image", filetypes=[("PNG", "*.png")]
        )
        self.root.title(f"{filename.split('/')[-1]} - Decrypt")
        try:
            encryptor, decoded_text = utils.decrypt(
                filename, self.key
            )  # KEY KAHA SE LE RAHE HAI????
            print(encryptor)
            img = encryptor.img
            self.canvas.config(image=img, text="")
            self.text.configure(bg=DARK_GRAY, fg=WHITE)
            super().info.set(
                f"{len(decoded_text)-1} characters   |   {img.width}px x {img.height}px"
            )
        except KeyError:  # invalid decryption key
            self.text.config(state=NORMAL)
            self.text.delete("1.0", END)
            self.text.insert("1.0", "Invalid secret key.\nPlease check the key.")
            self.text.config(state=DISABLED)
            self.text.configure(bg=DARK_GRAY, fg=RED)
        # self.canvas.config(image=encryptor.img_scaled())

    def destroy(self):
        """Asdjhsadjk"""
        self.main.destroy()

    def export(self):
        """Saves the decrypted text as a file"""
        filename = fd.asksaveasfilename(
            title="Save File", filetypes=[("Text", "*.txt")]
        )
        if filename:
            with open(filename, "w") as f:
                f.write(self.text.get("1.0", END))

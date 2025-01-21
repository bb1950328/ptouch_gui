import pathlib
import tkinter as tk
from tkinter import ttk

import PIL.Image
import PIL.ImageTk

import data


class Preview(ttk.LabelFrame):
    def __init__(self, root: tk.Tk):
        super().__init__(root, text="Preview")

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.TOP, fill=tk.X)

        self.preview_image_id: int | None = None
        self.preview_image: PIL.ImageTk.PhotoImage | None = None

    def init(self, device_info: data.DeviceInfo):
        self.canvas.configure(height=device_info.max_printing_width)
        # todo display ruler (maybe in second canvas that doesn't scroll)

    def update_preview(self, preview_path: pathlib.Path):
        self.clear_preview()
        self.preview_image = PIL.ImageTk.PhotoImage(PIL.Image.open(preview_path))
        self.preview_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)

    def clear_preview(self):
        if self.preview_image_id is not None:
            self.canvas.delete(self.preview_image_id)
            self.preview_image_id = None

import tkinter as tk
from tkinter import ttk
import data


class PrinterInfo(ttk.LabelFrame):
    def __init__(self, root: tk.Tk):
        super().__init__(root, text="Printer")

        # lbl_options = {"anchor": "w",}
        lbl_options = {}

        grid_options = {"sticky": tk.W}

        ttk.Label(self, text="SW Version:", **lbl_options).grid(row=0, column=0, **grid_options)
        ttk.Label(self, text="Device:", **lbl_options).grid(row=1, column=0, **grid_options)
        ttk.Label(self, text="Media type:", **lbl_options).grid(row=2, column=0, **grid_options)
        ttk.Label(self, text="Media width:", **lbl_options).grid(row=3, column=0, **grid_options)
        ttk.Label(self, text="Max printing width:", **lbl_options).grid(row=4, column=0, **grid_options)
        ttk.Label(self, text="Color:", **lbl_options).grid(row=5, column=0, **grid_options)
        ttk.Label(self, text="Error:", **lbl_options).grid(row=6, column=0, **grid_options)

        self.sw_version = ttk.Label(self, **lbl_options)
        self.sw_version.grid(row=0, column=1, **grid_options)
        self.device_name = ttk.Label(self, **lbl_options)
        self.device_name.grid(row=1, column=1, **grid_options)
        self.media_type = ttk.Label(self, **lbl_options)
        self.media_type.grid(row=2, column=1, **grid_options)
        self.media_width = ttk.Label(self, **lbl_options)
        self.media_width.grid(row=3, column=1, **grid_options)
        self.max_printing_width = ttk.Label(self, **lbl_options)
        self.max_printing_width.grid(row=4, column=1, **grid_options)
        self.color = ttk.Label(self, **lbl_options)
        self.color.grid(row=5, column=1, **grid_options)
        self.error = ttk.Label(self, **lbl_options)
        self.error.grid(row=6, column=1, **grid_options)

    def display_info(self, info: data.DeviceInfo):
        self.sw_version.configure(text=info.version)
        self.device_name.configure(text=info.device_name)
        self.media_type.configure(text=info.media_type)
        self.media_width.configure(text=f"{info.media_width_mm}mm")
        self.max_printing_width.configure(text=f"{info.max_printing_width}px")
        self.color.configure(text=f"{info.text_color} on {info.tape_color}")
        self.error.configure(text=f"{info.error}")

    def display_error(self, error: data.DeviceError):
        self.sw_version.configure(text="?")
        self.device_name.configure(text="?")
        self.media_type.configure(text="?")
        self.media_width.configure(text="?")
        self.max_printing_width.configure(text="?")
        self.color.configure(text="?")
        self.error.configure(text=error.description)

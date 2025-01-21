import pathlib
import tkinter as tk

import ttkthemes

import data
import device
import ui_printer_info
import ui_input
import ui_preview
from tkinter import ttk


class App(ttkthemes.ThemedTk):
    def __init__(self):
        super().__init__(theme="adapta")

        # style = ttk.Style(self)
        # style.theme_use('alt')

        self.title("PTouch GUI")

        self.device = device.Device("ptouch-print")

        self.printer_info = ui_printer_info.PrinterInfo(self)
        self.printer_info.pack(side=tk.TOP, fill=tk.X)

        self.input = ui_input.Input(self)
        self.input.pack(side=tk.TOP, fill=tk.X)

        self.preview = ui_preview.Preview(self)
        self.preview.pack(side=tk.TOP, fill=tk.X)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)
        self.print_button = tk.Button(self.buttons_frame, text="Print", command=self.print)
        self.print_button.pack(side=tk.RIGHT)
        self.num_copies_var = tk.StringVar()
        self.num_copies_var.set("1")
        tk.Spinbox(self.buttons_frame, from_=1, to=100, width=3, increment=1, textvariable=self.num_copies_var).pack(side=tk.RIGHT, padx=5)
        tk.Label(self.buttons_frame, text="Num copies").pack(side=tk.RIGHT)

        self.input.add_design_change_listener(self.input_changed)

    def input_changed(self):
        design = self.input.get_current_design()
        self.print_button.config(state=tk.DISABLED if design is None else tk.NORMAL)
        if design is None:
            self.preview.clear_preview()
        else:
            preview_path = self.device.render_preview(design)
            self.preview.update_preview(preview_path)

    def print(self):
        design = self.input.get_current_design()
        if design:
            num_copies = int(self.num_copies_var.get())
            self.device.print(design, num_copies)

    def init(self):
        info = self.device.get_info()
        if isinstance(info, data.DeviceInfo):
            self.printer_info.display_info(info)
        else:
            self.printer_info.display_error(info)

    def run(self):
        self.mainloop()

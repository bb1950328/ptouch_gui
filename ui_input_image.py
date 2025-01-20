import enum
import os
import pathlib
import random
import tempfile
from tkinter import filedialog

import PIL.Image

import data
import ui_input
import tkinter as tk

from data import DeviceInfo


class ResizeMode(enum.Enum):
    ORIGINAL = 0
    AUTOMATIC = 1
    FIXED = 2

class ImageDesignCommand(data.DesignCommand):
    def __init__(self, original_file: pathlib.Path, resize_mode: ResizeMode, fixed_width: int|None=None):
        self.original_file = original_file
        self.resize_mode = resize_mode
        self.fixed_width = fixed_width
        self.file: pathlib.Path | None = None
        self.should_cleanup_file = False

    def initialize(self, device_info: DeviceInfo) -> None:
        if self.resize_mode == ResizeMode.ORIGINAL:
            self.file = self.original_file
        else:
            self.file = pathlib.Path(tempfile.gettempdir()) / f"resized_{os.urandom(16).hex()}.png"
            self.should_cleanup_file = True
            im = PIL.Image.open(self.original_file)
            factor: float
            if self.resize_mode == ResizeMode.AUTOMATIC:
                factor = device_info.max_printing_width / im.size[1]
            else:
                factor = self.fixed_width / im.size[0]
            im_resized = im.resize((int(im.size[0]*factor), int(im.size[1]*factor)), resample=PIL.Image.Resampling.NEAREST)
            im_resized.save(self.file)

    def get_command(self) -> list[str]:
        return ["--image", str(self.file)]

    def cleanup(self) -> None:
        if self.file is not None and self.should_cleanup_file:
            self.file.unlink()


class ImageDesign(data.Design):
    def __init__(self, image: pathlib.Path, resize_mode: ResizeMode, fixed_width: int|None=None):
        self.image = image
        self.resize_mode = resize_mode
        self.fixed_width = fixed_width

    def get_command(self) -> ImageDesignCommand:
        return ImageDesignCommand(self.image, self.resize_mode, self.fixed_width)


class InputDetailImage(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        ui_input.InputDetail.__init__(self, master, ui_input.InputType.IMAGE)

        tk.Label(self, text="Image file").grid(row=0, column=0, sticky=tk.W)

        self.path_var = tk.StringVar()
        self.path_var.trace("w", lambda *args: self._path_changed())
        self.path_entry = tk.Entry(self, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=1)

        self.chooser_button = tk.Button(self, text="...", command=self._open_filechooser)
        self.chooser_button.grid(row=0, column=2)

        tk.Label(self, text="Original Size:").grid(row=1, column=0, sticky=tk.W)
        self.original_size_var = tk.StringVar()
        tk.Label(self, textvariable=self.original_size_var).grid(row=1, column=1, sticky=tk.W)

        tk.Label(self, text="Set Height:").grid(row=2, column=0, sticky=tk.W)
        self.resize_type_var = tk.IntVar()
        self.resize_type_var.trace("w", lambda *args: self._resize_type_changed())
        tk.Radiobutton(self, text="Original", value=0, variable=self.resize_type_var).grid(row=2, column=1, sticky=tk.W)
        tk.Radiobutton(self, text="Automatic", value=1, variable=self.resize_type_var).grid(row=3, column=1, sticky=tk.W)
        fixed_frame = tk.Frame(self)
        fixed_frame.grid(row=4, column=1, sticky=tk.W)
        tk.Radiobutton(fixed_frame, text="Fixed: ", value=2, variable=self.resize_type_var).pack(side=tk.LEFT)
        self.fixed_size_var = tk.StringVar()
        self.fixed_size_spinbox = tk.Spinbox(fixed_frame, textvariable=self.fixed_size_var, from_=1, to=1024, width=4)
        self.fixed_size_spinbox.pack(side=tk.LEFT)

    def _path_changed(self):
        im = PIL.Image.open(self.path_var.get())
        w, h = im.size
        self.original_size_var.set(f"{w}*{h}")
        return self._fire_design_changed()

    def _resize_type_changed(self):
        self.fixed_size_spinbox.configure(state= tk.NORMAL if self.resize_type_var.get() == 2 else tk.DISABLED)
        self._fire_design_changed()

    def _open_filechooser(self):
        chosen_path = filedialog.askopenfilename(initialfile=str(self.path_var.get()), parent=self)
        if chosen_path:
            self.path_var.set(chosen_path)

    def get_settings(self) -> str:
        return self.path_var.get()

    def set_settings(self, settings: str) -> None:
        self.path_var.set(settings)

    def get_design(self) -> data.Design|None:
        path = pathlib.Path(self.path_var.get())
        if path.is_file():
            resize_mode = ResizeMode(self.resize_type_var.get())
            fixed_width = int(self.fixed_size_var.get()) if resize_mode == ResizeMode.FIXED else None
            return ImageDesign(path, resize_mode, fixed_width)
        return None

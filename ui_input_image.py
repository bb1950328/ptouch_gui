import pathlib
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import PIL.Image
import tkinterdnd2

import data
import designs
import ui_input


class InputDetailImage(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        super().__init__(master, designs.DesignType.IMAGE)

        self.drop_target_register(tkinterdnd2.DND_FILES)
        self.dnd_bind("<<Drop>>", lambda e: self.path_var.set(e.data))

        ttk.Label(self, text="Image file").grid(row=0, column=0, sticky=tk.W)

        self.path_var = tk.StringVar()
        self.path_var.trace("w", lambda *args: self._path_changed())
        self.path_entry = ttk.Entry(self, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=1)

        self.chooser_button = ttk.Button(self, text="...", command=self._open_filechooser)
        self.chooser_button.grid(row=0, column=2)

        ttk.Label(self, text="Original Size:").grid(row=1, column=0, sticky=tk.W)
        self.original_size_var = tk.StringVar()
        ttk.Label(self, textvariable=self.original_size_var).grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self, text="Set Height:").grid(row=2, column=0, sticky=tk.W)
        self.resize_type_var = tk.IntVar()
        self.resize_type_var.trace("w", lambda *args: self._resize_type_changed())
        ttk.Radiobutton(self, text="Original", value=0, variable=self.resize_type_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(self, text="Automatic", value=1, variable=self.resize_type_var).grid(row=3, column=1, sticky=tk.W)
        fixed_frame = ttk.Frame(self)
        fixed_frame.grid(row=4, column=1, sticky=tk.W)
        ttk.Radiobutton(fixed_frame, text="Fixed: ", value=2, variable=self.resize_type_var).pack(side=tk.LEFT)
        self.fixed_size_var = tk.StringVar()
        self.fixed_size_spinbox = ttk.Spinbox(fixed_frame, textvariable=self.fixed_size_var, from_=1, to=1024, width=4)
        self.fixed_size_spinbox.pack(side=tk.LEFT)

    def _path_changed(self):
        im = PIL.Image.open(self.path_var.get())
        w, h = im.size
        self.original_size_var.set(f"{w}*{h}")
        return self._fire_design_changed()

    def _resize_type_changed(self):
        self.fixed_size_spinbox.configure(state=tk.NORMAL if self.resize_type_var.get() == 2 else tk.DISABLED)
        self._fire_design_changed()

    def _open_filechooser(self):
        chosen_path = filedialog.askopenfilename(initialfile=str(self.path_var.get()), parent=self)
        if chosen_path:
            self.path_var.set(chosen_path)

    def set_design(self, design: designs.ImageDesign) -> None:
        self.path_var.set(str(design.image))
        self.resize_type_var.set(design.resize_mode.value)
        if design.fixed_width:
            self.fixed_size_var.set(str(design.fixed_width))

    def get_design(self) -> designs.ImageDesign | None:
        path = pathlib.Path(self.path_var.get())
        if path.is_file():
            resize_mode = designs.ImageResizeMode(self.resize_type_var.get())
            fixed_width = int(self.fixed_size_var.get()) if resize_mode == designs.ImageResizeMode.FIXED else None
            return designs.ImageDesign(path, resize_mode, fixed_width)
        return None

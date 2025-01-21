import tkinter as tk
from tkinter import ttk
import designs
import ui_input
import tkfontchooser


class InputDetailText(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        super().__init__( master, designs.DesignType.TEXT)
        self.font = tk.font.nametofont("TkDefaultFont").actual()
        self.default_font_size = self.font["size"]

        param_frame = ttk.Frame(self)
        param_frame.pack(side=tk.TOP, fill=tk.X)
        self.font_label = ttk.Label(param_frame)
        self.font_label.pack(side=tk.LEFT)

        self.font_size_var = tk.StringVar()
        self.font_size_var.set(str(self.font["size"]))
        self.font_size_entry = ttk.Spinbox(param_frame, from_=1, to=200, increment=1, width=3, textvariable=self.font_size_var)
        self.font_size_var.trace("w", lambda *args: self._font_size_changed())
        self.font_size_entry.pack(side=tk.LEFT, padx=5)

        self.font_btn = ttk.Button(param_frame, text="...", command=self._open_font_chooser)
        self.font_btn.pack(side=tk.LEFT)

        self.auto_font_size_var = tk.BooleanVar()
        self.auto_font_size = ttk.Checkbutton(param_frame, text="Auto Font Size", variable=self.auto_font_size_var, command=lambda: self._auto_font_size_changed())
        self.auto_font_size.pack(side=tk.LEFT)

        self._update_font_label()

        self.text = tk.Text(self)
        self.text.bind("<KeyRelease>", lambda e: self._fire_design_changed())
        self.text.pack(side=tk.TOP, fill=tk.BOTH)

    def _auto_font_size_changed(self):
        self.font_size_entry.configure(state=tk.DISABLED if self.auto_font_size_var.get() else tk.NORMAL)
        self._fire_design_changed()

    def _open_font_chooser(self):
        font = tkfontchooser.askfont(self)
        if font:
            self.font = font
            self._update_font_label()
            self.font_size_var.set(str(self.font["size"]))

    def _update_font_label(self):
        tkfamily = self.font['family'].replace(' ', '\ ')
        font_str = f"{tkfamily} {self.default_font_size:d} {self.font['weight']} {self.font['slant']}"
        if self.font['underline']:
            font_str += ' underline'
        if self.font['overstrike']:
            font_str += ' overstrike'
        self.font_label.configure(font=font_str, text=self.font["family"])

    def _font_size_changed(self):
        self.font["size"] = int(self.font_size_var.get())
        self._fire_design_changed()

    def set_design(self, design: designs.TextDesign) -> None:
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", design.text)

        self.font = {"family": design.font, "weight": tk.font.NORMAL, "slant": tk.font.ROMAN, "underline": 0, "overstrike": 0}
        if design.fontsize is None:
            self.auto_font_size_var.set(True)
        else:
            self.auto_font_size_var.set(False)
            self.font_size_var.set(str(design.fontsize))


    def get_design(self) -> designs.TextDesign | None:
        text = self.text.get("1.0", tk.END).strip()
        if text:
            font = self.font["family"]
            fontsize = None if self.auto_font_size_var.get() else int(self.font_size_var.get())
            return designs.TextDesign(text, font, fontsize)
        return None

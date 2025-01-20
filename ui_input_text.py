import tkinter as tk

import data
import ui_input
import tkfontchooser


class TextDesign(data.Design):
    def __init__(self, text: str, font: str, fontsize: int | None) -> None:
        self.text = text
        self.font = font
        self.fontsize = fontsize

    def get_command(self) -> data.DesignCommand:
        command = ["--font", self.font]
        if self.fontsize is not None:
            command += ["--fontsize", str(self.fontsize)]
        command += ["--text", self.text]
        return data.SimpleDesignCommand(command)


class InputDetailText(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        ui_input.InputDetail.__init__(self, master, ui_input.InputType.TEXT)
        self.font = tk.font.nametofont("TkDefaultFont").actual()
        self.default_font_size = self.font["size"]

        param_frame = tk.Frame(self)
        param_frame.pack(side=tk.TOP, fill=tk.X)
        self.font_label = tk.Label(param_frame)
        self.font_label.pack(side=tk.LEFT)

        self.font_size_var = tk.StringVar()
        self.font_size_var.set(str(self.font["size"]))
        self.font_size_entry = tk.Spinbox(param_frame, from_=1, to=200, increment=1, width=3, textvariable=self.font_size_var)
        self.font_size_var.trace("w", lambda *args: self._font_size_changed())
        self.font_size_entry.pack(side=tk.LEFT, padx=5)

        self.font_btn = tk.Button(param_frame, text="...", command=self._open_font_chooser)
        self.font_btn.pack(side=tk.LEFT)

        self.auto_font_size_var = tk.BooleanVar()
        self.auto_font_size = tk.Checkbutton(param_frame, text="Auto Font Size", variable=self.auto_font_size_var, command=lambda: self._auto_font_size_changed())
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

    def get_settings(self) -> str:
        return self.text.get("1.0", tk.END)

    def set_settings(self, settings: str) -> None:
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", settings)

    def get_design(self) -> data.Design|None:
        text = self.text.get("1.0", tk.END).strip()
        if text:
            font = self.font["family"]
            fontsize = None if self.auto_font_size_var.get() else int(self.font_size_var.get())
            return TextDesign(text, font, fontsize)
        return None

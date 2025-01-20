import os
import pathlib
import tempfile
import tkinter as tk

import PIL.Image
import qrcode

import data
import device
import ui_input
from data import DeviceInfo

ERROR_CORRECTION_LEVELS = {
    qrcode.ERROR_CORRECT_L: 0.07,
    qrcode.ERROR_CORRECT_M: 0.15,
    qrcode.ERROR_CORRECT_Q: 0.25,
    qrcode.ERROR_CORRECT_H: 0.30,
}


class QRCodeCommand(data.DesignCommand):
    def __init__(self, design: "QRCodeDesign"):
        self.design = design
        self.file = pathlib.Path(tempfile.gettempdir()) / f"qr_{os.urandom(16).hex()}.png"

    def initialize(self, device_info: DeviceInfo) -> None:
        qr = qrcode.QRCode(
            error_correction=self.design.ec_level,
            box_size=10,
            border=1,
        )
        qr.add_data(self.design.code)
        qr.make(fit=True)
        img: PIL.Image = qr.make_image(fill_color="black", back_color="white")
        img_resized = img.resize((device_info.max_printing_width, device_info.max_printing_width), resample=PIL.Image.Resampling.NEAREST)
        img_resized.save(self.file)

    def get_command(self) -> list[str]:
        return ["--image", str(self.file)]

    def cleanup(self) -> None:
        if self.file.is_file():
            self.file.unlink()


class QRCodeDesign(data.Design):
    def __init__(self, code: str, ec_level: int):
        self.code = code
        self.ec_level = ec_level

    def get_command(self) -> QRCodeCommand:
        return QRCodeCommand(self)


class InputDetailQRCode(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        ui_input.InputDetail.__init__(self, master, ui_input.InputType.QR_CODE)

        tk.Label(self, text="Data").grid(column=0, row=0)
        self.data_text = tk.Text(self, height=8)
        self.data_text.bind("<KeyRelease>", lambda *args: self._fire_design_changed())
        self.data_text.grid(column=1, row=0)

        tk.Label(self, text="Error Correction").grid(column=0, row=1)
        ec_frame = tk.Frame(self)
        self.error_correction_level_var = tk.IntVar()
        self.error_correction_level_var.set(qrcode.ERROR_CORRECT_M)
        self.error_correction_level_var.trace("w", lambda *args: self._fire_design_changed())
        for lvl, fraction in sorted(ERROR_CORRECTION_LEVELS.items(), key=lambda x: x[1]):
            percent = f"{int(fraction * 100):d}%"
            rb = tk.Radiobutton(ec_frame, text=percent, value=lvl, variable=self.error_correction_level_var)
            rb.pack(side=tk.LEFT)
        ec_frame.grid(column=1, row=1)

    def get_settings(self) -> str:
        return f"{self.error_correction_level_var.get():d};{self.data_text.get('1.0', tk.END)}"

    def set_settings(self, settings: str) -> None:
        ec, data_t = settings.split(";", maxsplit=1)
        self.error_correction_level_var.set(int(ec))
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert("1.0", data_t)

    def get_design(self) -> data.Design | None:
        return QRCodeDesign(self.data_text.get("1.0", tk.END), self.error_correction_level_var.get())

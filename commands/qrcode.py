import os
import pathlib
import tempfile

import qrcode
import PIL.Image

from . import base
import data
import designs


class QRCodeCommand(base.DesignCommand):
    def __init__(self, design: "designs.QRCodeDesign"):
        self.design = design
        self.file = pathlib.Path(tempfile.gettempdir()) / f"qr_{os.urandom(16).hex()}.png"

    def initialize(self, device_info: data.DeviceInfo) -> None:
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


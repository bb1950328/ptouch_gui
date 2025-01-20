import os
import pathlib
import tempfile

import data
import designs

import PIL.Image

from . import base


class ImageDesignCommand(base.DesignCommand):
    def __init__(self, design: "designs.ImageDesign"):
        self.design = design
        self.file: pathlib.Path | None = None
        self.should_cleanup_file = False

    def initialize(self, device_info: data.DeviceInfo) -> None:
        if self.design.resize_mode == designs.ImageResizeMode.ORIGINAL:
            self.file = self.design.image
        else:
            self.file = pathlib.Path(tempfile.gettempdir()) / f"resized_{os.urandom(16).hex()}.png"
            self.should_cleanup_file = True
            im = PIL.Image.open(self.design.image)
            factor: float
            if self.design.resize_mode == designs.ImageResizeMode.AUTOMATIC:
                factor = device_info.max_printing_width / im.size[1]
            else:
                factor = self.design.fixed_width / im.size[0]
            im_resized = im.resize((int(im.size[0] * factor), int(im.size[1] * factor)), resample=PIL.Image.Resampling.NEAREST)
            im_resized.save(self.file)

    def get_command(self) -> list[str]:
        return ["--image", str(self.file)]

    def cleanup(self) -> None:
        if self.file is not None and self.should_cleanup_file:
            self.file.unlink()

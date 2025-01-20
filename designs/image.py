import enum
import json
import pathlib

import commands
import data
import designs


class ImageResizeMode(enum.Enum):
    ORIGINAL = 0
    AUTOMATIC = 1
    FIXED = 2

class ImageDesign(designs.Design):
    def __init__(self, image: pathlib.Path, resize_mode: ImageResizeMode, fixed_width: int | None = None):
        self.image = image
        self.resize_mode = resize_mode
        self.fixed_width = fixed_width

    def get_command(self) -> commands.DesignCommand:
        return commands.ImageDesignCommand(self)

    def _serialize(self) -> str:
        return json.dumps({"image": str(self.image),
                           "resize_mode": self.resize_mode.value,
                           "fixed_width": self.fixed_width})

    def get_type(self) -> designs.DesignType:
        return designs.DesignType.IMAGE

    @staticmethod
    def deserialize(s: str) -> "ImageDesign":
        d = json.loads(s)
        return ImageDesign(pathlib.Path(d["image"]), ImageResizeMode(d["resize_mode"]), d["fixed_width"])
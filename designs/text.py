import json

from . import base
import commands


class TextDesign(base.Design):
    def __init__(self, text: str, font: str | None, fontsize: int | None) -> None:
        self.text = text
        self.font = font
        self.fontsize = fontsize

    def get_command(self) -> commands.DesignCommand:
        options = {}
        if self.font is not None:
            options["--font"] = self.font
        if self.fontsize is not None:
            options["--fontsize"] = str(self.fontsize)
        return commands.SimpleDesignCommand(["--text", self.text], options)

    def _serialize(self) -> str:
        return json.dumps({"text": self.text, "font": self.font, "fontsize": self.fontsize})

    def get_type(self) -> base.DesignType:
        return base.DesignType.TEXT

    @staticmethod
    def deserialize(s: str) -> "TextDesign":
        d = json.loads(s)
        return TextDesign(d["text"], d["font"], d["fontsize"])

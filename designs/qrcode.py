import json

from . import base
import commands


class QRCodeDesign(base.Design):
    def __init__(self, code: str, ec_level: int):
        self.code = code
        self.ec_level = ec_level

    def get_command(self) -> commands.DesignCommand:
        return commands.QRCodeCommand(self)

    def _serialize(self) -> str:
        return json.dumps({"code": self.code, "ec_level": self.ec_level})

    def get_type(self) -> base.DesignType:
        return base.DesignType.QR_CODE

    @staticmethod
    def deserialize(s: str) -> "QRCodeDesign":
        d = json.loads(s)
        return QRCodeDesign(d["code"], d["ec_level"])
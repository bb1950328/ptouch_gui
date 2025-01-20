import abc
import enum

import commands


class DesignType(enum.Enum):
    TEXT = 0
    IMAGE = 1
    QR_CODE = 2
    CHAIN = 3


DESIGN_TYPE_DESCRIPTIONS = {DesignType.TEXT: "Text",
                            DesignType.IMAGE: "Image",
                            DesignType.QR_CODE: "QR Code",
                            DesignType.CHAIN: "Chain",
                            }


class Design(abc.ABC):
    @abc.abstractmethod
    def get_command(self) -> commands.DesignCommand:
        pass

    def serialize(self) -> str:
        return str(self.get_type().value) + ";" + self._serialize()

    @abc.abstractmethod
    def _serialize(self) -> str:
        pass

    @abc.abstractmethod
    def get_type(self) -> DesignType:
        pass

    @staticmethod
    def deserialize(text: str) -> "Design":
        ty, s = text.split(";", maxsplit=1)
        ty = DesignType(ty)
        if ty == DesignType.TEXT:
            import text
            return text.TextDesign.deserialize(s)
        elif ty == DesignType.IMAGE:
            import image
            return image.ImageDesign.deserialize(s)
        elif ty == DesignType.QR_CODE:
            from . import qrcode
            return qrcode.QRCodeDesign.deserialize(s)
        elif ty == DesignType.CHAIN:
            import chain
            return chain.ChainDesign.deserialize(s)

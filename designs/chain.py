import json

from . import base
import commands
import designs


class ChainDesign(base.Design):
    def __init__(self, children: list[base.Design], types: list[base.DesignType]):
        self.children = children
        self.types = types

    def get_command(self) -> commands.DesignCommand:
        return commands.ChainDesignCommand(self)

    def _serialize(self) -> str:
        return json.dumps([[d.serialize() for d in self.children], [t.value for t in self.types]])

    @staticmethod
    def deserialize(text: str) -> "ChainDesign":
        d, t = json.loads(text)
        ds = [designs.Design.deserialize(n) for n in d]
        ts = [designs.DesignType(n) for n in t]
        return ChainDesign(ds, ts)

    def get_type(self) -> designs.DesignType:
        return designs.DesignType.CHAIN
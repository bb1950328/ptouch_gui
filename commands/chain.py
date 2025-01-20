import data
from . import base
import designs


class ChainDesignCommand(base.DesignCommand):
    def __init__(self, design: "designs.ChainDesign"):
        self.child_commands = [c.get_command() for c in design.children if c is not None]

    def initialize(self, device_info: data.DeviceInfo) -> None:
        for c in self.child_commands:
            c.initialize(device_info)

    def get_options(self) -> dict[str, str]:
        options: dict[str, str] = {}
        for c in self.child_commands:
            for k, v in c.get_options().items():
                if k in options and v != options[k]:
                    print("WARNING: duplicate option " + k + " with different values")
                else:
                    options[k] = v
        return options

    def get_command(self) -> list[str]:
        res: list[str] = []
        for c in self.child_commands:
            res.append("--chain")
            res.extend(c.get_command())
        return res

    def cleanup(self) -> None:
        for c in self.child_commands:
            c.cleanup()

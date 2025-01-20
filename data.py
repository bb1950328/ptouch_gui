import abc
import dataclasses


@dataclasses.dataclass
class DeviceInfo(object):
    version: str
    device_name: str
    max_printing_width: int
    media_type: str
    media_width_mm: int
    tape_color: str
    text_color: str
    error: int


@dataclasses.dataclass
class DeviceError(object):
    description: str


class Design(abc.ABC):
    @abc.abstractmethod
    def get_command(self) -> "DesignCommand":
        pass


class DesignCommand(abc.ABC):
    def initialize(self, device_info: DeviceInfo) -> None:
        pass
    @abc.abstractmethod
    def get_command(self) -> list[str]:
        pass

    def cleanup(self) -> None:
        pass


class SimpleDesignCommand(DesignCommand):
    def __init__(self, command: list[str]):
        self.command = command

    def get_command(self) -> list[str]:
        return self.command

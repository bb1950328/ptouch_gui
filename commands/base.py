import abc

import data


class DesignCommand(abc.ABC):
    def initialize(self, device_info: data.DeviceInfo) -> None:
        pass

    def get_options(self) -> dict[str, str]:
        return {}

    @abc.abstractmethod
    def get_command(self) -> list[str]:
        pass

    def cleanup(self) -> None:
        pass


class SimpleDesignCommand(DesignCommand):
    def __init__(self, command: list[str], options: dict[str, str]=None) -> None:
        self.command = command
        self.options = options if options is not None else {}

    def get_options(self) -> dict[str, str]:
        return self.options

    def get_command(self) -> list[str]:
        return self.command


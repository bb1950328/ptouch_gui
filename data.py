import abc
import dataclasses
import enum


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


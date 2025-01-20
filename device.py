import pathlib
import re
import subprocess
import tempfile

import data
import designs


class Device(object):
    def __init__(self, executable: str):
        self.executable = executable
        self.info: data.DeviceInfo | None = None

    def _run_command(self, command: list[str] | str) -> tuple[str, str]:
        if isinstance(command, str):
            command = [command]
        executable = ["sudo", self.executable] # todo remove sudo
        full_command = executable + command
        print("DEBUG:", full_command)
        proc = subprocess.run(full_command, capture_output=True)
        return proc.stdout.decode(), proc.stderr.decode()

    def get_version(self) -> str:
        out, err = self._run_command("--version")
        return (out + err).strip()

    def get_info(self) -> data.DeviceInfo | data.DeviceError:
        if self.info is None:
            out, err = self._run_command("--info")
            device_name_result = re.search(".* found on USB bus .*, device .*", err)
            if device_name_result is None:
                return data.DeviceError(err + out)
            self.info = data.DeviceInfo(self.get_version(),
                                        device_name_result.string.strip(),
                                        int(re.search("maximum printing width for this tape is ([0-9]+)px", out).group(1)),
                                        re.search("media type = .* \\((.*)\\)", out).group(1),
                                        int(re.search("media width = ([0-9]+) mm", out).group(1)),
                                        re.search("tape color = .* \\((.*)\\)", out).group(1),
                                        re.search("text color = .* \\((.*)\\)", out).group(1),
                                        int(re.search("error = ([0-9]+)", out).group(1)))
        return self.info

    def _options_to_list(self, options: dict[str, str]) -> list[str]:
        return [value for item in options.items() for value in item]

    def render_preview(self, design: designs.Design) -> pathlib.Path:
        png_path = pathlib.Path(tempfile.gettempdir()) / "ptouch_preview.png"
        command = design.get_command()
        try:
            command.initialize(self.get_info())
            out, err = self._run_command(self._options_to_list(command.get_options()) + command.get_command() + ["--writepng", str(png_path)])
        finally:
            command.cleanup()
        print(out, err)
        # todo check out and err
        return png_path

    def print(self, design: designs.Design, num_copies: int = 1) -> None:
        command = design.get_command()
        try:
            command.initialize(self.get_info())
            options = command.get_options()
            options["--copies"] = str(num_copies)
            out, err = self._run_command(self._options_to_list(options) + command.get_command())
        finally:
            command.cleanup()
        # todo check out and err
        print(out, err)

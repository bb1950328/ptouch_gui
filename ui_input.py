import abc
import tkinter as tk
from typing import Callable

import designs


class Input(tk.LabelFrame):

    def __init__(self, root: tk.Tk):
        tk.LabelFrame.__init__(self, root, text="Input")

        self.type_var = tk.IntVar()
        self.type_var.set(designs.DesignType.TEXT.value)

        self.type_frame = tk.Frame(self)
        self.type_frame.pack(side=tk.TOP)

        for it in designs.DesignType:
            rb = tk.Radiobutton(self.type_frame, variable=self.type_var, value=it.value, text=designs.DESIGN_TYPE_DESCRIPTIONS[it], command=self._change_type)
            rb.pack(side=tk.LEFT)

        self.inactive_settings: dict[designs.DesignType, str] = {}
        self.current_detail: InputDetail | None = None
        self.design_change_listeners: list[Callable] = []

        self._change_type()

    def _change_type(self):
        if self.current_detail is not None:
            old_design = self.current_detail.get_design()
            if old_design is not None:
                self.inactive_settings[self.current_detail.input_type] = old_design.serialize()
            self.current_detail.pack_forget()
        input_type = designs.DesignType(self.type_var.get())
        self.current_detail = InputDetail.create(self, input_type)
        if input_type in self.inactive_settings:
            self.current_detail.set_design(designs.Design.deserialize(self.inactive_settings[input_type]))
            del self.inactive_settings[input_type]
        for li in self.design_change_listeners:
            self.current_detail.add_design_change_listener(li)
            li()
        self.current_detail.pack(side=tk.TOP, fill=tk.X)

    def get_current_design(self) -> designs.Design | None:
        return self.current_detail.get_design()

    def add_design_change_listener(self, listener: Callable):
        self.design_change_listeners.append(listener)
        if self.current_detail is not None:
            self.current_detail.add_design_change_listener(listener)


class InputDetail(tk.Frame, abc.ABC):
    def __init__(self, master: tk.Widget, input_type: designs.DesignType):
        tk.Frame.__init__(self, master)
        self._input_type = input_type
        self.design_change_listeners: list[Callable] = []

    @classmethod
    def create(cls, master: tk.Widget, input_type: designs.DesignType):
        if input_type == designs.DesignType.TEXT:
            import ui_input_text
            return ui_input_text.InputDetailText(master)
        elif input_type == designs.DesignType.IMAGE:
            import ui_input_image
            return ui_input_image.InputDetailImage(master)
        elif input_type == designs.DesignType.QR_CODE:
            import ui_input_qrcode
            return ui_input_qrcode.InputDetailQRCode(master)
        elif input_type == designs.DesignType.CHAIN:
            import ui_input_chain
            return ui_input_chain.InputDetailChain(master)
        else:
            raise ValueError(f"Input type {input_type} not implemented")

    @property
    def input_type(self):
        return self._input_type

    @abc.abstractmethod
    def set_design(self, design: designs.Design) -> None:
        pass

    @abc.abstractmethod
    def get_design(self) -> designs.Design | None:
        pass

    def add_design_change_listener(self, listener: Callable):
        self.design_change_listeners.append(listener)

    def _fire_design_changed(self):
        for listener in self.design_change_listeners:
            listener()

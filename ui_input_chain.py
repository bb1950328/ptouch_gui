import json

import designs
import ui_input
import tkinter as tk
from tkinter import ttk


class InputDetailChain(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        super().__init__(master, designs.DesignType.CHAIN)

        self.child_designs: list[designs.Design] = []
        self.child_types: list[designs.DesignType] = []
        self.current_detail: ui_input.InputDetail | None = None
        self.current_detail_index: int = 0

        list_frame = ttk.Frame(self)
        list_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self._listbox_selection_changed())
        self.listbox.pack(side=tk.TOP, fill=tk.Y)

        value_inside = tk.StringVar()
        value_inside.set("Add...")

        def add_click(*args):
            ty = next(k for k, v in designs.DESIGN_TYPE_DESCRIPTIONS.items() if v == value_inside.get())
            value_inside.set("Add...")
            self._add_child(ty)

        self.add_button = ttk.OptionMenu(list_frame, value_inside, *designs.DESIGN_TYPE_DESCRIPTIONS.values())
        self.add_button.pack(side=tk.LEFT)
        delete_button = ttk.Button(list_frame, text="Delete", command=lambda: self._delete_selected())
        delete_button.pack(side=tk.LEFT)

        self.detail_frame = ttk.Frame(self)
        self.detail_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        value_inside.trace("w", add_click)

    def _leave_detail(self):
        if self.current_detail is not None:
            self.child_designs[self.current_detail_index] = self.current_detail.get_design()
            self.child_types[self.current_detail_index] = self.current_detail.input_type
            self.current_detail.pack_forget()
            self.current_detail = None
            self.current_detail_index = -1

    def _enter_detail(self, detail: ui_input.InputDetail, index: int):
        self.current_detail = detail
        self.current_detail_index = index
        self.current_detail.pack(side=tk.TOP, fill=tk.BOTH)
        self.listbox.selection_set(index)

    def _add_child(self, design_type: designs.DesignType):
        self._leave_detail()

        detail = ui_input.InputDetail.create(self.detail_frame, design_type)
        detail.add_design_change_listener(lambda: self._fire_design_changed())
        self.child_designs.append(detail.get_design())
        self.child_types.append(design_type)
        self.listbox.insert(tk.END, designs.DESIGN_TYPE_DESCRIPTIONS[design_type])

        self._enter_detail(detail, len(self.child_designs) - 1)
        self._fire_design_changed()

    def _listbox_selection_changed(self):
        self._leave_detail()

        if len(self.listbox.curselection()) > 0:
            new_index = self.listbox.curselection()[0]
            new_type = self.child_types[new_index]
            new_detail = ui_input.InputDetail.create(self.detail_frame, new_type)
            new_detail.add_design_change_listener(lambda: self._fire_design_changed())
            new_design = self.child_designs[new_index]
            if new_design is not None:
                new_detail.set_design(new_design)

            self._enter_detail(new_detail, new_index)

    def _delete_selected(self):
        idx_to_delete = self.current_detail_index

        self._leave_detail()

        self.listbox.delete(idx_to_delete)
        del self.child_designs[idx_to_delete]
        del self.child_types[idx_to_delete]

        self._fire_design_changed()

        self.listbox.selection_set(min(idx_to_delete, len(self.child_designs) - 1))

    def set_design(self, design: designs.ChainDesign) -> None:
        self.child_designs: list[designs.Design] = design.children
        self.listbox.delete(0, tk.END)
        for c in self.child_designs:
            self.listbox.insert(tk.END, designs.DESIGN_TYPE_DESCRIPTIONS[c.get_type()])

    def set_settings(self, settings: str) -> None:
        self.child_designs: list[designs.Design] = json.loads(settings)

    def get_design(self) -> designs.Design | None:
        if self.current_detail is not None and self.current_detail_index >= 0:
            self.child_designs[self.current_detail_index] = self.current_detail.get_design()
            self.child_types[self.current_detail_index] = self.current_detail.input_type
        return designs.ChainDesign(self.child_designs, self.child_types) if any(self.child_designs) else None

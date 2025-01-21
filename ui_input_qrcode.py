import tkinter as tk
from tkinter import ttk

import qrcode

import designs
import ui_input

ERROR_CORRECTION_LEVELS = {
    qrcode.ERROR_CORRECT_L: 0.07,
    qrcode.ERROR_CORRECT_M: 0.15,
    qrcode.ERROR_CORRECT_Q: 0.25,
    qrcode.ERROR_CORRECT_H: 0.30,
}






class InputDetailQRCode(ui_input.InputDetail):
    def __init__(self, master: tk.Widget):
        super().__init__(master, designs.DesignType.QR_CODE)

        ttk.Label(self, text="Data").grid(column=0, row=0)
        self.data_text = tk.Text(self, height=8)
        self.data_text.bind("<KeyRelease>", lambda *args: self._fire_design_changed())
        self.data_text.grid(column=1, row=0)

        ttk.Label(self, text="Error Correction").grid(column=0, row=1)
        ec_frame = ttk.Frame(self)
        self.error_correction_level_var = tk.IntVar()
        self.error_correction_level_var.set(qrcode.ERROR_CORRECT_M)
        self.error_correction_level_var.trace("w", lambda *args: self._fire_design_changed())
        for lvl, fraction in sorted(ERROR_CORRECTION_LEVELS.items(), key=lambda x: x[1]):
            percent = f"{int(fraction * 100):d}%"
            rb = ttk.Radiobutton(ec_frame, text=percent, value=lvl, variable=self.error_correction_level_var)
            rb.pack(side=tk.LEFT)
        ec_frame.grid(column=1, row=1)

    def set_design(self, design: designs.QRCodeDesign) -> None:
        self.error_correction_level_var.set(int(design.ec_level))
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert("1.0", design.code)

    def get_design(self) -> designs.QRCodeDesign | None:
        return designs.QRCodeDesign(self.data_text.get("1.0", tk.END), self.error_correction_level_var.get())

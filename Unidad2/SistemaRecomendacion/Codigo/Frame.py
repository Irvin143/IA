import customtkinter as ctk

class FrameIngredientes(ctk.CTkFrame):
    def __init__(self, master, category, mode="Gustos", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected = set()
        self.buttons = {}
        self.mode = mode

        
        ctk.CTkLabel(self, text=mode, font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 5)) 
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(anchor="w", pady=(0, 5))

        if "Gustos" in mode:
            normal_color = "#2b8b85"
        else:
            normal_color = "#f81a1a"

        scroll = ctk.CTkScrollableFrame(btn_frame, height=10, width=1500)
        scroll.pack(anchor="w", fill="x")
        # evitar que el scroll se expanda según el contenido para mantenerlo más pequeño
        scroll.pack_propagate(False)
        cols = 9  # ajustar número de columnas por fila según convenga

        for i, sabor in enumerate(category):
            btn = ctk.CTkButton(scroll, text=sabor,
                    fg_color=normal_color,
                    font=("Arial", 14),
                    command=lambda s=sabor: self.toggle(s))
            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5, sticky="w")
            self.buttons[sabor] = btn
        
        

        """ctk.CTkLabel(btn_frame, text="Restricciones", font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 5)) 
        scroll2 = ctk.CTkScrollableFrame(btn_frame, height=140, width=1500)
        scroll2.pack(anchor="w", fill="x", expand=True)
        cols = 9  # ajustar número de columnas por fila según convenga

        for i, sabor in enumerate(category):
            saborRestriccion = sabor + "(No)"
            btn = ctk.CTkButton(scroll2, text=sabor,
                    fg_color=normal_color,
                    font=("Arial", 14),
                    command=lambda s=saborRestriccion: self.toggle(s, mode="restricciones"))
            btn.grid(row=i // cols, column=i % cols, padx=5, pady=5, sticky="w")
            self.buttons[saborRestriccion] = btn"""

        

    def toggle(self, opt):
        if self.mode == "Gustos":
            normal_color = "#2b8b85"
            selected_color = "#3d5c8d"
        else:  # restricciones
            normal_color = "#f81a1a"
            selected_color = "#f87c71"
            
        if opt in self.selected:
            self.selected.remove(opt)
            self.buttons[opt].configure(fg_color=normal_color)
        else:
            self.selected.add(opt)
            self.buttons[opt].configure(fg_color=selected_color)

import customtkinter as ctk

class FrameIngredientes(ctk.CTkFrame):
    def __init__(self, master, category, mode="gustos", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected = set()
        self.buttons = {}
        self.mode = mode

        title_text = category["nombre"]
        
        ctk.CTkLabel(self, text=title_text, font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 5)) 
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(anchor="w", pady=(0, 5))

        # Colores según el modo
        if mode == "gustos":
            normal_color = "#2b8b85"
        else:  # restricciones
            normal_color = "#f81a1a"

        for sabor in category["sabores"]:
            btn = ctk.CTkButton(
                btn_frame, text=sabor, width=100, fg_color=normal_color,
                command=lambda o=sabor: self.toggle(o)
            )
            btn.pack(side="left", padx=5, pady=2)
            self.buttons[sabor] = btn 

    def toggle(self, opt):
        if self.mode == "gustos":
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

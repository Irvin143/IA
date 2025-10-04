import customtkinter as ctk
import json

class IngredientSelector(ctk.CTkFrame):
    def __init__(self, master, category, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected = set()
        self.negative_selected = set()
        self.buttons = {}
        self.negative_buttons = {}

        ctk.CTkLabel(self, text=category["nombre"], font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 5)) 
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(anchor="w", pady=(0, 5))

        for sabor in category["sabores"]:
            btn = ctk.CTkButton(
                btn_frame, text=sabor, width=100, fg_color="#2b8b85",
                command=lambda o=sabor: self.toggle(o)
            )
            btn.pack(side="left", padx=5, pady=2)
            self.buttons[sabor] = btn 

    def toggle(self, opt):
        if opt in self.selected:
            self.selected.remove(opt)
            self.buttons[opt].configure(fg_color="#2b8b85")
        else:
            self.selected.add(opt)
            self.buttons[opt].configure(fg_color="#3d5c8d")

    def toggle_negative(self, neg):
        if neg in self.negative_selected:
            self.negative_selected.remove(neg)
            self.negative_buttons[neg].configure(fg_color="#ffcccc")
        else:
            self.negative_selected.add(neg)
            self.negative_buttons[neg].configure(fg_color="#ff6f61")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Recomendación de Restaurante")
        self.geometry("700x700")
                
        with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion.py\\Categorias.json", "r", encoding="utf-8") as f:
            categorias = json.load(f)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        for cat in categorias:
            selector = IngredientSelector(
                main_frame, cat
            )
            selector.pack(fill="x", pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
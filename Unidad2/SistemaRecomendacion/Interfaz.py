import customtkinter as ctk
import json
from Frame import FrameIngredientes
from Recomendacion import recomendarPlatillos
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Recomendación de Restaurante")
        self.geometry("700x700")
                
        with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion\\Categorias.json", "r", encoding="utf-8") as f:
            self.categorias = json.load(f)

        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Sistema de Recomendación", 
                                  font=("Arial", 24, "bold"))
        title_label.pack(pady=(10, 20))

        # Frame para los radio buttons
        radio_frame = ctk.CTkFrame(main_frame)
        radio_frame.pack(fill="x", pady=(0, 20))

        self.mode_var = ctk.StringVar(value="gustos")
        
        radio_gustos = ctk.CTkRadioButton(radio_frame, text="Gustos", 
                                         variable=self.mode_var, value="gustos",
                                         command=self.cambiar_frame)
        radio_gustos.pack(side="left", padx=20, pady=10)

        radio_restricciones = ctk.CTkRadioButton(radio_frame, text="Restricciones", 
                                               variable=self.mode_var, value="restricciones",
                                               command=self.cambiar_frame)
        radio_restricciones.pack(side="left", padx=20, pady=10)

        # Crear ambos frames desde el inicio
        self.crear_frames(main_frame)
        
        # Mostrar frame inicial (gustos)
        self.cambiar_frame()

    def crear_frames(self, parent):
        """Crea ambos frames: gustos y restricciones"""
        
        # Frame para GUSTOS
        self.frame_gustos = ctk.CTkScrollableFrame(parent)
        
        info_gustos = ctk.CTkLabel(self.frame_gustos, 
                                 text="Selecciona tus gustos culinarios:", 
                                 font=("Arial", 16))
        info_gustos.pack(pady=(10, 20))
        
        self.selectores_gustos = []
        for cat in self.categorias:
            selector = FrameIngredientes(self.frame_gustos, cat, mode="gustos")
            selector.pack(fill="x", pady=10, padx=10)
            self.selectores_gustos.append(selector)
            
        btn_gustos = ctk.CTkButton(self.frame_gustos, text="Obtener Recomendaciones",
                                 font=("Arial", 16, "bold"), height=40,
                                 command=lambda: self.veredicto())
        btn_gustos.pack(pady=20)
        
        # Frame para RESTRICCIONES
        self.frame_restricciones = ctk.CTkScrollableFrame(parent)
        
        info_restricciones = ctk.CTkLabel(self.frame_restricciones, 
                                        text="Selecciona lo que NO quieres o no puedes comer:", 
                                        font=("Arial", 16))
        info_restricciones.pack(pady=(10, 20))
        
        self.selectores_restricciones = []
        for cat in self.categorias:
            selector = FrameIngredientes(self.frame_restricciones, cat, mode="restricciones")
            selector.pack(fill="x", pady=10, padx=10)
            self.selectores_restricciones.append(selector)
            
        btn_restricciones = ctk.CTkButton(self.frame_restricciones, text="Aplicar Restricciones",
                                        font=("Arial", 16, "bold"), height=40,
                                        command=lambda: self.obtener_selecciones("restricciones"))
        btn_restricciones.pack(pady=20)

    def cambiar_frame(self):
        """Muestra el frame correspondiente al modo actual"""
        modo_actual = self.mode_var.get()
        
        if modo_actual == "gustos":
            # Ocultar frame de restricciones y mostrar gustos
            self.frame_restricciones.pack_forget()
            self.frame_gustos.pack(fill="both", expand=True, pady=(0, 10))
        else:
            # Ocultar frame de gustos y mostrar restricciones
            self.frame_gustos.pack_forget()
            self.frame_restricciones.pack(fill="both", expand=True, pady=(0, 10))

    def obtener_selecciones(self, modo=None):
        """Obtiene todas las selecciones actuales"""
        if modo is None:
            modo = self.mode_var.get()
            
        # Seleccionar los selectores correctos según el modo
        if modo == "gustos":
            selectores = self.selectores_gustos
        else:
            selectores = self.selectores_restricciones
            
        selecciones = {}
        
        for selector in selectores:
            if selector.selected:
                categoria = selector.winfo_children()[0].cget("text")
                selecciones[categoria] = list(selector.selected)
        
        # Mostrar en una ventana emergente
        if selecciones:
            mensaje = f"Modo: {modo.capitalize()}\n\n"
            for cat, items in selecciones.items():
                mensaje += f"{cat}: {', '.join(items)}\n"
        else:
            mensaje = f"No hay selecciones en {modo}"

        
    def veredicto(self):
        """Obtiene todas las selecciones de ambos modos"""
        gustos = {}
        restricciones = {}
        
        # Obtener gustos
        for selector in self.selectores_gustos:
            if selector.selected:
                categoria = selector.winfo_children()[0].cget("text")
                gustos[categoria] = list(selector.selected)
                
        # Obtener restricciones
        for selector in self.selectores_restricciones:
            if selector.selected:
                categoria = selector.winfo_children()[0].cget("text")
                restricciones[categoria] = list(selector.selected)
        
        recomendarPlatillos(gustos, restricciones)
        return gustos, restricciones
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
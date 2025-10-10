import customtkinter as ctk
import json

try:
    # Preferred: relative imports when running as a package
    from .Frame import FrameIngredientes
    from .Recomendacion import recomendarPlatillos
    from .TablaRecomendacion import TablaRecomendacion
except ImportError:
    # Fallback: allow running the module directly (script mode)
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from Frame import FrameIngredientes
    from Recomendacion import recomendarPlatillos
    from TablaRecomendacion import TablaRecomendacion

from tkinter import ttk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Recomendación de Restaurante")
        self.geometry("700x700")
        
        with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion\\Json\\Sabores.json", "r", encoding="utf-8") as f:
            self.sabores = json.load(f)
        with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion\\Json\\Ingredientes.json", "r", encoding="utf-8") as f:
            self.ingredientes = json.load(f)

        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(main_frame, text="Sistema de Recomendación", 
                                font=("Arial", 24, "bold"))
        title_label.pack(pady=(10, 20))

        # Crear ambos frames desde el inicio
        self.crear_frames(main_frame)

    def crear_frames(self, parent):
        """Crea ambos frames: gustos y restricciones"""
        
        # Frame para GUSTOS
        self.frame_gustos = ctk.CTkScrollableFrame(parent)
        

        """ APARTADO DE GUSTOS Y INGREDIENTES """
        info_gustos = ctk.CTkLabel(self.frame_gustos, 
                                text="Selecciona tus gustos culinarios:", 
                                font=("Arial", 16))
        info_gustos.pack(pady=(10, 20))
        
        #Crear apartado de gustos
        self.selectores_gustos = []
        selector = FrameIngredientes(self.frame_gustos, self.sabores, mode="Gustos")
        selector.pack(fill="x", pady=10, padx=10)
        self.selectores_gustos.append(selector)


        #Crear apartado de ingredientes
        self.selectores_ingredientes = []
        selector = FrameIngredientes(self.frame_gustos, self.ingredientes, mode="Gustos Ingredientes")
        selector.pack(fill="x", pady=10, padx=10)
        self.selectores_ingredientes.append(selector)

        """ APARTADO DE RESTRICCIONES """

        #Crear apartado de restricciones
        info_restricciones = ctk.CTkLabel(self.frame_gustos, 
                                        text="Selecciona lo que NO quieres", 
                                        font=("Arial", 16))
        info_restricciones.pack(pady=(10, 20))
        
        self.selectores_restricciones = []
        selector = FrameIngredientes(self.frame_gustos, self.sabores, mode="Restricciones")
        selector.pack(fill="x", pady=10, padx=10)
        self.selectores_restricciones.append(selector)

        #Crear apartado de restricciones dieteticos
        self.selectores_dieteticos = []
        listaDieteticos = ["Vegetariano", "Vegano", "Sin Gluten", "Sin Lactosa"]
        selector = FrameIngredientes(self.frame_gustos, listaDieteticos, mode="Restricciones Dieteticos")
        selector.pack(fill="x", pady=10, padx=10)
        self.selectores_dieteticos.append(selector)

        self.tabla_recomendacion = TablaRecomendacion(self.frame_gustos)
        self.tabla_recomendacion.frame.pack(fill="both", expand=True, pady=(10, 10), padx=10)

            # Botón para obtener recomendaciones
        btn_gustos = ctk.CTkButton(self.frame_gustos, text="Obtener Recomendaciones",
                                    font=("Arial", 16, "bold"), height=40,
                                    command=lambda: self.veredicto())
        btn_gustos.pack(pady=20)
        self.frame_gustos.pack(fill="both", expand=True, pady=(0, 10))
        
        
    """"Funcion que da el veredicto final"""
    def veredicto(self):
        """Obtiene todas las selecciones de ambos modos"""
        gustos = {}
        restricciones = {}
        
        # Obtener gustos
        for selector in self.selectores_gustos:
            if selector.selected:
                gustos = list(selector.selected)
                
        # Obtener restricciones
        for selector in self.selectores_restricciones:
            if selector.selected:
                restricciones = list(selector.selected)
        
        print("Gustos:", gustos)
        print("Restricciones:", restricciones)
        
        self.tabla_recomendacion.llenar_tabla(recomendarPlatillos(gustos, restricciones))

    
if __name__ == "__main__":
    app = App()
    app.mainloop()
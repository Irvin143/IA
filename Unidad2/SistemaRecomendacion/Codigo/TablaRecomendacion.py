import customtkinter as ctk
from tkinter import ttk

class TablaRecomendacion:
    """
    Clase para poner la recomendacion en una tabla dentro de un frame.
    Cada fila es un platillo con sus detalles.
    """

    def __init__(self, parent):
        # Frame para la tabla de platillos
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, pady=(10, 10), padx=10)

        label_tabla = ctk.CTkLabel(self.frame, text="Tabla de Platillos", font=("Arial", 16))
        label_tabla.pack(pady=(5, 5))

        # Definir columnas
        cols = ("nombre", "sabores", "ingredientes", "categoria", "preparacion")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=6)

        # Encabezados en español
        self.tree.heading("nombre", text="Nombre del platillo")
        self.tree.heading("sabores", text="Sabores")
        self.tree.heading("ingredientes", text="Ingredientes")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("preparacion", text="Preparación")

        # Anchos y alineación
        self.tree.column("nombre", width=160, anchor="w")
        self.tree.column("sabores", width=250, anchor="w")
        self.tree.column("ingredientes", width=250, anchor="w")
        self.tree.column("categoria", width=120, anchor="w")
        self.tree.column("preparacion", width=100, anchor="w")

        # Scrollbar vertical
        self.tree_scrollbar = ctk.CTkScrollbar(self.frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)
        self.tree_scrollbar.pack(side="right", fill="y", pady=5)

    def llenar_tabla(self, platillos):
        """
        platillos: lista de dicts con claves:
          'nombre' (str),
          'sabores' (list o str),
          'ingredientes' (list o str),
          'categoria' (str),
          'preparacion' (str)
        """
        # limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
        # insertar filas
        for p in platillos:
            # soportar dicts o listas/tuplas (por ejemplo filas devueltas como tuplas)
            for pla in p:
                nombre = pla["nombre"] 
                sabores = pla.get("sabores", "")
                ingredientes = pla.get("ingredientes", "")
                categoria = pla.get("categoria", "")
                preparacion = pla.get("preparacion", "")

            if isinstance(sabores, (list, tuple)):
                sabores = ", ".join(map(str, sabores))
            if isinstance(ingredientes, (list, tuple)):
                ingredientes = ", ".join(map(str, ingredientes))

            self.tree.insert("", "end", values=(nombre, sabores, ingredientes, categoria, preparacion))
           
import tkinter as tk
from tkinter import scrolledtext

# Clase Nodo para representar cada elemento del árbol
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

# Clase Árbol de Búsqueda Binaria
class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # Método para insertar un nuevo valor en el árbol
    def insertar(self, valor):
        """
        Inserta un nuevo nodo con el valor dado en el árbol.
        Si el árbol está vacío, el nuevo nodo será la raíz.
        Si no, se busca la posición correcta recursivamente.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)
    

    # Método para eliminar un nodo con un valor específico
    def eliminarNodo(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            # Nodo con solo un hijo o sin hijos
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            # Nodo con dos hijos: obtener el sucesor inorder (el más pequeño en el subárbol derecho)
            temp = self._minimo(nodo.derecha)
            nodo.valor = temp.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, temp.valor)
        return nodo
    def _minimo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual


        # Método auxiliar para la inserción recursiva
    def _insertar_recursivo(self, nodo_actual, valor):
        # Si el valor es menor, va a la izquierda
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, valor)
        # Si el valor es mayor o igual, va a la derecha
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo_actual.derecha, valor)

    # Método para imprimir el árbol en orden (izquierda, raíz, derecha)
    def imprimir_arbol(self):
        """
        Imprime el árbol en forma vertical con ramas.
        """
        self._imprimir_estructura(self.raiz, "", True)

    def _imprimir_estructura(self, nodo, prefijo, es_ultimo):
        if nodo is not None:
            # Dibujar prefijo + rama
            rama = "└── " if es_ultimo else "├── "
            print(prefijo + rama + str(nodo.valor))

            # Nuevo prefijo para los hijos
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")

            # Llamadas recursivas a los hijos
            hijos = [h for h in (nodo.izquierda, nodo.derecha) if h is not None]
            for i, hijo in enumerate(hijos):
                es_ultimo_hijo = (i == len(hijos) - 1)
                self._imprimir_estructura(hijo, nuevo_prefijo, es_ultimo_hijo)
    

    # Método para buscar un valor en el árbol
    def buscar(self, valor):
        """
        Busca un valor en el árbol.
        """
        return self._buscar_recursivo(self.raiz, valor, 1)
    
    def _buscar_recursivo(self, nodo, valor, profundidad):
        if nodo is None:
            return 100  # Valor no encontrado
        if valor == nodo.valor:
            return profundidad
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor, profundidad + 1)
        else:
            return self._buscar_recursivo(nodo.derecha, valor, profundidad + 1)




def mostrar_arbol_en_textarea(arbol, textarea):
    # Limpiar el contenido anterior
    textarea.delete(1.0, tk.END)
    # Usar una función auxiliar para capturar el árbol como texto
    def capturar_estructura(nodo, prefijo, es_ultimo):
        if nodo is not None:
            rama = "└── " if es_ultimo else "├── "
            linea = prefijo + rama + str(nodo.valor) + "\n"
            resultado = linea
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            hijos = [h for h in (nodo.izquierda, nodo.derecha) if h is not None]
            for i, hijo in enumerate(hijos):
                es_ultimo_hijo = (i == len(hijos) - 1)
                resultado += capturar_estructura(hijo, nuevo_prefijo, es_ultimo_hijo)
            return resultado
        return ""
    texto_arbol = capturar_estructura(arbol.raiz, "", True)
    textarea.insert(tk.END, texto_arbol)



import customtkinter as ctk

if __name__ == "__main__":
    arbol = ArbolBinarioBusqueda()
    datos = [50, 30, 70, 20, 40, 60, 80, 20, 68]
    for valor in datos:
        arbol.insertar(valor)

    # Crear ventana principal usando customtkinter
    ventana = ctk.CTk()
    ventana.title("Visualización de Árbol Binario de Búsqueda")
    ventana.geometry("700x500")

    # Crear un CTkTextbox con scroll (usando CTkTextbox en vez de scrolledtext)
    textarea = ctk.CTkTextbox(ventana, width=650, height=400, font=("Consolas", 18))
    textarea.place(x=25, y=20)

    # Mostrar el árbol en el TextArea
    def mostrar_arbol_en_textarea_custom(arbol, textarea):
        textarea.delete("0.0", "end")
        def capturar_estructura(nodo, prefijo, es_ultimo):
            if nodo is not None:
                rama = "└── " if es_ultimo else "├── "
                linea = prefijo + rama + str(nodo.valor) + "\n"
                resultado = linea
                nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
                hijos = [h for h in (nodo.izquierda, nodo.derecha) if h is not None]
                for i, hijo in enumerate(hijos):
                    es_ultimo_hijo = (i == len(hijos) - 1)
                    resultado += capturar_estructura(hijo, nuevo_prefijo, es_ultimo_hijo)
                return resultado
            return ""
        texto_arbol = capturar_estructura(arbol.raiz, "", True)
        textarea.insert("end", texto_arbol)

    mostrar_arbol_en_textarea_custom(arbol, textarea)
    # Entry para ingresar valores
    entry_valor = ctk.CTkEntry(ventana, font=("Consolas", 18), width=100)
    entry_valor.place(x=25, y=440)

    def eliminarArbol():
        arbol.raiz = None 
        mostrar_arbol_en_textarea_custom(arbol, textarea)

    # Funciones para los botones
    def insertar_valor():
        try:
            valor = int(entry_valor.get())
            arbol.insertar(valor)
            mostrar_arbol_en_textarea_custom(arbol, textarea)
        except ValueError:
            textarea.insert("end", "Valor inválido para insertar\n")

    def buscar_valor():
        try:
            valor = int(entry_valor.get())
            profundidad = arbol.buscar(valor)
            if profundidad == 100:
                textarea.insert("end", f"Valor {valor} no encontrado\n")
            else:
                textarea.insert("end", f"Valor {valor} encontrado en profundidad {profundidad}\n")
        except ValueError:
            textarea.insert("end", "Valor inválido para buscar\n")

    def eliminar_valor():
        try:
            valor = int(entry_valor.get())
            arbol.eliminarNodo(valor)
            mostrar_arbol_en_textarea_custom(arbol, textarea)
        except ValueError:
            textarea.insert("end", "Valor inválido para eliminar\n")

    # Botones para insertar, buscar y eliminar
    btn_insertar = ctk.CTkButton(
        ventana,
        text="Insertar",
        font=("Consolas", 18),
        command=insertar_valor,
        corner_radius=10,
        fg_color="#393E46",
        text_color="white",
        width=100,
        height=30
    )
    btn_insertar.place(x=150, y=440)

    btn_buscar = ctk.CTkButton(
        ventana,
        text="Buscar",
        font=("Consolas", 18),
        command=buscar_valor,
        corner_radius=10,
        fg_color="#393E46",
        text_color="white",
        width=100,
        height=30
    )
    btn_buscar.place(x=260, y=440)

    btn_eliminar = ctk.CTkButton(
        ventana,
        text="Eliminar",
        font=("Arial", 18, "bold"),
        corner_radius=20,
        fg_color="#00ADB5",
        text_color="white",
        width=100,
        height=30,
        command=eliminar_valor
    )
    btn_eliminar.place(x=370, y=440)

    btn_eliminar_arbol = ctk.CTkButton(
        ventana,
        text="Eliminar Árbol",
        font=("Arial", 18, "bold"),
        corner_radius=20,
        fg_color="#00ADB5",
        text_color="white",
        width=150,
        height=30,
        command=eliminarArbol
    )
    btn_eliminar_arbol.place(x=480, y=440)

    ventana.mainloop()

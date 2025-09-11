import tkinter as tk
from tkinter import messagebox
import heapq
import random
import customtkinter as ctk


ESTADO_META = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

#Encontrar la posición del cero en el estado, el cuadro vacío
def encontrar_cero(estado):
    for fila in range(3):
        for columna in range(3):
            if estado[fila][columna] == 0:
                return fila, columna

def es_resoluble(estado):
    plano = sum(estado, [])
    conteo_inversiones = 0
    for i in range(8):
        for j in range(i+1, 9):
            if plano[i] and plano[j] and plano[i] > plano[j]:
                conteo_inversiones += 1
    return conteo_inversiones % 2 == 0

#Función heurística: distancia Manhattan, para sacar el costo de cada estado
def manhattan(estado):
    distancia = 0
    for fila in range(3):
        for columna in range(3):
            valor = estado[fila][columna]
            if valor != 0:
                meta_fila = (valor - 1) // 3
                meta_columna = (valor - 1) % 3
                distancia += abs(fila - meta_fila) + abs(columna - meta_columna)
    return distancia

#Guarda los vecinos del estado actual
def vecinos(estado):
    fila_cero, columna_cero = encontrar_cero(estado)
    movimientos = []
    for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nueva_fila, nueva_columna = fila_cero+df, columna_cero+dc #Se guarda la nueva posición del cero
        if 0 <= nueva_fila < 3 and 0 <= nueva_columna < 3: #Verifica que la nueva posición esté dentro de los límites
            nuevo_estado = [fila[:] for fila in estado]
            nuevo_estado[fila_cero][columna_cero], nuevo_estado[nueva_fila][nueva_columna] = nuevo_estado[nueva_fila][nueva_columna], nuevo_estado[fila_cero][columna_cero]
            movimientos.append(nuevo_estado)
    return movimientos

#Convierte el estado(matriz) a una tupla
def estado_a_tupla(estado):
    return tuple(tuple(fila) for fila in estado)

def astar(inicio):
    estadoActual = []  # Es una lista que se usa como cola de prioridad, guarda todas las posibles soluciones
    heapq.heappush(estadoActual, (manhattan(inicio), 0, inicio, []))  # Agrega el primer elemento a la lista, que es el estado inicial
    visitados = []
    while estadoActual:  # Mientras la lista no este vacia
        f, g, actual, camino = heapq.heappop(estadoActual)  # Elimina el elemento con menor costo(f) y elimina los demas
        if actual == ESTADO_META:
            return camino + [actual]  # Camino es la lista con todo su recorrido hasta llegar al estado meta
        est = estado_a_tupla(actual)
        if est in visitados:
            continue
        visitados.append(est)
        for vecino in vecinos(actual):
            if estado_a_tupla(vecino) not in visitados:
                heapq.heappush(estadoActual, (g+1+manhattan(vecino), g+1, vecino, camino + [actual]))  # Agrega los vecinos del estado actual a la lista
    return None

#INTERFAZ GRÁFICA
class Puzzle8GUI:
    def __init__(self, master):
        self.master = master
        master.title("Puzzle 8 - Búsqueda A*")
        self.estado = [
            [1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]
        ]
        self.botones = [[None]*3 for _ in range(3)]
        self.etiqueta_movimientos = None
        self.crear_widgets()
        self.actualizar_botones()

    def crear_widgets(self):
        marco = tk.Frame(self.master)
        marco.pack(padx=10, pady=5)
        for fila in range(3):
            for columna in range(3):
                btn = tk.Button(
                    marco,
                    width=4,
                    height=2,
                    font=("Arial", 24),
                    command=lambda x=fila, y=columna: self.mover_ficha(x, y)
                )
                
                btn.grid(row=fila, column=columna)
                self.botones[fila][columna] = btn
                
        
        self.etiqueta_movimientos = tk.Label(
            self.master,
            text="Movimientos: 0",
            font=("Arial", 14)
        )
        self.etiqueta_movimientos.pack(pady=10)

        ctk.CTkButton(
            self.master,
            text="Resolver",
            font=("Arial", 18, "bold"),
            corner_radius=20,
            fg_color="#00ADB5",
            text_color="white",
            width=180,
            height=40,
            command=self.resolver
        ).pack(pady=10)

        ctk.CTkButton(
            self.master,
            text="Mezclar",
            font=("Arial", 18, "bold"),
            corner_radius=20,
            fg_color="#00ADB5",
            text_color="white",
            width=180,
            height=40,
            command=self.mezclar
        ).pack(pady=10)


    def actualizar_botones(self):
        for fila in range(3):
            for columna in range(3):
                valor = self.estado[fila][columna]
                self.botones[fila][columna]['text'] = str(valor) if valor != 0 else ""
                self.botones[fila][columna]['bg'] = "SystemButtonFace" if valor != 0 else "lightgray"

    def mover_ficha(self, fila, columna):
        fila_cero, columna_cero = encontrar_cero(self.estado)
        if abs(fila_cero - fila) + abs(columna_cero - columna) == 1:
            self.estado[fila_cero][columna_cero], self.estado[fila][columna] = self.estado[fila][columna], self.estado[fila_cero][columna_cero]
            self.actualizar_botones()
            if self.estado == ESTADO_META:
                messagebox.showinfo("¡Felicidades!", "¡Has resuelto el puzzle!")

    def resolver(self):
        if not es_resoluble(self.estado):
            messagebox.showerror("Error", "Este puzzle no es resoluble.")
            return
        solucion = astar(self.estado)
        if not solucion:
            messagebox.showerror("Error", "No se encontró solución.")
            return
        self.animar_solucion(solucion)

    def animar_solucion(self, solucion):
        def paso(idx):
            if idx < len(solucion):
                self.estado = solucion[idx]
                self.actualizar_botones()
                self.etiqueta_movimientos['text'] = f"Movimientos: {idx}"
                self.master.after(250, lambda: paso(idx+1))
            else:
                messagebox.showinfo("Resuelto", "Puzzle resuelto con A*.")
        paso(0)

    def mezclar(self):
        plano = list(range(9))
        while True:
            random.shuffle(plano)
            estado = [plano[:3], plano[3:6], plano[6:]]
            if es_resoluble(estado):
                self.estado = estado
                self.actualizar_botones()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = Puzzle8GUI(root)
    root.mainloop()

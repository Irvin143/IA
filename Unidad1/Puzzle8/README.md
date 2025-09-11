
## Integrantes
- Irvin Jair Carrillo Beltran
- Jesús Omar Langarica Ornelas
# Proyecto Puzzle 8

Este proyecto es una implementación del juego del **Puzzle 8** con una interfaz gráfica desarrollada en Tkinter y CustomTkinter.
El objetivo principal es resolver el rompecabezas utilizando el **algoritmo de búsqueda A***  con la distancia **Manhattan** como heurística.


## Imagenes
<img width="209" height="379" alt="Image" src="https://github.com/user-attachments/assets/6a746d6e-c1f1-4fbd-a568-e8541191a584" />




## Estructura general del codigo
**1.Funciones de lógica del puzzle**

- Manejo de estados del tablero.

- Verificación de resolubilidad.

- Generación de vecinos.

- Implementación del algoritmo A*.

**2.Interfaz gráfica**

- Creación de la ventana y botones del tablero.

- Interacción con el usuario (mover fichas manualmente).

- Botones para mezclar el tablero y resolver automáticamente.

- Animación paso a paso de la solución.

## Metodos

- encontrar_cero: Localiza la posición del espacio vacío en el tablero.
- copiar_estado: Crea una copia del estado actual para manipular sin alterar el original.
- es_resoluble: Verifica si una configuración del puzzle se puede resolver.
- manhattan: Calcula la distancia Manhattan como heurística para el algoritmo A*.
- vecinos: Genera todos los posibles estados vecinos moviendo la casilla vacía.
- estado_a_tupla: Convierte el tablero en tuplas para poder guardarlos como visitados.
- astar: Implementa el algoritmo de búsqueda A* para encontrar la solución más corta.  

- crear_widgets: Crea botones del tablero y controles.
- actualizar_botones: Refresca los valores mostrados en los botones.
- mover_ficha: Permite mover manualmente las fichas.
- resolver: Llama al algoritmo A* y muestra la solución.
- animar_solucion: Muestra paso a paso el proceso de resolución.
- mezclar: Genera un tablero aleatorio válido.




## Funcionamiento del algoritmo de busqueda
El algoritmo implementado es A*, que combina:

- Costo acumulado (g): Número de movimientos realizados desde el inicio.

- Heurística (h): Distancia Manhattan, que mide cuán lejos está cada ficha de su posición objetivo.

- Función de evaluación (f): f = g + h, utilizada para priorizar los estados más prometedores.

**Proceso:**

1.Se inicia con el estado actual del tablero.

2.Se expanden sus vecinos (posibles movimientos de la ficha vacía).

3.Se selecciona el siguiente estado con el menor valor de f.

4.Se repite el proceso hasta llegar al estado meta.

5.El resultado es la secuencia óptima de movimientos que resuelve el puzzle.

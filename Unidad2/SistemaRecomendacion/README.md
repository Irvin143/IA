
## Integrantes
- Irvin Jair Carrillo Beltran
- Jesús Omar Langarica Ornelas
# Proyecto Unidad 2 Sistema de Recomendación

En este proyecto desarrollamos un Sistema de Recomendación de Platillos en Python con la biblioteca CustomTkinter para la interfaz gráfica. Su objetivo es sugerir platillos personalizados a los usuarios con base en sus gustos culinarios y restricciones alimenticias. El sistema utiliza archivos JSON para representar los datos de los platillos, ingredientes y sabores, lo que permite un funcionamiento sin dependencia de bases de datos externas. 


# Imagenes
<img width="998" height="498" alt="Image" src="https://github.com/user-attachments/assets/bca517e7-cc5d-43ba-bfe0-23fb41e5c0f5" />
<img width="998" height="279" alt="Image" src="https://github.com/user-attachments/assets/ce0af439-0c70-4cb6-a267-df7dc7d0a05b" />





## Estructura general del codigo
* **Interfaz.py:** Clase principal que levanta la interfaz gráfica.
* **Frame.py:** Crea los selectores de gustos, ingredientes y restricciones.
* **TablaRecomendacion.py:** Muestra las recomendaciones en una tabla con scroll.
* **Recomendacion.py:** Contiene la lógica del sistema de recomendación
* **Archivos JSON:** Almacenan los datos de entrada (platillos, sabores, ingredientes).


## Flujo de funcionamiento
**1.** El usuario selecciona sus gustos y restricciones.

**2.** El sistema procesa los datos y calcula probabilidades de afinidad con cada platillo. 

**3.** Se muestran los platillos recomendados en una tabla con detalles.

## Dependencias
* customtkinter
* tkinter
* json
* pathlib

## Manual de Usuario
**1.** 	Ejecuta el programa interfaz.py  

**2.**	Se abrirá una ventana con varios apartados:
* Gustos Culinarios: selecciona sabores o ingredientes que te gusten.
* Restricciones: selecciona los sabores que no quieres.      

**3.**  Restricciones Dietéticas: selecciona si eres vegetariano, vegano, etc.  

**4.** Presiona el botón "Obtener Recomendaciones".

**5.**	Observa los resultados en la tabla inferior con los detalles de los platillos sugeridos.

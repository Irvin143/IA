## Integrantes
- Irvin Jair Carrillo Beltran
- Jesús Omar Langarica Ornelas
# Proyecto Unidad 3 Sistema Experto

En este proyecto para la Unidad 3 realizamos un Sistema Experto para el diagnóstico de enfermedades respiratorias simulando el proceso de razonamiento de un medico especialista utilizando Inteligencia Artificial para la precisión y eficiencia de los diagnósticos realizados por nuestro sistema.

# Imagenes
<img width="660" height="422" alt="Image" src="https://github.com/user-attachments/assets/765b80e0-76d4-455f-a83a-fc74913f8998" />

<img width="664" height="423" alt="Image" src="https://github.com/user-attachments/assets/383cd150-e331-4803-9f4d-148c6cda76d2" />

<img width="621" height="484" alt="Image" src="https://github.com/user-attachments/assets/527087d0-31e8-4b76-9bc5-ca04bde27f0d" />

## Estructura general del codigo
**1. base_conocimiento.py:** Contiene toda la información médica del sistema:

* REGLAS_PRODUCCION: Reglas de diagnóstico para cada enfermedad (condiciones, factor de certeza)
* INFORMACION_ENFERMEDADES: Detalles de cada enfermedad (descripción, hallazgos, recomendaciones, urgencia)
* SINTOMAS_DISPONIBLES: Diccionario de síntomas con sus preguntas
* FACTORES_RIESGO_DISPONIBLES: Diccionario de factores de riesgo con sus preguntas
* REGLAS_OMISION: Lógica para evitar preguntas redundantes

**2. motor_inferencia.py:** Implementa la lógica de razonamiento:

* evaluar_regla(): Verifica si una regla se cumple (umbral 75%)
* calcular_factor_certeza_combinado(): Combina múltiples factores de certeza usando la fórmula FC(A,B) = FC(A) + FC(B) × (1 - FC(A))
* diagnosticar(): Evalúa todas las reglas, ajusta factores de certeza, combina evidencias y retorna diagnósticos ordenados
* obtener_info_enfermedad(): Recupera información detallada de una enfermedad

**3. interfaz.py:** Maneja la interacción con el usuario mediante Tkinter:

* Pantalla de bienvenida
* Cuestionario interactivo con preguntas Sí/No
* Lógica para omitir preguntas redundantes
* Pantalla de resultados con diagnósticos, * factores de certeza y recomendaciones

**4. main.py:** Punto de entrada que coordina todo el sistema:

* Importa todos los componentes
* Instancia el motor de inferencia
* Crea y ejecuta la interfaz gráfica


## Flujo de ejecución
El flujo general del sistema sigue esta secuencia:
* El usuario ejecuta main.py que instancia todos los componentes, la interfaz muestra la pantalla de bienvenida
* El usuario inicia el cuestionario que presenta preguntas una por una aplicando las reglas de omisión inteligentes, cada respuesta afirmativa actualiza los datos del usuario y las preguntas a omitir
* Al completar todas las preguntas relevantes se invoca el motor de inferencia que evalúa reglas, calcula factores de certeza ajustados, combina evidencias múltiples y genera diagnósticos ordenados por probabilidad
* Finalmente la interfaz presenta los resultados de forma completa y transparente con opciones para realizar una nueva consulta o salir del sistema.
## Librerias
* tkinter


## Integrantes
- Irvin Jair Carrillo Beltran
- Jesús Omar Langarica Ornelas

# Tarea 3 Detector de Spam
En este proyecto desarrollamos un detector de correos spam utilizando Python y diferentes librerías de análisis de texto, nuestra idea era hacer un programa que pueda identificar si un correo electrónico es malicioso o no, basándose en su contenido, asunto y remitente. Para lograr esto utilizamos herramientas como numpy, pandas y scikit-learn, que ayudan a procesar los datos y a representar el texto mediante el modelo TF-IDF, el cual permite analizar qué tan importantes son las palabras dentro de un mensaje. 


# Imagenes
<img width="745" height="784" alt="Image" src="https://github.com/user-attachments/assets/7ed6de8a-9f2a-4406-8e98-66ed6526fa00" />
<img width="526" height="555" alt="Image" src="https://github.com/user-attachments/assets/0b9a36f4-3953-493f-8a9d-704b0e3ff65e" />

## Estructura general del codigo
* Entrenamiento con dataset CSV (train.csv) que contiene ejemplos de mensajes spam y no spam.

* Análisis de texto avanzado: limpieza, lematización y eliminación de stopwords (palabras vacías).

* Dos modos de razonamiento:

    * Razonamiento No Monótono: usa un modelo probabilístico con TF-IDF y frecuencias de palabras para calcular la probabilidad de spam.

    * Razonamiento Monótono: aplica reglas lógicas predefinidas (patrones comunes en correos spam).

* Interfaz gráfica: desarrollada con CustomTkinter, permite introducir remitente, asunto y contenido del correo.

* Extracción automática de texto desde URLs 

## Reglas
1.	Detección de enlaces sospechosos o dominios poco confiables.
2.	Presencia de frases persuasivas como “hazlo ahora”, “oferta especial” o “gana”.
3.	Exceso de signos de exclamación o interrogación.
4.	Menciones relacionadas con dinero o premios (“has ganado”, “transferencia bancaria”, “bitcoin”).
5.	Dominios de correo extraños (como “@xyz”, “@top”, “@click”).
6.	Uso excesivo de mayúsculas, lo que suele ser típico en mensajes engañosos.
7.	Empleo de emojis llamativos.
8.	Palabras que transmiten urgencia o presión, como “última oportunidad” o “solo hoy”.
9.	Correos con demasiados números o caracteres raros en el nombre del remitente.
10.	Exceso de enlaces dentro del mensaje (más de tres).


## Dependencias
* pip install numpy
* pip install pandas
* pip install scikit-learn
* pip install nltk
* pip install requests
* pip install beautifulsoup4
* pip install customtkinter

* python -m nltk.downloader stopwords wordnet
## Componentes
**Clase DetectorSpam**
* preProcesar(texto) → limpia y lematiza el texto.

* extraer_texto_desde_url(url) → obtiene el texto desde una página web.

* razonamientoMonotono(correo) → aplica reglas predefinidas para detectar spam.

* razonamientoNoMonotono(correo) → utiliza probabilidades y TF-IDF.

* detectar(correo, razonamiento) → ejecuta la detección según el tipo elegido.

**Clase Interfaz**

* Crear la ventana principal con CustomTkinter.

* Mostrar campos de entrada y botones.

* Conectar la interfaz con el detector de spam.
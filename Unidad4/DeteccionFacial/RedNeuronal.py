import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import os

# Se definen las rutas donde están las imágenes de entrenamiento y prueba
train_dir = "IA/Unidad4/DeteccionFacial/dataset/train"
test_dir = "IA/Unidad4/DeteccionFacial/dataset/test"

# Se crea un generador de datos para entrenamiento con aumento de imágenes
# Esto mejora la capacidad del modelo para generalizar al agregar variaciones artificiales
train_datagen = ImageDataGenerator(
    rescale=1./255,              # normaliza los valores de píxeles entre 0 y 1
    rotation_range=20,           # rota aleatoriamente las imágenes hasta 20 grados
    zoom_range=0.2,              # aplica zoom aleatorio
    horizontal_flip=True         # invierte imágenes horizontalmente
)

# Para las imágenes de prueba solo se normalizan, sin aumentos
test_datagen = ImageDataGenerator(rescale=1./255)

# Se crea el generador para el conjunto de entrenamiento
# flow_from_directory carga las imágenes directamente desde las carpetas organizadas por clase
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(48, 48),        # Todas las imágenes se redimensionan a 48x48 píxeles
    color_mode="grayscale",      # Las imágenes se convierten a escala de grises
    class_mode="categorical",    # Las etiquetas se codifican como categorías 
    batch_size=32                # Tamaño de lote para el entrenamiento
)

# Se crea el generador para el conjunto de prueba
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(48, 48),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=32
)

# Se construye el modelo de red neuronal convolucional (CNN)
# Sequential indica que las capas se agregan en orden
modelo = models.Sequential([
    # Primera capa convolucional con 32 filtros
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(48,48,1)),
    # Reduce la dimensión espacial manteniendo la información importante
    layers.MaxPooling2D(2,2),

    # Segunda capa convolucional con 64 filtros
    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),

    # Tercera capa convolucional con 128 filtros
    layers.Conv2D(128, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),

    # Aplana las características obtenidas de las capas convolucionales
    layers.Flatten(),
    # Capa completamente conectada de 128 neuronas
    layers.Dense(128, activation="relu"),
    # Dropout para evitar sobreajuste apagando el 30% de neuronas aleatoriamente
    layers.Dropout(0.3),
    # Capa de salida con 4 neuronas para las clases: angry, happy, neutral y sad
    layers.Dense(4, activation="softmax")
])

# Se compila el modelo definiendo el optimizador, la función de pérdida y la métrica
modelo.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"] #Se usa la metrica accuracy
)

# Muestra un resumen de las capas del modelo
modelo.summary()

# Se entrena el modelo usando las imágenes del generador
# validation_data permite evaluar el rendimiento en el conjunto de prueba cada epoch
entrenamiento = modelo.fit(
    train_generator,
    epochs=40,
    validation_data=test_generator
)

# Se guarda el modelo entrenado en un archivo .h5
modelo.save("IA/Unidad4/DeteccionFacial/modelo_emociones.h5")

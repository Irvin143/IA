import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import os

# Rutas del dataset
train_dir = "IA/Unidad4/DeteccionFacial/dataset/train"
test_dir = "IA/Unidad4/DeteccionFacial/dataset/test"

# Generador de imágenes
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(48, 48),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=32
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(48, 48),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=32
)

# Red neuronal CNN
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(48,48,1)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(4, activation="softmax")   # angry, happy, neutral, sad
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Entrenamiento
history = model.fit(
    train_generator,
    epochs=40,
    validation_data=test_generator
)

# Guardar modelo
model.save("IA/Unidad4/DeteccionFacial/modelo_emociones.h5")

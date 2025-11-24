import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tensorflow import keras
import matplotlib.pyplot as plt

# Configuración para estabilidad
tf.keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

# ----------------------------
# 1. CARGAR Y ANALIZAR FER2013
# ----------------------------

ruta = r"IA/Unidad4/DeteccionFacial/dataset/fer2013.csv"
data = pd.read_csv(ruta)

print("=== ANÁLISIS DEL DATASET ===")
print(f"Total de imágenes: {len(data)}")
print("\nDistribución de emociones:")
conteo = data['emotion'].value_counts().sort_index()
clases = ['Enojo', 'Disgusto', 'Miedo', 'Feliz', 'Triste', 'Sorprendido', 'Neutral']
for i, clase in enumerate(clases):
    print(f"{i} - {clase}: {conteo[i]} ({conteo[i]/len(data)*100:.1f}%)")

# ----------------------------
# 2. PREPROCESAMIENTO
# ----------------------------

imagenes = []
for pixels in data['pixels']:
    img = np.fromstring(pixels, dtype=np.uint8, sep=' ').reshape((48, 48))
    imagenes.append(img)

imagenes = np.array(imagenes, dtype="float32")

# Normalización [0, 1]
imagenes = imagenes / 255.0
imagenes = np.expand_dims(imagenes, -1)

# One-hot encoding
emociones = keras.utils.to_categorical(data['emotion'], num_classes=7)

# Split estratificado
X_train, X_val, y_train, y_val = train_test_split(
    imagenes, emociones, 
    test_size=0.2, 
    random_state=42, 
    shuffle=True,
    stratify=data['emotion']
)

print(f"\nTrain: {X_train.shape}, Val: {X_val.shape}")

# ----------------------------
# 3. CLASS WEIGHTS (CRUCIAL)
# ----------------------------

pesos_clase = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(data['emotion']),
    y=data['emotion']
)
class_weights = dict(enumerate(pesos_clase))
print("\n=== PESOS DE CLASE ===")
for i, peso in class_weights.items():
    print(f"{clases[i]}: {peso:.2f}")

# ----------------------------
# 4. DATA AUGMENTATION MODERADO
# ----------------------------

datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)
datagen.fit(X_train)

# ----------------------------
# 5. ARQUITECTURA OPTIMIZADA
# ----------------------------

def crear_modelo():
    modelo = keras.Sequential([
        # Bloque 1
        keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same', 
                           input_shape=(48, 48, 1)),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.3),

        # Bloque 2
        keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.3),

        # Bloque 3
        keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        keras.layers.BatchNormalization(),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.4),

        # Dense layers
        keras.layers.Flatten(),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.5),
        
        keras.layers.Dense(7, activation='softmax')
    ])
    
    return modelo

modelo = crear_modelo()

# Compilar con learning rate bajo
modelo.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)


# ----------------------------
# 6. CALLBACKS
# ----------------------------

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=20,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ModelCheckpoint(
        "IA/Unidad4/DeteccionFacial/modelo/mejor_modelo.keras",
        save_best_only=True,
        monitor='val_loss',
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=8,
        min_lr=1e-7,
        verbose=1
    )
]

# ----------------------------
# 7. ENTRENAMIENTO
# ----------------------------

print("\n=== INICIANDO ENTRENAMIENTO ===")

history = modelo.fit(
    datagen.flow(X_train, y_train, batch_size=64),
    steps_per_epoch=len(X_train) // 64,
    validation_data=(X_val, y_val),
    epochs=100,
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
)


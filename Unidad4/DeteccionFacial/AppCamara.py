import cv2
import numpy as np
import tensorflow as tf
from collections import deque, Counter

# Cargar modelo
model = tf.keras.models.load_model("IA/Unidad4/DeteccionFacial/modelo_emociones.h5")

# Diccionario de emociones
emociones = ["angry", "happy", "neutral", "sad"]

# Buffer para suavizar predicciones (últimas 10)
prediction_buffer = deque(maxlen=10)

# Cargar detector de rostro
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Iniciar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostros = face_cascade.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
        # Dibujar recuadro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

        rostro = gris[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (48, 48))
        rostro = rostro.reshape(1, 48, 48, 1) / 255.0

        pred = model.predict(rostro, verbose=0)
        emocion = emociones[np.argmax(pred)]

        # Guardar emoción en buffer
        prediction_buffer.append(emocion)

        # Emoción más repetida en últimas N predicciones
        emocion_estable = Counter(prediction_buffer).most_common(1)[0][0]

        # Colocar texto más estable
        cv2.putText(frame, emocion_estable, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Detector de emociones", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

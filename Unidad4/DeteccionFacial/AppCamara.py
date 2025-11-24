import cv2
import numpy as np
import tensorflow as tf

# Cargar modelo entrenado
modelo = tf.keras.models.load_model("IA/Unidad4/DeteccionFacial/modelo/mejor_modelo.keras")

clases = ['enojo', 'miedo', 'feliz', 'triste', 'sorprendido']

# Detector de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Captura de video
cap = cv2.VideoCapture(0)

while True: 
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (48, 48))
        rostro = rostro / 255.0
        rostro = np.expand_dims(rostro, axis=(0, -1))

        pred = modelo.predict(rostro, verbose=0)
        clase = np.argmax(pred)
        confianza = pred[0][clase]

        # Filtro para mostrar solo las predicciones confiables
        if confianza > 0.5:  
            etiqueta = f'{clases[clase]} ({confianza:.2f})'
        else:
            etiqueta = "Inseguro"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, etiqueta, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 0), 2)

    cv2.imshow("Reconocimiento de Expresiones", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

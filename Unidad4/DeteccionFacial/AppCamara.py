import cv2
import numpy as np
import tensorflow as tf

# Cargar modelo
modelo = tf.keras.models.load_model("IA/Unidad4/DeteccionFacial/modelo/mejor_modelo.keras")

# Clases FER2013 (ORDEN CORRECTO: 0-6)
clases = ['enojo', 'disgusto', 'miedo', 'feliz', 'triste', 'sorprendido', 'neutral']

# Detector de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Captura de cámara
cap = cv2.VideoCapture(0)

# Variables para suavizado temporal
ventana_predicciones = []
TAMANO_VENTANA = 5  # Promedia últimas 5 predicciones

print("Presiona 'q' para salir")
print("Mostrando todas las probabilidades para debug...\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detección de rostros
    faces = face_cascade.detectMultiScale(
        gris,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:
        rostro = gris[y:y+h, x:x+w]

        # Expandir el ROI del rostro (captura más contexto)
        padding = int(h * 0.2)
        y1 = max(0, y - padding)
        y2 = min(gris.shape[0], y + h + padding)
        x1 = max(0, x - padding)
        x2 = min(gris.shape[1], x + w + padding)
        rostro = gris[y1:y2, x1:x2]

        # Redimensionar PRIMERO
        rostro = cv2.resize(rostro, (48, 48), interpolation=cv2.INTER_AREA)
        
        # DESPUÉS mejorar contraste
        rostro = cv2.equalizeHist(rostro)
        
        # Aplicar filtro bilateral para reducir ruido
        rostro = cv2.bilateralFilter(rostro, 5, 50, 50)

        # Normalizar EXACTAMENTE igual que en entrenamiento
        rostro = rostro.astype("float32") / 255.0

        # Reshape para el modelo (1, 48, 48, 1)
        rostro_input = np.expand_dims(rostro, axis=0)
        rostro_input = np.expand_dims(rostro_input, axis=-1)

        # Predicción
        pred = modelo.predict(rostro_input, verbose=0)[0]
        
        # Agregar a ventana de suavizado
        ventana_predicciones.append(pred)
        if len(ventana_predicciones) > TAMANO_VENTANA:
            ventana_predicciones.pop(0)
        
        # Promediar predicciones
        pred_suavizada = np.mean(ventana_predicciones, axis=0)
        
        clase = np.argmax(pred_suavizada)
        confianza = pred_suavizada[clase]

        # MOSTRAR TODAS LAS PROBABILIDADES EN CONSOLA (para debug)
        print("\n--- Probabilidades ---")
        for i, prob in enumerate(pred_suavizada):
            print(f"{clases[i]}: {prob:.3f}")
        print(f"Predicción final: {clases[clase]} ({confianza:.3f})")

        # Etiqueta principal con umbral
        if confianza < 0.35:
            etiqueta = "Indefinido"
            color = (128, 128, 128)
        else:
            etiqueta = f"{clases[clase]}: {confianza:.2f}"
            color = (0, 255, 0) if confianza > 0.5 else (0, 165, 255)

        # Dibujar rectángulo y texto
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(
            frame,
            etiqueta,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        # Mostrar top 3 emociones en el frame
        top_3_indices = np.argsort(pred_suavizada)[-3:][::-1]
        y_offset = y + h + 25
        
        for idx in top_3_indices:
            texto_prob = f"{clases[idx]}: {pred_suavizada[idx]:.2f}"
            cv2.putText(
                frame,
                texto_prob,
                (x, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
            y_offset += 20

    cv2.imshow("Deteccion de Emociones", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
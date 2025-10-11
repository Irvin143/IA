import os
import customtkinter as ctk

from DetectarSpam import DetectorSpam

from DetectarSpam import DetectorSpam

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class Interfaz(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Detector de Spam")
        self.geometry("500x500")
        self.configure(bg="#f5f5f5")

        # Apartado para ingresar el correo remitente
        ctk.CTkLabel(self, text="Correo remitente:", font=("Arial", 14)).pack(pady=5)
        self.sender_entry = ctk.CTkEntry(self, width=400)
        self.sender_entry.pack(pady=5)

        # Apartado para ingresar el asunto
        ctk.CTkLabel(self, text="Asunto del correo:", font=("Arial", 14)).pack(pady=5)
        self.subject_entry = ctk.CTkEntry(self, width=400)
        self.subject_entry.pack(pady=5)

        # Apartado para ingresar el contenido del correo
        ctk.CTkLabel(self, text="Contenido del correo:", font=("Arial", 14)).pack(pady=5)
        
        self.email_content = ctk.CTkTextbox(self, width=400, height=100)
        self.email_content.pack(pady=5)

        # Radio buttons para seleccionar el tipo de razonamiento
        self.razonamiento_var = ctk.StringVar(value="monotono")
        ctk.CTkLabel(self, text="Tipo de razonamiento:", font=("Arial", 14)).pack(pady=5)
        ctk.CTkRadioButton(self, text="Monótono", variable=self.razonamiento_var, value="monotono").pack(pady=2)
        ctk.CTkRadioButton(self, text="No monótono", variable=self.razonamiento_var, value="no_monotono").pack(pady=2)

        self.spam_result = ctk.CTkLabel(self, text="¿Es spam?:", font=("Arial", 14))
        self.spam_result.pack(pady=10)

        ctk.CTkButton(self, text="Detectar Spam", command=self.detect_spam).pack(pady=10)
        # Cache del detector para no recargar el dataset en cada detección
        self.detector = None

    def detect_spam(self):
        self.spam_result.configure(text=f"¿Es spam?:")
        # Validar que al menos uno de los campos tenga texto
        if not (self.sender_entry.get() or self.subject_entry.get() or self.email_content.get("1.0", "end-1c")):
            self.spam_result.configure(text="Por favor ingrese al menos un dato del correo.")
            return
        # Aquí iría la lógica de detección de spam
        dataset_path = os.path.join(os.path.dirname(__file__), "train.csv")
        if not os.path.exists(dataset_path):
            self.spam_result.configure(text=f"Archivo de datos no encontrado: {dataset_path}")
            return
        if self.detector is None:
            try:
                self.detector = DetectorSpam(dataset_path)
            except Exception as e:
                self.spam_result.configure(text=f"Error al cargar dataset: {e}")
                return

        email_text = f"{self.sender_entry.get()}, {self.subject_entry.get()}, {self.email_content.get('1.0', 'end-1c')}"
        resultado = self.detector.detectar(email_text, 1 if self.razonamiento_var.get() == "no_monotono" else 2)
        self.spam_result.configure(text=f"¿Es spam?: {resultado}")


if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()

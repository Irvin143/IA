import os                                   
import customtkinter as ctk                 
from DetectarSpam import DetectorSpam       

ctk.set_appearance_mode("light")            
ctk.set_default_color_theme("blue")         

class Interfaz(ctk.CTk):
    def __init__(self):
        super().__init__()                  
        self.title("Detector de Spam")      
        self.geometry("500x500")            
        self.configure(bg="#f5f5f5")        

        # Etiqueta y campo de texto para ingresar el correo remitente
        ctk.CTkLabel(self, text="Correo remitente:", font=("Arial", 14)).pack(pady=5)
        self.sender_entry = ctk.CTkEntry(self, width=400)  
        self.sender_entry.pack(pady=5)

        # Etiqueta y campo de texto para ingresar el asunto del correo
        ctk.CTkLabel(self, text="Asunto del correo:", font=("Arial", 14)).pack(pady=5)
        self.subject_entry = ctk.CTkEntry(self, width=400)
        self.subject_entry.pack(pady=5)

        # Etiqueta y área de texto para el contenido del correo
        ctk.CTkLabel(self, text="Contenido del correo:", font=("Arial", 14)).pack(pady=5)
        self.email_content = ctk.CTkTextbox(self, width=400, height=100)  
        self.email_content.pack(pady=5)

        # Variable para almacenar el tipo de razonamiento seleccionado
        self.razonamiento_var = ctk.StringVar(value="monotono")

        # Etiqueta y botones de selección para elegir el tipo de razonamiento
        ctk.CTkLabel(self, text="Tipo de razonamiento:", font=("Arial", 14)).pack(pady=5)
        ctk.CTkRadioButton(self, text="Monótono", variable=self.razonamiento_var, value="monotono").pack(pady=2)
        ctk.CTkRadioButton(self, text="No monótono", variable=self.razonamiento_var, value="no_monotono").pack(pady=2)

        # Etiqueta para mostrar el resultado del análisis de spam
        self.spam_result = ctk.CTkLabel(self, text="¿Es spam?:", font=("Arial", 14))
        self.spam_result.pack(pady=10)

        # Botón que ejecuta la detección de spam al hacer clic
        ctk.CTkButton(self, text="Detectar Spam", command=self.detect_spam).pack(pady=10)

        # Variable para almacenar una instancia del detector y no recargar el dataset cada vez
        self.detector = None

    # Función que se ejecuta al presionar el botón "Detectar Spam"
    def detect_spam(self):
        self.spam_result.configure(text=f"¿Es spam?:")   # Reinicia el texto del resultado

        # Valida que el usuario haya ingresado algún texto en al menos un campo
        if not (self.sender_entry.get() or self.subject_entry.get() or self.email_content.get("1.0", "end-1c")):
            self.spam_result.configure(text="Por favor ingrese al menos un dato del correo.")
            return  # Sale de la función si no hay texto

        # Construye la ruta hacia el archivo "train.csv"
        dataset_path = os.path.join(os.path.dirname(__file__), "train.csv")

        # Verifica que el archivo de datos exista
        if not os.path.exists(dataset_path):
            self.spam_result.configure(text=f"Archivo de datos no encontrado: {dataset_path}")
            return

        # Si el detector aún no ha sido cargado, lo inicializa
        if self.detector is None:
            try:
                self.detector = DetectorSpam(dataset_path)  # Crea una instancia del detector usando el dataset
            except Exception as e:
                # Si ocurre un error al cargar el dataset, muestra el mensaje de error
                self.spam_result.configure(text=f"Error al cargar dataset: {e}")
                return

        # Combina el remitente, asunto y contenido en un solo texto
        email_text = f"{self.sender_entry.get()}, {self.subject_entry.get()}, {self.email_content.get('1.0', 'end-1c')}"

        # Determina qué tipo de razonamiento usar según el radio button seleccionado
        resultado = self.detector.detectar(
            email_text,
            1 if self.razonamiento_var.get() == "no_monotono" else 2
        )

        # Muestra el resultado final en pantalla
        self.spam_result.configure(text=f"¿Es spam?: {resultado}")

if __name__ == "__main__":
    app = Interfaz()      
    app.mainloop()        

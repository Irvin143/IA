import unittest
import pandas as pd
import numpy as np
from DetectarSpam import DetectorSpam
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class DummyVectorizer:
    def transform(self, texts):
        # Return a fixed array for testing
        return np.array([[0.5, 0.5]])

class DummyDetectorSpam(DetectorSpam):
    def __init__(self):

        self.lematizador = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('spanish'))

        data = pd.read_csv(r"c:\VisualStudio\Python\BrayanIA\IA-Tareas\Unidad 2\Tarea 3\train.csv")
        data.columns = data.columns.str.strip() # Eliminar espacios en los nombres de las columnas
        self.vectorizador = TfidfVectorizer()
        caracteristicas = self.vectorizador.fit_transform(data["mensaje"])
        data["tipo"] = data["tipo"].map({"spam": 1, "ham": 0})
        y = data["tipo"].astype(int).values
        self.P_spam = np.sum(y) / len(y)
        self.P_no_spam = 1 - self.P_spam
        spam_arr = (y == 1)
        no_spam_arr = (y == 0)
        frecuencia_spam = np.sum(caracteristicas[spam_arr], axis=0)
        frecuencia_no_spam = np.sum(caracteristicas[no_spam_arr], axis=0)
        total_spam = frecuencia_spam.sum()
        total_no_spam = frecuencia_no_spam.sum()
        self.P_caracteristicas_spam = frecuencia_spam / total_spam
        self.P_caracteristicas_no_spam = frecuencia_no_spam / total_no_spam

    def preProcesar(self, texto):
        # Return text as is for testing
        return texto

    def extraer_texto_desde_url(self, url):
        # Simulate extracting text from URL
        return "oferta especial hazlo ahora"

class TestRazonamientoNoMonotono(unittest.TestCase):
    def setUp(self):
        self.detector = DummyDetectorSpam()

    def test_spam_detection(self):
        correo = "oferta especial hazlo ahora"
        resultado = self.detector.razonamientoNoMonotono(correo)
        self.assertEqual(resultado, "Spam")

    def test_no_spam_detection(self):
        # Adjust dummy probabilities to force "No Spam"
        self.detector.P_caracteristicas_spam = np.array([0.1, 0.1])
        self.detector.P_caracteristicas_no_spam = np.array([0.9, 0.9])
        correo = "hola amigo como estas"
        resultado = self.detector.razonamientoNoMonotono(correo)
        self.assertEqual(resultado, "No Spam")

    def test_url_input(self):
        correo = "http://example.com"
        resultado = self.detector.razonamientoNoMonotono(correo)
        self.assertEqual(resultado, "Spam")

if __name__ == "__main__":
    unittest.main()
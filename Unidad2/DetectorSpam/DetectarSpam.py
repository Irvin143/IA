import numpy as np                            # Para operaciones numéricas y manejo de matrices
import re                                     # Para usar expresiones regulares en detección de patrones
import pandas as pd                           # Para manejar datasets en formato CSV
from sklearn.feature_extraction.text import TfidfVectorizer  # Para convertir texto en vectores numéricos TF-IDF
from nltk.corpus import stopwords             # Para eliminar palabras irrelevantes (stopwords)
from nltk.stem import WordNetLemmatizer       # Para lematizar palabras (reducirlas a su forma base)
import requests                               # Para hacer solicitudes HTTP (descargar contenido web)
from bs4 import BeautifulSoup                 # Para extraer texto limpio del HTML

class DetectorSpam:
    def __init__(self, dataset_path):
        # Inicializa el lematizador
        self.lematizador = WordNetLemmatizer()
        # Carga las stopwords en español
        self.stop_words = set(stopwords.words('spanish'))

        # Carga el dataset desde la ruta indicada
        data = pd.read_csv(dataset_path)
        # Elimina espacios sobrantes en los nombres de las columnas
        data.columns = data.columns.str.strip()
        # Inicializa el vectorizador TF-IDF
        self.vectorizador = TfidfVectorizer()
        # Convierte los mensajes de texto a vectores numéricos
        caracteristicas = self.vectorizador.fit_transform(data["mensaje"])
        # Convierte las etiquetas “spam” y “ham” a 1 y 0 respectivamente
        data["tipo"] = data["tipo"].map({"spam": 1, "ham": 0})
        # Extrae las etiquetas como un array de enteros
        y = data["tipo"].astype(int).values

        # Calcula la probabilidad general de que un mensaje sea spam o no
        self.P_spam = np.sum(y) / len(y)
        self.P_no_spam = 1 - self.P_spam

        # Crea máscaras booleanas para separar los mensajes spam y no spam
        spam_arr = (y == 1)
        no_spam_arr = (y == 0)

        # Calcula la frecuencia total de palabras en los mensajes spam y no spam
        frecuencia_spam = np.sum(caracteristicas[spam_arr], axis=0)
        frecuencia_no_spam = np.sum(caracteristicas[no_spam_arr], axis=0)

        # Suma total de todas las frecuencias
        total_spam = frecuencia_spam.sum()
        total_no_spam = frecuencia_no_spam.sum()

        # Calcula las probabilidades de cada característica dado que es spam o no spam
        self.P_caracteristicas_spam = frecuencia_spam / total_spam
        self.P_caracteristicas_no_spam = frecuencia_no_spam / total_no_spam

    # Función para preprocesar el texto
    def preProcesar(self, texto):
        # Reemplaza todo lo que no sea letras o números por espacios
        texto = texto.str.replace("[^a-z0-9]", " ")
        # Divide el texto en listas de palabras
        texto = texto.str.split()
        # Lematiza y elimina stopwords, luego une las palabras en un solo string
        texto = texto.apply(lambda x: " ".join([self.lematizador.lemmatize(word) for word in x if word not in self.stop_words]))
        return texto

    # Extrae texto limpio desde una URL
    def extraer_texto_desde_url(self, url):
        try:
            # Realiza la solicitud HTTP con un tiempo límite de 5 segundos
            response = requests.get(url, timeout=5)
            # Analiza el HTML y lo convierte en texto limpio
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        except Exception:
            # Si hay un error, devuelve texto vacío
            return ""
        
    # Método con razonamiento monótono
    def razonamientoMonotono(self, correo):
        cont = 0                               # Contador de señales de spam
        correoNormal = correo                  # Guarda el texto original
        correo = correo.lower()                # Convierte todo a minúsculas

        # 1. Busca enlaces sospechosos
        if "builtit4unow.com" in correo or "wiildaccess.com" in correo:
            print("Posible spam: Enlace sospechoso encontrado.")
            cont += 1

        # 2. Detecta frases persuasivas comunes en spam
        if "gratis" in correo or "hazlo ahora" in correo or "oferta especial" in correo or "gana" in correo:
            print("Posible spam: Frase persuasiva encontrada.")
            cont += 1

        # 3. Detecta exceso de signos de exclamación o interrogación
        if "!!" in correo or "??" in correo:
            print("Posible spam: Exceso de signos de exclamación o interrogación.")
            cont += 1

        # 4. Detecta frases relacionadas con dinero o premios
        if "has ganado" in correo or "dinero" in correo or "transferencia bancaria" in correo or "bitcoin" in correo or "premio" in correo:
            print("Posible spam: Frases relacionadas con dinero o premios encontradas.")
            cont += 1

        # 5. Detecta dominios de correo sospechosos
        if "@xyz" in correo or "@top" in correo or "@click" in correo or "@info" in correo:
            print("Posible spam: Dirección de correo con dominio sospechoso.")
            cont += 1

        # 6. Detecta exceso de palabras completamente en mayúsculas
        palabras = correoNormal.split()
        mayusculas = sum(1 for palabra in palabras if palabra.isupper())
        if mayusculas > 3:
            print("Posible spam: Exceso de palabras en MAYÚSCULAS.")
            cont += 1

        # 7. Detecta uso de emojis llamativos
        if "💰" in correo or "🔥" in correo or "💵" in correo or "🎁" in correo:
            print("Posible spam: Uso de emojis llamativos.")
            cont += 1

        # 8. Detecta frases que generan urgencia
        if "urgente" in correo or "acción inmediata" in correo or "solo hoy" in correo or "ultima oportunidad" in correo:
            print("Posible spam: Uso de palabras que generan urgencia.")
            cont += 1

        # 9. Detecta direcciones de correo con muchos números o caracteres raros
        if re.search(r'[a-zA-Z]+[0-9]{3,}@', correo) or re.search(r'[a-zA-Z]+@[a-zA-Z0-9-]+\.(xyz|top|click|info)', correo):
            print("Posible spam: Dirección de correo con demasiados números o caracteres sospechosos.")
            cont += 1

        # 10. Detecta si hay más de 3 enlaces en el correo
        enlaces = correo.count("http")
        if enlaces > 3:
            print("Posible spam: Demasiados enlaces en el correo.")
            cont += 1

        # Resultado final
        if cont == 0:
            return ("El correo NO contiene spam.")
        else:
            return (f"Total de detecciones de spam: {cont} de 10 posibles.")
    
    # Método con razonamiento no monótono
    def razonamientoNoMonotono(self, correo):
        # Si el correo contiene una URL, se extrae su texto
        if "http://" in correo or "https://" in correo:
            correo = self.extraer_texto_desde_url(correo)

        # Preprocesa el texto del correo
        correo_proc = self.preProcesar(pd.Series([correo]))
        # Convierte el texto a vector TF-IDF
        correo_tfidf = self.vectorizador.transform(correo_proc)

        # Calcula la probabilidad de las características de ser spam
        P_caracteristicas_spam_correo = correo_tfidf @ self.P_caracteristicas_spam.T
        print("P_caracteristicas_spam_correo:", P_caracteristicas_spam_correo)

        # Calcula la probabilidad de las características de no ser spam
        P_caracteristicas_no_spam_correo = correo_tfidf @ self.P_caracteristicas_no_spam.T
        print("P_caracteristicas_no_spam_correo:", P_caracteristicas_no_spam_correo)

        # Calcula la probabilidad condicional de que el correo sea spam
        P_spam_caracteristicas = (self.P_spam * P_caracteristicas_spam_correo) / (
            (self.P_spam * P_caracteristicas_spam_correo) + (self.P_no_spam * P_caracteristicas_no_spam_correo) + 1e-100)

        # Convierte el resultado a número escalar
        prob_spam = np.squeeze(np.asarray(P_spam_caracteristicas))
        print("Probabilidad de spam dado el correo:", prob_spam)

        # Devuelve la clasificación según el umbral de 0.3
        return "Spam" if prob_spam > 0.3 else "No Spam"
    
    # Método principal que permite elegir el tipo de razonamiento
    def detectar(self, correo: str, razonamiento: int) -> str:
        # Si se elige 1, usa el razonamiento no monótono (probabilístico)
        if razonamiento == 1:
            return self.razonamientoNoMonotono(correo)
        # Si se elige 2, usa el razonamiento monótono (por reglas)
        if razonamiento == 2:
            return self.razonamientoMonotono(correo)

import numpy as np
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import requests
from bs4 import BeautifulSoup

class DetectorSpam:
    def __init__(self, dataset_path):
        self.lematizador = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('spanish'))

        data = pd.read_csv(dataset_path)
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
# ...existing code...
    #Funcion que preprocesa el texto para eliminar stopwords y lematizar, y asi dejar solo las palabras importantes
    def preProcesar(self, texto):
        texto = texto.str.replace("[^a-z0-9]", " ")
        texto = texto.str.split()
        texto = texto.apply(lambda x: " ".join([self.lematizador.lemmatize(word) for word in x if word not in self.stop_words]))
        return texto

    #Funcion que extrae el texto de una URL y lo devuelve como string su contenido
    def extraer_texto_desde_url(self, url):
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        except Exception:
            return ""
        
    #funcion para el razonamiento monotono
    def razonamientoMonotono(self, correo):
        cont = 0  # Contador de detecciones de spam
        correoNormal = correo # Guardar el correo original para análisis de mayusculas
        correo = correo.lower()  # Convertir a minúsculas para evitar problemas con mayúsculas

        # 1 Detectar enlaces sospechosos
        if "builtit4unow.com" in correo or "wiildaccess.com" in correo:
            print("Posible spam: Enlace sospechoso encontrado.")
            cont += 1

        # 2 Detectar frases persuasivas
        if "gratis" in correo or "hazlo ahora" in correo or  "oferta especial" in correo or "gana" in correo:
            print("Posible spam: Frase persuasiva encontrada.")
            cont += 1

        # 3 Detectar exceso de signos de exclamación o interrogación
        if "!!" in correo or "??" in correo:
            print("Posible spam: Exceso de signos de exclamación o interrogación.")
            cont += 1

        # 4 Detectar frases relacionadas con dinero o premios
        if "has ganado" in correo or "dinero" in correo or "transferencia bancaria" in correo or "bitcoin" in correo or "premio" in correo:
            print("Posible spam: Frases relacionadas con dinero o premios encontradas.")
            cont += 1

        # 5 Detectar direcciones de correo con dominios sospechosos
        if "@xyz" in correo or "@top" in correo or "@click" in correo or "@info" in correo:
            print("Posible spam: Dirección de correo con dominio sospechoso.")
            cont += 1

        # 6 Demasiadas palabras en MAYÚSCULAS
        palabras = correoNormal.split()
        mayusculas = sum(1 for palabra in palabras if palabra.isupper())
        if mayusculas > 3:  # Si hay más de 3 palabras en mayúsculas, podría ser spam
            print("Posible spam: Exceso de palabras en MAYÚSCULAS.")
            cont += 1

        # 7 Uso de emojis relacionados con dinero/regalos/ofertas
        if "💰" in correo or "🔥" in correo or "💵" in correo or "🎁" in correo:
            print("Posible spam: Uso de emojis llamativos.")
            cont += 1

        # 8 Palabras que crean urgencia
        if "urgente" in correo or "acción inmediata" in correo or "solo hoy" in correo or "ultima oportunidad" in correo:
            print("Posible spam: Uso de palabras que generan urgencia.")
            cont += 1

        # 9 Correos electrónicos con números extraños o caracteres raros
        if re.search(r'[a-zA-Z]+[0-9]{3,}@', correo) or re.search(r'[a-zA-Z]+@[a-zA-Z0-9-]+\.(xyz|top|click|info)', correo):
            print("Posible spam: Dirección de correo con demasiados números o caracteres sospechosos.")
            cont += 1

        # 10 Demasiados enlaces en el correo (más de 3)
        enlaces = correo.count("http")
        if enlaces > 3:
            print("Posible spam: Demasiados enlaces en el correo.")
            cont += 1

        # Resultado final
        if cont == 0:
            return ("El correo NO contiene spam.")
        else:
            return (f"Total de detecciones de spam: {cont} de 10 posibles.")
    
    #Funcion para el razonamiento no monotono
    def razonamientoNoMonotono(self, correo):
        """
        Analiza un correo electrónico para determinar la probabilidad de que sea spam utilizando razonamiento no monótono.

        Parámetros:
            correo (str): El texto del correo electrónico o una URL que contiene el correo.

        Detalles de cada línea:
            1. Si el correo contiene una URL (http:// o https://), extrae el texto del correo desde la URL usando el método extraer_texto_desde_url.
            2. Preprocesa el texto del correo convirtiéndolo en una serie de pandas y aplicando el método preProcesar para limpiar y normalizar el texto.
            3. Transforma el texto preprocesado en una representación vectorial TF-IDF usando el vectorizador previamente entrenado.
            4. Calcula la probabilidad de que las características del correo correspondan a spam mediante el producto matricial entre el vector TF-IDF y la matriz de características de spam.
            5. Calcula la probabilidad de que las características del correo correspondan a no spam mediante el producto matricial entre el vector TF-IDF y la matriz de características de no spam.
            6. Calcula la probabilidad final de que el correo sea spam usando la fórmula de probabilidad condicional, considerando las probabilidades previas y las características extraídas.
            7. Imprime la probabilidad calculada de que el correo sea spam.
            8. Retorna "Spam" si la probabilidad calculada es mayor a 0.3, de lo contrario retorna "No Spam".

        Retorno:
            str: "Spam" si el correo se clasifica como spam, "No Spam" en caso contrario.
        """
        if "http://" in correo or "https://" in correo:
            correo = self.extraer_texto_desde_url(correo)
        correo_proc = self.preProcesar(pd.Series([correo]))
        correo_tfidf = self.vectorizador.transform(correo_proc)

        P_caracteristicas_spam_correo = correo_tfidf @ self.P_caracteristicas_spam.T
        print("P_caracteristicas_spam_correo:", P_caracteristicas_spam_correo)

        P_caracteristicas_no_spam_correo = correo_tfidf @ self.P_caracteristicas_no_spam.T

        print("P_caracteristicas_no_spam_correo:", P_caracteristicas_no_spam_correo)
        P_spam_caracteristicas = (self.P_spam * P_caracteristicas_spam_correo) / (
            (self.P_spam * P_caracteristicas_spam_correo) + (self.P_no_spam * P_caracteristicas_no_spam_correo) + 1e-100)
        
        prob_spam = np.squeeze(np.asarray(P_spam_caracteristicas))
        print("Probabilidad de spam dado el correo:", prob_spam)
        return "Spam" if prob_spam > 0.3 else "No Spam"
    
    #Funcion principal para detectar spam
    def detectar(self, correo: str,razonamiento: int) -> str:
        if razonamiento == 1:  # No monótono
            return self.razonamientoNoMonotono(correo)
        if razonamiento == 2:  # Monótono
            return self.razonamientoMonotono(correo)




from base_conocimiento import (REGLAS_PRODUCCION, SINTOMAS_DISPONIBLES, FACTORES_RIESGO_DISPONIBLES, INFORMACION_ENFERMEDADES,REGLAS_OMISION)
from motor_inferencia import MotorInferencia
from interfaz import Interfaz

def main():
    motor = MotorInferencia(REGLAS_PRODUCCION, INFORMACION_ENFERMEDADES)
    interfaz = Interfaz(motor, SINTOMAS_DISPONIBLES, FACTORES_RIESGO_DISPONIBLES, REGLAS_OMISION)
    interfaz.ejecutar()

if __name__ == "__main__":
    main()
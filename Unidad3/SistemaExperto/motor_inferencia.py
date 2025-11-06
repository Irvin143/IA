class MotorInferencia:
    def __init__(self, reglas, informacion_enfermedades):
        # Constructor: guarda las reglas del sistema experto y la información
        # adicional sobre enfermedades (por ejemplo: síntomas, descripción, tratamiento).
        self.reglas = reglas
        self.informacion = informacion_enfermedades
        
    def evaluar_regla(self, condiciones, datos_usuario):
        """
        Evalúa si una regla se cumple con los datos del usuario.
        Retorna una tupla: (se_cumple, porcentaje_cumplimiento, condiciones_cumplidas)
        - se_cumple: booleano si la regla se considera activa (>=75% por defecto)
        - porcentaje: porcentaje de condiciones cumplidas (0-100)
        - condiciones_cumplidas: lista de condiciones presentes en los datos del usuario
        """
        total_condiciones = len(condiciones)     # número total de condiciones de la regla
        condiciones_cumplidas = []               # lista donde almacenaremos las condiciones que se cumplen
        
        # Recorremos cada condición y comprobamos si está presente en los datos del usuario
        for condicion in condiciones:
            if condicion in datos_usuario:
                condiciones_cumplidas.append(condicion)
        
        cumplidas = len(condiciones_cumplidas)   # cantidad de condiciones satisfechas
        # Evitamos división por cero: si total_condiciones = 0, porcentaje = 0
        porcentaje = (cumplidas / total_condiciones) * 100 if total_condiciones > 0 else 0
        
        # Regla de decisión: se considera cumplida si el porcentaje >= 75%
        se_cumple = porcentaje >= 75
        
        return se_cumple, porcentaje, condiciones_cumplidas
    
    def calcular_factor_certeza_combinado(self, factores_certeza):
        """
        Combina múltiples factores de certeza (FC) usando la fórmula iterativa:
        FC_combinado = FC1 + FC2 * (1 - FC1)
        Esta fórmula conserva la semántica de "aumentar la certeza" cuando se mezclan
        evidencias independientes.
        Entrada: factores_certeza -> lista de flotantes entre 0 y 1
        Retorna: fc_combinado -> flotante entre 0 y 1
        """
        if not factores_certeza:
            return 0.0  # sin factores, certeza nula
        
        fc_combinado = factores_certeza[0]  # iniciamos con el primer factor
        
        # iteramos a partir del segundo factor y aplicamos la fórmula recursiva
        for i in range(1, len(factores_certeza)):
            fc_combinado = fc_combinado + factores_certeza[i] * (1 - fc_combinado)
        
        return fc_combinado
    
    def diagnosticar(self, datos_usuario):
        """
        Realiza el diagnóstico usando reglas de producción.
        - Recorre todas las enfermedades y sus reglas asociadas.
        - Activa reglas cuyo cumplimiento >= 75% (según evaluar_regla).
        - Ajusta cada factor de certeza de la regla según el porcentaje de cumplimiento.
        - Combina factores de certeza activados para obtener un FC final por enfermedad.
        - Devuelve diagnósticos válidos (probabilidad >= 25%) ordenados por FC descendente.
        """
        resultados = {}  # diccionario para guardar resultados por enfermedad
        
        # Iteramos sobre cada enfermedad y sus reglas
        for enfermedad, reglas_enfermedad in self.reglas.items():
            reglas_activadas = []              # lista de reglas que se activaron para esta enfermedad
            factores_certeza_activados = []    # factores de certeza (ajustados) de reglas activadas
            
            # Revisamos cada regla asociada a la enfermedad
            for regla in reglas_enfermedad:
                se_cumple, porcentaje, condiciones_cumplidas = self.evaluar_regla(
                    regla['condiciones'], 
                    datos_usuario
                )
                
                if se_cumple:
                    # Ajustar el factor de certeza según el porcentaje real de cumplimiento.
                    # Si la regla tenía FC = 0.8 pero solo se cumple en 80% de condiciones,
                    # el FC ajustado será 0.8 * 0.8 = 0.64.
                    fc_ajustado = regla['factor_certeza'] * (porcentaje / 100)
                    factores_certeza_activados.append(fc_ajustado)
                    
                    # Guardamos información útil sobre la regla activada para trazabilidad
                    reglas_activadas.append({
                        'descripcion': regla['descripcion'],
                        'factor_certeza': regla['factor_certeza'],
                        'factor_certeza_ajustado': fc_ajustado,
                        'porcentaje_cumplimiento': porcentaje,
                        'condiciones_totales': len(regla['condiciones']),
                        # condiciones_cumplidas ya es una lista retornada por evaluar_regla
                        'condiciones_cumplidas': len(condiciones_cumplidas)
                    })
            
            if reglas_activadas:
                # Si existieron reglas activadas, combinamos sus factores de certeza
                fc_final = self.calcular_factor_certeza_combinado(factores_certeza_activados)
                
                resultados[enfermedad] = {
                    'factor_certeza': fc_final,         # FC combinado [0..1]
                    'probabilidad': fc_final * 100,     # probabilidad en porcentaje
                    'reglas_activadas': reglas_activadas,
                    'num_reglas_activadas': len(reglas_activadas)
                }
        
        # Ordenar resultados por factor de certeza de forma descendente
        diagnosticos_ordenados = sorted(
            resultados.items(),
            key=lambda x: x[1]['factor_certeza'],
            reverse=True
        )
        
        # Filtrar para devolver solo diagnósticos con probabilidad >= 25%
        diagnosticos_validos = [
            (enfermedad, datos) for enfermedad, datos in diagnosticos_ordenados
            if datos['probabilidad'] >= 25
        ]
        
        return diagnosticos_validos
    
    def obtener_info_enfermedad(self, enfermedad):
        """
        Obtiene información detallada de una enfermedad desde la estructura
        'informacion_enfermedades' pasada al inicializar la clase.
        Si no existe la enfermedad, retorna None.
        """
        if enfermedad in self.informacion:
            return self.informacion[enfermedad]
        return None

import json
from pathlib import Path

def recomendarPlatillos(lista_gustos, lista_restricciones, lista_dieteticos=[], lista_ingredientes=[]):
    # Obtiene la ruta del archivo Platillos.json dentro de la carpeta Json
    base_json_dir = Path(__file__).resolve().parent.parent / "Json"
    platillos_path = base_json_dir / "Platillos.json"

    # Carga el contenido del archivo JSON que contiene los platillos
    with open(platillos_path, "r", encoding="utf-8") as f:
        diccionario_platillos = json.load(f)

    # Calcula las probabilidades de recomendación para cada platillo
    probs_dict = probabilidadesPlatillos(
        lista_gustos,
        lista_restricciones,
        diccionario_platillos,
        lista_dieteticos,
        lista_ingredientes
    )

    # Si se obtuvieron resultados de probabilidad
    if probs_dict:
        # Determina la probabilidad más alta entre todos los platillos
        max_prob = max((v[0] for v in probs_dict.values()), default=0.0)
        ganadores = []
        aux_ganadores = []
        categoria = ""

        # Recorre los platillos para identificar los que tienen la máxima probabilidad
        for k, v in probs_dict.items():
            prob_norm, cat = v
            # Si el platillo tiene la probabilidad máxima o igual a ella, se considera ganador
            if (prob_norm == max_prob and prob_norm > 0) or prob_norm >= max_prob:
                aux_ganadores.append((k, cat))
                # Agrupa los ganadores por categoría
                if categoria != cat:
                    categoria = cat
                    ganadores.append(aux_ganadores)
                    aux_ganadores = []
    else:
        ganadores = []

    # Devuelve la información completa de los platillos ganadores
    return platillosGanadores(diccionario_platillos, ganadores)


def platillosGanadores(diccionario_platillos, ganadores):
    # Crea un mapa de acceso rápido con (nombre, categoría) como clave
    mapa = {}
    for p in diccionario_platillos:
        clave = (p.get("nombre", ""), p.get("categoria", ""))
        mapa[clave] = p

    resultados = []

    # Asegura que "ganadores" sea una lista de listas
    if ganadores and isinstance(ganadores[0], tuple):
        ganadores = [ganadores]

    # Recorre cada grupo de ganadores para recuperar la información detallada
    for grupo in ganadores:
        grupo_info = []
        for item in grupo:
            if not item:
                continue
            nombre, categoria = item
            plat = mapa.get((nombre, categoria))
            # Si se encuentra el platillo exacto, se añade al grupo
            if plat:
                grupo_info.append(plat)
            else:
                # Si no se encuentra, busca coincidencia por nombre
                for p in diccionario_platillos:
                    if p.get("nombre", "") == nombre:
                        grupo_info.append(p)
                        break
        # Agrega el grupo de platillos encontrados al resultado final
        if grupo_info:
            resultados.append(grupo_info)

    # Muestra los platillos ganadores en consola
    print("Platillos ganadores (detalles):", resultados)
    return resultados


def probabilidadesPlatillos(lista_gustos, lista_restricciones, diccionario_platillos, lista_dieteticos=[], lista_ingredientes=[]):
    #Calcula una puntuación probabilística para cada platillo según varios criterios
    probabilidades_platillos = {}
    total_general = 0.0

    #Pesos que determinan la importancia de cada criterio
    w_sabores = 0.6
    w_dieteticos = 0.4
    w_ingredientes = 0.5

    # Recorre cada platillo del JSON para calcular su probabilidad
    for platillo in diccionario_platillos:
        nombre = platillo.get("nombre", "")
        categoria = platillo.get("categoria", "")
        sabores = platillo.get("sabores", []) or []
        diet_tags = platillo.get("restricciones", []) or []
        ingredientes_plat = platillo.get("ingredientes", []) or []

        #Cálculo de afinidad de sabores (gustos vs restricciones)
        match_gustos = sum(1 for s in sabores if s in lista_gustos)
        match_restr = sum(1 for s in sabores if s in lista_restricciones)
        denom_sabores = len(sabores) or 1
        score_sabores = max((match_gustos - match_restr) / denom_sabores, 0.0)

        #Cálculo de coincidencias dietéticas
        if lista_dieteticos:
            match_diet = sum(1 for d in diet_tags if d in lista_dieteticos)
            score_dieteticos = match_diet / len(lista_dieteticos)
        else:
            score_dieteticos = 0.0

        # Cálculo de coincidencias de ingredientes
        if lista_ingredientes:
            match_ing = sum(1 for ing in ingredientes_plat if ing in lista_ingredientes)
            score_ingredientes = match_ing / len(lista_ingredientes)
        else:
            score_ingredientes = 0.0

        #Combina las tres señales ponderadas
        prob_combinada = (
            w_sabores * score_sabores +
            w_dieteticos * score_dieteticos +
            w_ingredientes * score_ingredientes
        )
        prob_combinada = max(min(prob_combinada, 1.0), 0.0)

        # Guarda la probabilidad del platillo y su categoría
        probabilidades_platillos[nombre] = {
            "probabilidad": float(prob_combinada),
            "categoria": categoria
        }
        total_general += prob_combinada

    #Normaliza las probabilidades respecto al total
    probabilidades_norm = {}
    for nombre, meta in probabilidades_platillos.items():
        categoria = meta["categoria"]
        prob = meta["probabilidad"]
        prob_norm = (prob / total_general) if total_general > 0 else 0.0
        probabilidades_norm[nombre] = (prob_norm, categoria)

    return probabilidades_norm

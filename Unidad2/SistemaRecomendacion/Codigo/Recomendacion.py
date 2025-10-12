import json
def recomendarPlatillos(lista_gustos, lista_restricciones,lista_dieteticos=[], lista_ingredientes=[]):
    with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion\\Json\\Platillos.json", "r", encoding="utf-8") as f:
        diccionario_platillos = json.load(f)

    probs_dict = probabilidadesPlatillos(lista_gustos, lista_restricciones, diccionario_platillos, lista_dieteticos, lista_ingredientes)

    # Si quieres todos los platillos que empatan en la probabilidad máxima:
    if probs_dict:
        # probs_dict maps nombre -> (probabilidad_normalizada, categoria)
        max_prob = max((v[0] for v in probs_dict.values()), default=0.0)
        # guardamos lista de tuplas (nombre, categoria) para los ganadores
        ganadores = []
        aux_ganadores = []
        categoria = ""
        for k, v in probs_dict.items():
            prob_norm, cat = v
            if (prob_norm == max_prob and prob_norm > 0) or prob_norm >= max_prob:
                aux_ganadores.append((k, cat))
                if categoria != cat:
                    categoria = cat
                    ganadores.append(aux_ganadores)
                    aux_ganadores = []
    else:
        ganadores = []

    return platillosGanadores(diccionario_platillos, ganadores)

def platillosGanadores(diccionario_platillos, ganadores):
    """
    Devuelve la información completa (diccionarios) de los platillos ganadores.
    Conserva la misma estructura de agrupación que 'ganadores' (lista de grupos).
    """
    # mapa rápido por (nombre, categoria) -> platillo
    mapa = {}
    for p in diccionario_platillos:
        clave = (p.get("nombre", ""), p.get("categoria", ""))
        mapa[clave] = p

    resultados = []

    # Aceptar dos posibles formatos de 'ganadores':
    # 1) lista de grupos: [[(nombre,categoria), ...], [(nombre,categoria), ...], ...]
    # 2) lista plana de tuplas: [(nombre,categoria), ...]
    if ganadores and isinstance(ganadores[0], tuple):
        ganadores = [ganadores]

    for grupo in ganadores:
        grupo_info = []
        for item in grupo:
            if not item:
                continue
            nombre, categoria = item
            plat = mapa.get((nombre, categoria))
            if plat:
                grupo_info.append(plat)
            else:
                # fallback: intentar emparejar solo por nombre si no hay match exacto
                for p in diccionario_platillos:
                    if p.get("nombre", "") == nombre:
                        grupo_info.append(p)
                        break
        if grupo_info:
            resultados.append(grupo_info)

    print("Platillos ganadores (detalles):", resultados)
    return resultados

def probabilidadesPlatillos(lista_gustos, lista_restricciones, diccionario_platillos, lista_dieteticos=[], lista_ingredientes=[]):
    """
    Calcula una probabilidad combinada por platillo integrando:
      - coincidencias de 'sabores' (gustos vs restricciones)
      - coincidencias con etiquetas 'dieteticos'
      - coincidencias con 'ingredientes' solicitados
    Devuelve un dict nombre -> (probabilidad_normalizada, categoria)
    """
    probabilidades_platillos = {}
    total_general = 0.0

    # pesos para combinar las tres señales (ajustables)
    w_sabores = 0.6
    w_dieteticos = 0.4
    w_ingredientes = 0.5

    for platillo in diccionario_platillos:
        nombre = platillo.get("nombre", "")
        categoria = platillo.get("categoria", "")

        sabores = platillo.get("sabores", []) or []
        diet_tags = platillo.get("restricciones", []) or []
        ingredientes_plat = platillo.get("ingredientes", []) or []

        # --- score sabores (gustos vs restricciones) ---
        match_gustos = sum(1 for s in sabores if s in lista_gustos)
        match_restr = sum(1 for s in sabores if s in lista_restricciones)
        denom_sabores = len(sabores) or 1
        score_sabores = max((match_gustos - match_restr) / denom_sabores, 0.0)

        # --- score dieteticos: fracción de dieteticos deseados presentes ---
        if lista_dieteticos:
            match_diet = sum(1 for d in diet_tags if d in lista_dieteticos)
            # normalizar respecto a lo solicitado por el usuario (lista_dieteticos)
            score_dieteticos = match_diet / len(lista_dieteticos)
        else:
            score_dieteticos = 0.0

        # --- score ingredientes: fracción de ingredientes deseados presentes ---
        if lista_ingredientes:
            match_ing = sum(1 for ing in ingredientes_plat if ing in lista_ingredientes)
            # normalizar respecto a lo solicitado por el usuario (lista_ingredientes)
            score_ingredientes = match_ing / len(lista_ingredientes)
        else:
            score_ingredientes = 0.0

        # combinar las señales con pesos y asegurar rango [0,1]
        prob_combinada = (
            w_sabores * score_sabores
            + w_dieteticos * score_dieteticos
            + w_ingredientes * score_ingredientes
        )
        prob_combinada = max(min(prob_combinada, 1.0), 0.0)

        probabilidades_platillos[nombre] = {"probabilidad": float(prob_combinada), "categoria": categoria}
        total_general += prob_combinada

    # Normalizar respecto al total general (si total_general == 0 quedan ceros)
    probabilidades_norm = {}
    for nombre, meta in probabilidades_platillos.items():
        categoria = meta["categoria"]
        prob = meta["probabilidad"]
        prob_norm = (prob / total_general) if total_general > 0 else 0.0
        probabilidades_norm[nombre] = (prob_norm, categoria)

    return probabilidades_norm

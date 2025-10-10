import json
def recomendarPlatillos(lista_gustos, lista_restricciones):
    with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion\\Json\\Platillos.json", "r", encoding="utf-8") as f:
        diccionario_platillos = json.load(f)

    probs_dict = probabilidadesPlatillos(lista_gustos, lista_restricciones, diccionario_platillos)

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

def probabilidadesPlatillos(lista_gustos, lista_restricciones, diccionario_platillos):
    probabilidades_platillos = {}
    total_general = 0.0

    # Primera pasada: calcular score bruto por platillo y acumular total general
    for platillo in diccionario_platillos:
        nombre = platillo.get("nombre", "")
        categoria = platillo.get("categoria", "")
        sabores = platillo.get("sabores", []) or []

        prob_estar = sum(1 for s in sabores if s in lista_gustos)
        prob_no_estar = sum(1 for s in sabores if s in lista_restricciones)
        total_ingredientes = len(sabores) or 1  # evita división por cero

        prob = max((prob_estar - prob_no_estar) / total_ingredientes, 0.0)
        probabilidades_platillos[nombre] = {"probabilidad": float(prob), "categoria": categoria}
        total_general += prob

    # Segunda pasada: normalizar respecto al total general (no por categoría)
    probabilidades_norm = {}
    for nombre, meta in probabilidades_platillos.items():
        categoria = meta["categoria"]
        prob = meta["probabilidad"]
        prob_norm = (prob / total_general) if total_general > 0 else 0.0
        # guardamos una tupla (probabilidad_normalizada, categoria)
        probabilidades_norm[nombre] = (prob_norm, categoria)

    return probabilidades_norm

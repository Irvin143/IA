import json
def recomendarPlatillos(diccionario_gustos, diccionario_restricciones):
    with open("C:\\VisualStudio\\Python\\MateriaIA\\IA\\Unidad2\\SistemaRecomendacion\\Platillos.json", "r", encoding="utf-8") as f:
        diccionario_platillos = json.load(f)
    lista_gustos = []
    categorias_gustos = []

    for categoria, gustos in diccionario_gustos.items():
        categorias_gustos.append(categoria)
        lista_gustos.extend(gustos)

    lista_restricciones = []
    categoria_restricciones = []

    for categoria, restricciones in diccionario_restricciones.items():
        categoria_restricciones.append(categoria)
        lista_restricciones.extend(restricciones)

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
            if prob_norm == max_prob and prob_norm > 0:
                aux_ganadores.append((k, cat))
                if categoria != cat:
                    categoria = cat
                    ganadores.append(aux_ganadores)
                    print("Ganadores por categoría:", aux_ganadores)
    else:
        ganadores = []

    print("Todos los ganadores (empates):", ganadores )
    return ganadores

# ...existing code...
def probabilidadesPlatillos(lista_gustos, lista_restricciones, diccionario_platillos):
    probabilidades_platillos = {}
    total_por_categoria = {}

    # Primera pasada: calcular score bruto por platillo y acumular total por categoría
    for platillo in diccionario_platillos:
        nombre = platillo.get("nombre", "")
        categoria = platillo.get("categoria", "")
        sabores = platillo.get("sabores", [])

        prob_estar = sum(1 for s in sabores if s in lista_gustos)
        prob_no_estar = sum(1 for s in sabores if s in lista_restricciones)
        total_ingredientes = len(sabores) or 1  # evita división por cero

        prob = max((prob_estar - prob_no_estar) / total_ingredientes, 0)
        probabilidades_platillos[nombre] = {"probabilidad": prob, "categoria": categoria}
        total_por_categoria[categoria] = total_por_categoria.get(categoria, 0) + prob

    # Segunda pasada: normalizar por categoría
    probabilidades_norm = {}
    for nombre, meta in probabilidades_platillos.items():
        categoria = meta["categoria"]
        prob = meta["probabilidad"]
        total_cat = total_por_categoria.get(categoria, 0)
        prob_norm = (prob / total_cat) if total_cat > 0 else 0.0
        # guardamos una tupla (probabilidad_normalizada, categoria)
        probabilidades_norm[nombre] = (prob_norm, categoria)

    return probabilidades_norm

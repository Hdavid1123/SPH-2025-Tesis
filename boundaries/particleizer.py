def generar_particulas(segmentos, tipo=1, h=0.01):
    """Convierte una lista de arrays de puntos en estructuras de partículas"""
    particulas = []
    id_counter = 0
    for segmento in segmentos:
        for p in segmento:
            particulas.append({
                "id": id_counter,
                "type": tipo,
                "position": [float(p[0]), float(p[1])],
                "velocity": [0.0, 0.0],
                "h": h
            })
            id_counter += 1
    return particulas
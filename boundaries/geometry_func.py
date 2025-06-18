import numpy as np

def segmentar_lado(P1, P2, sc):
    d = np.linalg.norm(P2 - P1)
    n_puntos = max(2, int(np.ceil(d / sc)))
    return np.linspace(P1, P2, n_puntos)


def construir_trapecio(d1, d2, d3, a1, a2, a3, k=1):
    sc = 1 / (d1 + d2 + d3)
    d1, d2, d3 = d1 * sc, d2 * sc, d3 * sc
    angulos = np.deg2rad([a1, a2, a3])

    A = np.array([-0.5, 0.0])
    B = A + d1 * np.array([np.cos(angulos[0]), np.sin(angulos[0])])
    C = B + d2 * np.array([np.cos(angulos[1]), np.sin(angulos[1])])
    D = C + d3 * np.array([np.cos(angulos[2]), np.sin(angulos[2])])

    offset = - ((min(A[1], B[1], C[1], D[1]) + max(A[1], B[1], C[1], D[1])) / 2)
    for p in [A, B, C, D]:
        p[1] += offset

    lados = {
        'AB': segmentar_lado(A, B, k * sc),
        'BC': segmentar_lado(B, C, k * sc),
        'CD': segmentar_lado(C, D, k * sc),
        'DA': segmentar_lado(D, A, k * sc),
    }

    vertices = {'A': A, 'B': B, 'C': C, 'D': D}
    return lados, vertices, sc


def agregar_agujero(P1, P2, longitud, offset, sc, k=1):
    longitud *= sc
    offset *= sc

    dir_vec = P2 - P1
    total_dist = np.linalg.norm(dir_vec)
    dir_unit = dir_vec / total_dist

    inicio = P1 + offset * dir_unit
    fin = inicio + longitud * dir_unit

    def fuera_de_agujero(p):
        dp = p - inicio
        return not (0 <= np.dot(dp, dir_unit) <= longitud)

    puntos = segmentar_lado(P1, P2, k*sc)
    filtrados = np.array([p for p in puntos if fuera_de_agujero(p)])

    print(f"Agujero en [{offset:.4f}, {offset + longitud:.4f}] (normalizado)")
    print(f"Puntos antes: {len(puntos)}; después: {len(filtrados)}")

    if len(filtrados) < 2:
        print("[⚠️ AVISO] Agujero elimina todos los puntos. Se conservan todos.")
        return puntos

    return filtrados


def agregar_linea(vertice, longitud, angulo_deg, sc, k=1):
    longitud *= sc
    angulo_rad = np.deg2rad(angulo_deg)
    desplazamiento = np.array([np.cos(angulo_rad), np.sin(angulo_rad)]) * longitud
    extremo = vertice + desplazamiento
    return segmentar_lado(vertice, extremo, k*sc)
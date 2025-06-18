from boundaries.geometry_func import construir_trapecio
from boundaries.geometry_func import agregar_agujero
from boundaries.geometry_func import agregar_linea
from boundaries import cargar_parametros

def construir_geometria_desde_parametros():
    params = cargar_parametros()

    # Construir trapecio
    trap = params["trapecio"]
    lados, vertices, sc = construir_trapecio(
        trap["d1"], trap["d2"], trap["d3"],
        trap["a1"], trap["a2"], trap["a3"],
        trap.get("resolucion", 1)
    )
    k = trap.get("resolucion", 1)

    # Aplicar agujeros
    for agujero in params.get("agujeros", []):
        lado = agujero["lado"]
        if lado in lados and lado in ["AB", "BC", "CD", "DA"]:
            # Obtener extremos verdaderos del lado
            extremos = {
                "AB": ("A", "B"),
                "BC": ("B", "C"),
                "CD": ("C", "D"),
                "DA": ("D", "A")
            }
            v1, v2 = extremos[lado]
            P1, P2 = vertices[v1], vertices[v2]

            nuevos_puntos = agregar_agujero(
                P1, P2,
                agujero["tam"],
                agujero["offset"],
                sc,
                k
            )
            lados[lado] = nuevos_puntos

    # Agregar líneas adicionales
    lineas_extra = []
    for linea in params.get("lineas_extra", []):
        v = linea["vertice"]
        if v in vertices:
            nueva_linea = agregar_linea(
                vertices[v],
                linea["tam"],
                linea["angulo"],
                sc,
                k
            )
            lineas_extra.append(nueva_linea)

    return lados, lineas_extra
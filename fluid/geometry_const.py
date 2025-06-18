from fluid.geometry_fluid import generar_particulas_fluidas
from fluid.filter import eliminar_solapamientos
import os
import json

def cargar_configuracion():
    ruta = os.path.join(os.path.dirname(__file__), "parameters", "fluid_region.json")
    with open(ruta, "r") as f:
        return json.load(f)
    
def construir_fluido(puntos_frontera=None):
    config = cargar_configuracion()
    fluido = generar_particulas_fluidas(config)

    if puntos_frontera is not None:
        espaciado = config["espaciado"]
        fluido = eliminar_solapamientos(fluido, puntos_frontera, distancia_minima=espaciado / 2)

    return fluido

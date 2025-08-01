import json


def exportar_particulas_json(particulas, ruta="estructura_ics.json"):
    with open(ruta, "w") as f:
        json.dump({"particles": particulas}, f, indent=2)
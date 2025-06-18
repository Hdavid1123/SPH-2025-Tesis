import json

def cargar_parametros(path="boundaries/parameters/boundary_conditions.json"):
    with open(path, 'r') as f:
        return json.load(f)
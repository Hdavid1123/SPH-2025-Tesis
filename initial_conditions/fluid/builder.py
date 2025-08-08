# initial_conditions/fluid/builder.py

import json
from pathlib import Path
import numpy as np
from fluid.geometry import sample_fluid_region
from fluid.filter import eliminar_solapamientos

PARAM_PATH = Path(__file__).resolve().parent.parent / "parameters" / "fluid_region.json"


class FluidBuilder:
    def __init__(self, config_file: Path | str = PARAM_PATH):
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

    def build(self, border_points: np.ndarray | None = None) -> np.ndarray:
        """
        Genera la nube de puntos de la región fluida.
        Si se proporcionan border_points, elimina solapamientos con las partículas de frontera.
        """
        # 1. Generar nube de puntos del fluido
        puntos = sample_fluid_region(self.config)

        # 2. Filtrar para evitar solapamiento con la frontera
        if border_points is not None and len(border_points) > 0:
            espaciado = self.config["espaciado"]
            puntos = eliminar_solapamientos(puntos, border_points, espaciado / 2)

        return puntos

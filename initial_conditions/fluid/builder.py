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

    def build(self, border_points: np.ndarray | None = None) -> dict:
        """
        Genera la nube de puntos de la región fluida y metadatos para el resumen.
        """
        # Generar nube inicial
        puntos = sample_fluid_region(self.config)
        print(f"[DEBUG] Puntos iniciales generados: {puntos.shape[0]}")

        # Guardar antes del filtrado
        y_vals_before = np.unique(np.round(puntos[:, 1], 6))
        x_vals_before = np.unique(np.round(puntos[:, 0], 6))

        # Filtrar solapamientos
        if border_points is not None and len(border_points) > 0:
            espaciado = self.config["espaciado"]
            puntos_filtrados = eliminar_solapamientos(puntos, border_points, espaciado / 2)
            print(f"[DEBUG] Puntos después del filtrado: {puntos_filtrados.shape[0]}")

            # Filas eliminadas
            y_vals_after = np.unique(np.round(puntos_filtrados[:, 1], 6))
            filas_perdidas = sorted(set(y_vals_before) - set(y_vals_after))
            if filas_perdidas:
                print(f"[DEBUG] Filas eliminadas (y): {filas_perdidas}")

            # Columnas eliminadas
            x_vals_after = np.unique(np.round(puntos_filtrados[:, 0], 6))
            columnas_perdidas = sorted(set(x_vals_before) - set(x_vals_after))
            if columnas_perdidas:
                print(f"[DEBUG] Columnas eliminadas (x): {columnas_perdidas}")

            puntos = puntos_filtrados

        # Construir metadatos
        fluid_data = {
            "particles": [(float(x), float(y)) for x, y in puntos],
            "area": self.config.get("area", None),
            "h": self.config.get("h", None),
            "start_pos": tuple(self.config["vertices"]["inf-izq"]),
            "vertices": [
                tuple(self.config["vertices"]["inf-izq"]),
                tuple(self.config["vertices"]["inf-der"]),
                tuple(self.config["vertices"]["sup-der"]),
                tuple(self.config["vertices"]["sup-izq"])
            ]
        }

        return fluid_data

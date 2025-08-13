# initial_conditions/boundaries/builder.py

import json
from pathlib import Path
from domains.quadrilateral import Quadrilateral
from .particleizer import BoundaryParticleizer

PARAM_PATH = Path(__file__).parent.parent / "parameters" / "boundary_conditions.json"

class BoundaryBuilder:
    def __init__(self, param_file: Path | str = PARAM_PATH):
        with open(param_file, 'r', encoding='utf-8') as f:
            self.params = json.load(f)

    def build(self,
              resolution: int = None,
              particle_type: int = 1,
              h: float = 0.01) -> dict:
        """
        Construye la geometría de frontera y genera la lista de partículas SPH,
        junto con metadatos para el resumen.

        Returns:
            dict: {"particles": [...], "spacing": float, "sections": [...], "holes": [...]}
        """
        # Configuración del trapecio
        cfg = self.params["trapecio"].copy()
        if resolution is not None:
            cfg["resolution"] = resolution

        # Instanciar Quadrilateral con agujeros y líneas extra
        quad = Quadrilateral(
            d1=cfg["d1"], d2=cfg["d2"], d3=cfg["d3"],
            a1=cfg["a1"], a2=cfg["a2"], a3=cfg["a3"],
            resolution=cfg.get("resolution", 1),
            holes=self.params.get("agujeros", []),
            extra_lines=self.params.get("lineas_extra", [])
        )

        # Obtener segmentos
        segmentos = quad.segments()

        # Generar partículas
        particleizer = BoundaryParticleizer()
        particles = particleizer.generate(
            segments=segmentos,
            ptype=particle_type,
            h=h
        )

        # Construir estructura de resumen
        boundary_data = {
            "particles": [(p["position"][0], p["position"][1]) for p in particles],
            "spacing": cfg.get("espaciado", None),
            "sections": quad.section_info(),  # método que debe devolver inicio/fin de cada sección
            "holes": quad.hole_info()         # método que debe devolver inicio/fin/partículas eliminadas
        }

        return boundary_data

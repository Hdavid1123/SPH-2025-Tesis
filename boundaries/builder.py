# boundaries/builder.py
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
              h: float = 0.01) -> list[dict]:
        """
        Construye la geometría de frontera y genera la lista de partículas SPH.
        
        Args:
            resolution: Factor de resolución para el muestreo de segmentos.
            particle_type: Tipo de partícula (int).
            h: Radio de suavizado para cada partícula.

        Returns:
            List[dict]: lista de partículas con campos id, type, position, velocity, h.
        """
        # 1) Configuración del trapecio
        cfg = self.params["trapecio"].copy()
        if resolution is not None:
            cfg["resolution"] = resolution

        # 2) Instanciar Quadrilateral con agujeros y líneas extra
        quad = Quadrilateral(
            d1=cfg["d1"], d2=cfg["d2"], d3=cfg["d3"],
            a1=cfg["a1"], a2=cfg["a2"], a3=cfg["a3"],
            resolution=cfg.get("resolution", 1),
            holes=self.params.get("agujeros", []),
            extra_lines=self.params.get("lineas_extra", [])
        )

        # 3) Obtener segmentos y particionar en partículas
        segmentos = quad.segments()
        particleizer = BoundaryParticleizer()
        particles = particleizer.generate(
            segments=segmentos,
            ptype=particle_type,
            h=h
        )

        return particles
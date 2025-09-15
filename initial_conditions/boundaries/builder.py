# boundaries/builder.py
import json
from pathlib import Path
from domains.quadrilateral import Quadrilateral
from domains.composite import CompositeDomain
from .particleizer import BoundaryParticleizer

PARAM_PATH = Path(__file__).parent.parent / "parameters" / "boundary_conditions.json"


class BoundaryBuilder:
    def __init__(self, param_file: Path | str = PARAM_PATH):
        with open(param_file, "r", encoding="utf-8") as f:
            self.params = json.load(f)

    def build_geometry(self, resolution: int = None) -> CompositeDomain:
        """
        Construye y devuelve un CompositeDomain con las geometrías
        definidas en el archivo de parámetros.
        """
        comp = CompositeDomain()

        # 1) Construcción de cuadriláteros (por ahora solo esta forma soportada)
        for quad_cfg in self.params.get("quadrilateros", []):
            cfg = quad_cfg.copy()
            if resolution is not None:
                cfg["resolution"] = resolution

            quad = Quadrilateral(
                d1=cfg["d1"], d2=cfg["d2"], d3=cfg["d3"],
                a1=cfg["a1"], a2=cfg["a2"], a3=cfg["a3"],
                resolution=cfg.get("resolution", 1),
                holes=cfg.get("agujeros", []),
            )
            comp.add_domain(quad)

        # 2) Conexiones entre dominios o puntos absolutos
        for conn in self.params.get("connections", []):
            p1, p2 = conn["p1"], conn["p2"]
            comp.add_connection(p1, p2, resolution=conn.get("resolution", 1))

        # 3) Líneas libres (desde un endpoint hacia un punto libre o longitud/ángulo)
        for fl in self.params.get("free_lines", []):
            comp.add_free_line(
                from_point=fl["from"],
                to_point=fl.get("to"),
                length=fl.get("length"),
                angle=fl.get("angle"),
                resolution=fl.get("resolution", 1),
            )

        return comp

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
        # 1) Construir geometría compuesta
        comp = self.build_geometry(resolution=resolution)

        # 2) Obtener segmentos de la geometría compuesta
        segmentos = comp.segments()

        # 3) Convertir segmentos en partículas
        particleizer = BoundaryParticleizer()
        particles = particleizer.generate(
            segments=segmentos,
            ptype=particle_type,
            h=h
        )

        return particles

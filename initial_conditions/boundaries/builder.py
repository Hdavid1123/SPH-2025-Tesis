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
        definidas en el archivo de parámetros, usando una escala global
        basada en todas las longitudes (cuadriláteros y líneas libres).
        """
        # 0) Definición de la escala global
        longitudes = []

        # cuadriláteros
        for quad_cfg in self.params.get("quadrilateros", []):
            longitudes.extend([quad_cfg["d1"], quad_cfg["d2"], quad_cfg["d3"]])

        # líneas libres
        for line in self.params.get("free_lines", []):
            if "length" in line:
                longitudes.append(line["length"])

        # conexiones
        for conn in self.params.get("connections", []):
            if "length" in conn:
                longitudes.append(conn["length"])

        # escala global: todo se normaliza para que la longitud máxima = 1
        sc_global = 1 / sum(longitudes) if longitudes else 1.0

        # 1) Construcción de cuadriláteros
        comp = CompositeDomain(sc_base=sc_global)

        for i, quad_cfg in enumerate(self.params.get("quadrilateros", [])):
            cfg = quad_cfg.copy()
            if resolution is not None:
                cfg["resolution"] = resolution

            quad = Quadrilateral(
                d1=cfg["d1"], d2=cfg["d2"], d3=cfg["d3"],
                a1=cfg["a1"], a2=cfg["a2"], a3=cfg["a3"],
                resolution=cfg.get("resolution", 1),
                holes=[{**h, "tam": h["tam"], "offset": h["offset"]}
                       for h in cfg.get("agujeros", [])],
                sc_base=sc_global
            )
            comp.add_domain(quad)

            # Registrar automáticamente los puntos A, B, C, D
            labels = ["A", "B", "C", "D"]
            for lbl, coords in zip(labels, quad.vertices()):
                name = f"{lbl}{i}" if len(self.params.get("quadrilateros", [])) > 1 else lbl
                comp.register_point(name, coords)

        # 2) Construcción de conexiones y líneas libres
        for conn in self.params.get("connections", []):
            comp.add_connection(
                conn["p1"], conn["p2"],
                resolution=conn.get("resolution", 1)
            )

        for fl in self.params.get("free_lines", []):
            comp.add_free_line(
                from_point=fl["from"],
                to_point=fl.get("to"),
                length=fl.get("length", None) * sc_global if fl.get("length") else None,
                angle=fl.get("angle"),
                resolution=fl.get("resolution", 1),
                name=fl.get("name"),
            )

        comp.print_points()  # Imprime los puntos registrados para verificación
        
        return comp

    def build(self,
              resolution: int = None,
              particle_type: int = 1,
              h: float = 0.01) -> list[dict]:
        """
        Construye la geometría de frontera y genera la lista de partículas SPH.
        """
        comp = self.build_geometry(resolution=resolution)
        segmentos = comp.segments()

        particleizer = BoundaryParticleizer()
        particles = particleizer.generate(
            segments=segmentos,
            ptype=particle_type,
            h=h
        )

        return particles

from typing import List, Dict, Any, Tuple

Point = Tuple[float, float]
Segment = List[Point]

class BoundaryParticleizer:
    def __init__(self):
        pass

    def generate(self,
                 segments: List[Segment],
                 ptype: int = 1,
                 h: float = 0.01) -> List[Dict[str, Any]]:
        """
        Convierte lista de segmentos (líneas de frontera) en partículas SPH.
        Filtra automáticamente segmentos vacíos o puntos inválidos.
        """
        particles: List[Dict[str, Any]] = []
        seen: set[Tuple[float, float]] = set()
        id_counter = 0

        for seg in segments:
            if seg is None or len(seg) == 0:
                continue  # Ignorar segmentos vacíos
            for pt in seg:
                if pt is None or len(pt) != 2:
                    continue  # Ignorar puntos inválidos
                x, y = pt
                key = (round(x, 8), round(y, 8))
                if key in seen:
                    continue
                seen.add(key)
                particles.append({
                    "id": id_counter,
                    "type": ptype,
                    "position": [x, y],
                    "velocity": [0.0, 0.0],
                    "h": h
                })
                id_counter += 1

        return particles

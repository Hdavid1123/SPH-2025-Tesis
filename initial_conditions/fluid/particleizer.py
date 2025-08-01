from typing import List, Dict, Any
import numpy as np

class FluidParticleizer:
    def __init__(self):
        pass

    def generate(self,
                 points: np.ndarray,
                 ptype: int = 0,
                 h: float = 0.01,
                 velocity: tuple[float, float] = (0.0, 0.0)) -> List[Dict[str, Any]]:
        """
        Convierte un array de puntos 2D en partículas SPH de fluido.

        Args:
            points: np.ndarray de forma (N, 2), coordenadas x, y.
            ptype: tipo de partícula (por defecto 0 para fluido).
            h: radio de suavizado.
            velocity: tupla con la velocidad inicial común (vx, vy).

        Returns:
            Lista de diccionarios con campos: id, type, position, velocity, h.
        """
        particles: List[Dict[str, Any]] = []

        for i, (x, y) in enumerate(points):
            particles.append({
                "id": i,
                "type": ptype,
                "position": [x, y],
                "velocity": list(velocity),
                "h": h
            })

        return particles
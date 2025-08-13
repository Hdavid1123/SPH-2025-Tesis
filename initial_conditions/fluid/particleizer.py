from typing import List, Dict, Any, Tuple
import numpy as np

class FluidParticleizer:
    def __init__(self):
        pass

    def generate(self,
                 points: np.ndarray,
                 ptype: int = 0,
                 h: float = 0.01,
                 velocity: Tuple[float, float] = (0.0, 0.0)) -> List[Dict[str, Any]]:
        """
        Convierte un array de puntos 2D en partículas SPH de fluido.
        Filtra automáticamente puntos vacíos o inválidos.
        """
        particles: List[Dict[str, Any]] = []

        if points is None or len(points) == 0:
            return particles

        # Asegurarse de que points tenga forma (N,2)
        points = np.array(points)
        if points.ndim != 2 or points.shape[1] != 2:
            return particles

        for i, (x, y) in enumerate(points):
            if np.isnan(x) or np.isnan(y):
                continue  # Ignorar NaN
            particles.append({
                "id": i,
                "type": ptype,
                "position": [x, y],
                "velocity": list(velocity),
                "h": h
            })

        return particles

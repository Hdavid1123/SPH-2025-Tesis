# domains/quadrilateral.py
import numpy as np
from typing import List
from .base import BoundaryShape, Point, Segment
from .utils import (
    construir_trapecio,
    agregar_agujero
)

class Quadrilateral(BoundaryShape):
    def __init__(self,
                 d1: float, d2: float, d3: float,
                 a1: float, a2: float, a3: float,
                 resolution: int = 1,
                 holes: List[dict] = None):
        """
        Construye un cuadrilátero normalizado con muestreo de lados,
        opcionalmente le aplica agujeros.

        Parámetros:
        - d1, d2, d3: longitudes de tres lados consecutivos.
        - a1, a2, a3: ángulos (grados) entre d1→d2, d2→d3, d3→d1.
        - resolution: factor de resolución para segmentar cada lado.
        - holes: lista de dicts { lado: "AB"|"BC"|"CD"|"DA", tam, offset }.
        """

        # Construir trapecio y normalizar
        lados, vertices, sc = construir_trapecio(
            d1, d2, d3,
            a1, a2, a3,
            k=resolution
        )

        self._vertices: dict[str, np.ndarray] = vertices
        self._segments: dict[str, np.ndarray] = lados
        self._sc: float = sc
        self._resolution: int = resolution

        # Agregar agujeros en lados si existen
        if holes:
            extremos = {
                "AB": ("A", "B"),
                "BC": ("B", "C"),
                "CD": ("C", "D"),
                "DA": ("D", "A")
            }
            for h in holes:
                side = h["lado"]
                if side in extremos:
                    v1, v2 = extremos[side]
                    P1, P2 = vertices[v1], vertices[v2]
                    self._segments[side] = agregar_agujero(
                        P1, P2,
                        h["tam"],
                        h["offset"],
                        sc,
                        k=resolution
                    )

    def segments(self) -> List[Segment]:
        """Retorna la lista de todos los segmentos del cuadrilátero."""
        return list(self._segments.values())

    def vertices(self) -> List[Point]:
        """Retorna los vértices A, B, C y D del cuadrilátero."""
        return [tuple(self._vertices[k]) for k in ["A", "B", "C", "D"]]

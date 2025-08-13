# initial_conditions/domains/quadrilateral.py

import numpy as np
from .base import Domain2D, Point, Segment
from typing import List
from .utils import (
    construir_trapecio,
    agregar_agujero,
    agregar_linea
)

class Quadrilateral(Domain2D):
    def __init__(self,
                 d1: float, d2: float, d3: float,
                 a1: float, a2: float, a3: float,
                 resolution: int = 1,
                 holes: List[dict] = None,
                 extra_lines: List[dict] = None):
        """
        Construye un cuadrilátero normalizado con muestreo de lados,
        opcionalmente le aplica agujeros y líneas extra.
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

        # Guardaremos info de secciones y agujeros
        self._holes_info: List[dict] = []

        # Procesar agujeros
        if holes:
            extremos = {
                "AB": ("A", "B"),
                "BC": ("B", "C"),
                "CD": ("C", "D"),
                "DA": ("D", "A")
            }
            for h in holes:
                side = h['lado']
                if side in extremos:
                    v1, v2 = extremos[side]
                    P1, P2 = vertices[v1], vertices[v2]

                    # Segmento original
                    original_seg = self._segments[side]

                    # Segmento modificado con agujero
                    mod_seg = agregar_agujero(
                        P1, P2,
                        h['tam'],
                        h['offset'],
                        sc,
                        k=resolution
                    )

                    # Solo actualizar si hay partículas restantes
                    if mod_seg.size > 0:
                        self._segments[side] = mod_seg
                        removed_count = len(original_seg) - len(mod_seg)
                        self._holes_info.append({
                            "section": side,
                            "start": tuple(mod_seg[0]),
                            "end": tuple(mod_seg[-1]),
                            "removed_particles": removed_count
                        })
                    else:
                        # Segmento eliminado completamente
                        del self._segments[side]
                        removed_count = len(original_seg)
                        self._holes_info.append({
                            "side": side,
                            "start": None,
                            "end": None,
                            "removed_particles": removed_count
                        })

        # Procesar líneas extra
        if extra_lines:
            for line in extra_lines:
                vert = line['vertice']
                if vert in vertices:
                    linea_seg = agregar_linea(
                        vertices[vert],
                        line['tam'],
                        line['angulo'],
                        sc,
                        k=resolution
                    )
                    if linea_seg.size > 0:
                        key = f"extra_{vert}_{line['angulo']}"
                        self._segments[key] = linea_seg

        # Construir info de secciones filtrando segmentos vacíos
        self._sections_info: List[dict] = self._build_sections_info()

    def _build_sections_info(self) -> List[dict]:
        """Construye la info de las secciones iniciales."""
        info = []
        for name in ["AB", "BC", "CD", "DA"]:
            if name in self._segments and self._segments[name].size > 0:
                seg = self._segments[name]
                start = tuple(seg[0])
                end = tuple(seg[-1])
                info.append({"name": name, "start": start, "end": end})
        return info

    def segments(self) -> List[Segment]:
        """Retorna la lista de todos los segmentos del cuadrilátero."""
        return list(self._segments.values())

    def vertices(self) -> List[Point]:
        """Retorna la lista de vértices A, B, C y D del cuadrilátero."""
        return [tuple(self._vertices[key]) for key in ['A', 'B', 'C', 'D']]

    def section_info(self) -> List[dict]:
        """Devuelve info de las secciones de frontera."""
        return self._sections_info

    def hole_info(self) -> List[dict]:
        """Devuelve info de los agujeros aplicados."""
        return self._holes_info

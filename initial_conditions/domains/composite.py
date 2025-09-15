import numpy as np
from typing import List, Optional
from .base import Point, Segment, BoundaryShape


class CompositeDomain(BoundaryShape):
    """
    Representa un dominio compuesto por varias formas 2D
    (cuadriláteros, círculos, etc.) y conexiones (líneas entre extremos).
    """

    def __init__(self,
                 domains: List[BoundaryShape] = None,
                 connections: List[Segment] = None):
        self.domains = domains or []
        self.connections = connections or []

    def add_domain(self, domain: BoundaryShape):
        """Agrega una forma al dominio compuesto."""
        self.domains.append(domain)

    def add_connection(self, p1: Point, p2: Point, resolution: int = 1):
        """Añade una línea de conexión entre dos puntos existentes."""
        p1, p2 = np.array(p1), np.array(p2)
        seg = np.linspace(p1, p2, resolution + 1)
        self.connections.append(seg)

    def add_free_line(self,
                      from_point: Point,
                      to_point: Optional[Point] = None,
                      length: Optional[float] = None,
                      angle: Optional[float] = None,
                      resolution: int = 1):
        """
        Añade una línea que parte desde un endpoint y termina en:
        - un punto arbitrario (to_point), o
        - un punto definido por (length, angle) relativo a from_point.

        Args:
            from_point: Punto inicial (usualmente un endpoint de un dominio).
            to_point: Punto final absoluto (si se pasa, ignora length/angle).
            length: Longitud de la línea (si se usa con angle).
            angle: Ángulo en grados respecto al eje x (si se usa con length).
            resolution: Número de subdivisiones.
        """
        p1 = np.array(from_point, dtype=float)

        if to_point is not None:
            p2 = np.array(to_point, dtype=float)
        elif length is not None and angle is not None:
            theta = np.radians(angle)
            dx, dy = length * np.cos(theta), length * np.sin(theta)
            p2 = p1 + np.array([dx, dy])
        else:
            raise ValueError("Debe especificar `to_point` o (`length` y `angle`).")

        seg = np.linspace(p1, p2, resolution + 1)
        self.connections.append(seg)

    def segments(self) -> List[Segment]:
        """Devuelve todos los segmentos: internos + conexiones."""
        segs = []
        for d in self.domains:
            segs.extend(d.segments())
        segs.extend(self.connections)
        return segs

    def endpoints(self) -> List[Point]:
        """Devuelve todos los extremos únicos de dominios y conexiones."""
        extremos = []
        for d in self.domains:
            extremos.extend(d.endpoints())
        for seg in self.connections:
            extremos.append(tuple(seg[0]))
            extremos.append(tuple(seg[-1]))
        return list(dict.fromkeys(extremos))


from abc import ABC, abstractmethod
from typing import List, Tuple

Point = Tuple[float, float]
Segment = List[Point]

class BoundaryShape(ABC):
    """Interfaz base para cualquier geometría 2D
    representada por segmentos."""
    
    @abstractmethod
    def segments(self) -> List[Segment]:
        """Retorna lista de segmentos
        (lados, líneas extra, etc.)"""
        
        pass

    def endpoints(self) -> List[Point]:
        """Por defecto: todos los extremos
        únicos de los segmentos"""
        
        extremos = []
        for seg in self.segments():
            extremos.append(seg[0])
            extremos.append(seg[-1])
        return list(dict.fromkeys(extremos))
from abc import ABC, abstractmethod
from typing import List, Tuple

Point = Tuple[float, float]
Segment = List[Point]

class Domain2D(ABC):
    @abstractmethod
    def segments(self) -> List[Segment]:
        """Retorna lista de segmentos (lados, líneas extra, etc.)"""
        pass

    @abstractmethod
    def vertices(self) -> List[Point]:
        """Retorna vértices característicos del dominio"""
        pass
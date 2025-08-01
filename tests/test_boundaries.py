import pytest
import matplotlib
from pathlib import Path
matplotlib.use('Agg')  # Para evitar abrir ventanas durante la prueba

from boundaries.builder import BoundaryBuilder
from boundaries.visualizer import visualize_boundary
from domains.quadrilateral import Quadrilateral
from boundaries.visualizer import visualize_boundary
import matplotlib.axes


def test_builder_generates_particles():
    """Verifica que el constructor de límites genere partículas válidas"""
    builder = BoundaryBuilder()
    particles = builder.build(resolution=2, particle_type=1, h=0.01)

    assert isinstance(particles, list)
    assert len(particles) > 0

    sample = particles[0]
    expected_keys = {"id", "type", "position", "velocity", "h"}
    assert expected_keys.issubset(sample), f"Faltan campos: {expected_keys - set(sample)}"
    assert isinstance(sample["position"], list) and len(sample["position"]) == 2


def test_visualize_boundary_renders_particles():
    """Verifica que visualize_boundary devuelva un Axes válido al graficar partículas"""
    builder = BoundaryBuilder()
    particles = builder.build(resolution=3, particle_type=1, h=0.01)

    ax = visualize_boundary(particles, show=False)

    import matplotlib
    assert isinstance(ax, matplotlib.axes.Axes)
    assert len(ax.lines) > 0  # Debería haber al menos un segmento reconstruido

def test_visualize_boundary_saves_image(tmp_path):
    """
    Verifica que la función visualize_boundary guarde una imagen PNG válida.
    """
    # Construir frontera
    builder = BoundaryBuilder()
    particles = builder.build(resolution=2, particle_type=1, h=0.01)

    # Definir ruta temporal para imagen
    save_file = Path("outputs/frontera.png")
    save_file.parent.mkdir(parents=True, exist_ok=True)

    # Llamar a la función con guardado
    ax = visualize_boundary(particles, show=False, save_path=str(save_file))

    # Validaciones
    assert isinstance(ax, matplotlib.axes.Axes)
    assert save_file.exists()
    assert save_file.stat().st_size > 0
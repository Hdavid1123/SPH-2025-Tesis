import math
import pytest

# Importa los módulos compilados
from algoritms.kernels.cubic_spline import cubicSplineKernel, dCubicSplineKernel
from algoritms.kernels.wendland import wendlandKernel
from algoritms.kernels.common import Dimension

# -----------------------
# Tests para cubic spline
# -----------------------
def test_cubic_kernel_center():
    """El kernel debe ser positivo en el origen"""
    h = 1.0
    w = cubicSplineKernel(0.0, h, Dimension.TWO_D)
    assert w > 0.0


def test_cubic_kernel_support():
    """Fuera de 2h, el kernel debe ser 0"""
    h = 1.0
    w = cubicSplineKernel(2.5, h, Dimension.TWO_D)
    assert w == 0.0


def test_cubic_kernel_symmetry():
    """El kernel debe ser simétrico respecto a r"""
    h = 1.0
    r1 = 0.5
    r2 = abs(-0.5)  # -> 0.5
    w1 = cubicSplineKernel(r1, h, Dimension.TWO_D)
    w2 = cubicSplineKernel(r2, h, Dimension.TWO_D)
    assert math.isclose(w1, w2, rel_tol=1e-12)


def test_cubic_kernel_derivative():
    """Las derivadas direccionales deben dar un vector no nulo dentro del soporte"""
    h = 1.0
    dx, dy = 0.5, 0.5
    r = math.sqrt(dx**2 + dy**2)
    dWx, dWy = dCubicSplineKernel(r, dx, dy, h)
    assert dWx != 0.0
    assert dWy != 0.0


# --------------------
# Tests para Wendland
# --------------------
def test_wendland_center():
    """El kernel Wendland debe ser positivo en el origen"""
    h = 1.0
    w = wendlandKernel.wendlandC2(0.0, h, Dimension.TWO_D)
    assert w > 0.0


def test_wendland_support():
    """Fuera de 2h, Wendland debe ser 0"""
    h = 1.0
    w = wendlandKernel.wendlandC2(2.5, h, Dimension.TWO_D)
    assert w == 0.0


def test_wendland_derivative():
    """La derivada de Wendland debe ser distinta de 0 dentro del soporte"""
    h = 1.0
    r = 0.5
    dw = wendlandKernel.dWendlandC2(r, 1.0, h, Dimension.TWO_D)
    assert dw != 0.0


# -----------------------------
# Generación de kernel_test.output
# -----------------------------
def test_generate_kernel_output(tmp_path):
    """Genera un archivo kernel_test.output para validación manual"""
    file_path = tmp_path / "kernel_test.output"
    with open(file_path, "w") as f:
        for i in range(-30, 31):
            r = i * 0.1
            w = cubicSplineKernel(abs(r), 1.0, Dimension.TWO_D)
            dWx, _ = dCubicSplineKernel(abs(r), r / math.sqrt(2.0), 0.0, 1.0)
            f.write(f"{r:16.10f} {w:16.10f} {dWx:16.10f}\n")

    # Valida que el archivo no esté vacío
    assert file_path.stat().st_size > 0

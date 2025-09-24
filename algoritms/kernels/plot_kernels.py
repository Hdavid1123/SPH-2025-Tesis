import math
import numpy as np
import matplotlib.pyplot as plt

from algoritms.kernels.cubic_spline import cubicSplineKernel, dCubicSplineKernel
from algoritms.kernels.wendland import wendlandKernel
from algoritms.kernels.common import Dimension

def plot_cubic_spline(h=1.0):
    r_values = np.linspace(-2.5 * h, 2.5 * h, 200)
    w_values = [cubicSplineKernel(abs(r), h, Dimension.TWO_D) for r in r_values]

    # derivadas direccionales en x, tomamos dy=0
    dw_values = [
        dCubicSplineKernel(abs(r), r, 0.0, h)[0] for r in r_values
    ]

    plt.figure(figsize=(7, 5))
    plt.plot(r_values, w_values, label="Cubic Spline W(r)")
    plt.plot(r_values, dw_values, label="dW/dr (x-dir)", linestyle="--")
    plt.title("Cubic Spline Kernel (2D)")
    plt.xlabel("r")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_wendland(h=1.0):
    r_values = np.linspace(0.0, 2.5 * h, 200)
    w_values = [wendlandKernel.wendlandC2(r, h, Dimension.TWO_D) for r in r_values]

    dw_values = [
        wendlandKernel.dWendlandC2(r, 1.0, h, Dimension.TWO_D) for r in r_values
    ]

    plt.figure(figsize=(7, 5))
    plt.plot(r_values, w_values, label="Wendland C2 W(r)")
    plt.plot(r_values, dw_values, label="dW/dr", linestyle="--")
    plt.title("Wendland C2 Kernel (2D)")
    plt.xlabel("r")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_cubic_spline()
    plot_wendland()

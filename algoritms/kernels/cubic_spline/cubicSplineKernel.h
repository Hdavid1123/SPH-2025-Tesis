#pragma once
#include <cmath>
#include <array>
#include "../common/common.h"   // Importa la definición de Dimension

namespace kernels {

// Kernel cúbico spline
double cubicSplineKernel(double r, double h, Dimension dim);

// Derivadas direccionales del kernel cúbico spline (2D)
std::array<double, 2> dCubicSplineKernel(double r, double dx, double dy, double h);

} // namespace kernels

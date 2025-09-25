#pragma once
#include <cmath>
#include <array>
#include "dimension.h"

namespace kernels {

using data_structures::Dimension;
using data_structures::ONE_D;
using data_structures::TWO_D;
using data_structures::THREE_D;

// Kernel cúbico spline
double cubicSplineKernel(double r, double h, Dimension dim);

// Derivadas direccionales del kernel cúbico spline (2D)
std::array<double, 2> dCubicSplineKernel(double r, double dx, double dy, double h);

} // namespace kernels

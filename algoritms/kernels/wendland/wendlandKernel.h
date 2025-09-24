#pragma once
#include <cmath>
#include "../common/common.h"   // ahora usamos la definición compartida

namespace kernels {

// Kernel Wendland C2
double wendlandC2(double r, double h, Dimension dim);

// Derivada direccional del Wendland C2
double dWendlandC2(double r, double dr, double h, Dimension dim);

} // namespace kernels

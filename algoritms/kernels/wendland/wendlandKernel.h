#pragma once
#include <cmath>
#include "dimension.h"   // ahora usamos la definición compartida

namespace kernels {

using data_structures::Dimension;
using data_structures::ONE_D;
using data_structures::TWO_D;
using data_structures::THREE_D;

// Kernel Wendland C2
double wendlandC2(double r, double h, Dimension dim);

// Derivada direccional del Wendland C2
double dWendlandC2(double r, double dr, double h, Dimension dim);

} // namespace kernels

#include "wendlandKernel.h"

namespace kernels {

using data_structures::Dimension;
using data_structures::ONE_D;
using data_structures::TWO_D;
using data_structures::THREE_D;

double wendlandC2(double r, double h, Dimension dim) {
    if (r < 0 || h <= 0) throw std::runtime_error("r>=0 and h>0 required");
    double q = r / h;
    if (q >= 1.0) return 0.0;

    double factor = 0.0;
    switch (dim) {
        case TWO_D:   factor = 7.0 / (4.0 * M_PI * h * h); break;
        case THREE_D: factor = 21.0 / (16.0 * M_PI * h * h * h); break;
        default: throw std::runtime_error("Unsupported dimension");
    }

    double one_minus_q = 1.0 - q;
    return factor * one_minus_q * one_minus_q * one_minus_q * (1.0 + 3.0*q);
}

double dWendlandC2(double r, double dr, double h, Dimension dim) {
    if (r < 0 || h <= 0) throw std::runtime_error("r>=0 and h>0 required");
    if (r == 0.0) return 0.0; // evita división por cero

    double q = r / h;
    if (q >= 1.0) return 0.0;

    double factor = 0.0;
    switch (dim) {
        case TWO_D:   factor = 7.0 / (4.0 * M_PI * h * h); break;
        case THREE_D: factor = 21.0 / (16.0 * M_PI * h * h * h); break;
        default: throw std::runtime_error("Unsupported dimension");
    }

    double one_minus_q = 1.0 - q;
    double dWdr = factor * (-12.0 * q * one_minus_q * one_minus_q); // ∂W/∂r
    return dWdr * dr / r; // derivada direccional
}

} // namespace kernels

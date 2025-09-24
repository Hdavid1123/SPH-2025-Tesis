#include <pybind11/pybind11.h>
#include "common.h"

namespace py = pybind11;

PYBIND11_MODULE(common, m) {
    py::enum_<kernels::Dimension>(m, "Dimension")
        .value("ONE_D", kernels::ONE_D)
        .value("TWO_D", kernels::TWO_D)
        .value("THREE_D", kernels::THREE_D)
        .export_values();
}

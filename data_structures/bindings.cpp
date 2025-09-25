#include <pybind11/pybind11.h>
#include "dimension.h"

namespace py = pybind11;

PYBIND11_MODULE(data_structures, m) {
    py::enum_<data_structures::Dimension>(m, "Dimension")
        .value("ONE_D", data_structures::Dimension::ONE_D)
        .value("TWO_D", data_structures::Dimension::TWO_D)
        .value("THREE_D", data_structures::Dimension::THREE_D)
        .export_values();
}

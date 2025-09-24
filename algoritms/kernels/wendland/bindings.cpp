#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wendlandKernel.h"

namespace py = pybind11;

PYBIND11_MODULE(wendlandKernel, m) {
    m.def("wendlandC2", &kernels::wendlandC2,
          py::arg("r"), py::arg("h"), py::arg("dim"),
          "Compute Wendland C2 kernel value");

    m.def("dWendlandC2", &kernels::dWendlandC2,
          py::arg("r"), py::arg("dr"), py::arg("h"), py::arg("dim"),
          "Compute Wendland C2 kernel derivative");
}

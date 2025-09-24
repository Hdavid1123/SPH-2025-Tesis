#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "cubicSplineKernel.h"

namespace py = pybind11;

PYBIND11_MODULE(cubicSplineKernel, m) {
    m.def("cubicSplineKernel",
          &kernels::cubicSplineKernel,
          "Calcula el kernel cúbico spline",
          py::arg("r"), py::arg("h"), py::arg("dim"));

    m.def("dCubicSplineKernel",
          &kernels::dCubicSplineKernel,
          "Calcula las derivadas direccionales del kernel cúbico spline",
          py::arg("r"), py::arg("dx"), py::arg("dy"), py::arg("h"));
}

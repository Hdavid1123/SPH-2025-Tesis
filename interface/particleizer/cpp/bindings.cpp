#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "particleizer.h"

namespace py = pybind11;

PYBIND11_MODULE(particleizer_cpp, m) {
    m.doc() = "C++ Particleizer para SPH (frontera y fluido)";

    // Binding para BoundaryParticleizer
    py::class_<BoundaryParticleizer>(m, "BoundaryParticleizer")
        .def(py::init<>())
        .def("generate", &BoundaryParticleizer::generate,
             py::arg("segments"),
             py::arg("ptype") = 1,
             py::arg("h") = 0.01,
             "Genera partículas de frontera y retorna el número total");

    // Binding para FluidParticleizer
    py::class_<FluidParticleizer>(m, "FluidParticleizer")
        .def(py::init<>())
        .def("generate", &FluidParticleizer::generate,
             py::arg("points"),
             py::arg("ptype") = 0,
             py::arg("h") = 0.01,
             py::arg("velocity") = std::array<double,2>{0.0,0.0},
             "Genera partículas de fluido y retorna el número total");

    // Funciones para acceder al array global
    m.def("get_particles_pointer", &ParticleizerBase::data,
          "Devuelve puntero al array C++ Particles");
    m.def("get_num_particles", &ParticleizerBase::size,
          "Devuelve número de partículas actuales");
}

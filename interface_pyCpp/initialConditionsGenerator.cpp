#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "Particle.h"

namespace py = pybind11;

std::vector<Particle> inicializar_particulas(py::array_t<double> arr) {
    auto buf = arr.unchecked<2>();  // matriz 2D
    size_t n = buf.shape(0);

    std::vector<Particle> particles;
    particles.reserve(n);

    for (size_t i = 0; i < n; i++) {
        Particle p;

        p.id         = static_cast<int>(buf(i, 0));
        p.pos        = {buf(i, 1), buf(i, 2)};
        p.vel        = {buf(i, 3), buf(i, 4)};
        p.accel      = {0.0, 0.0};   // inicialización por defecto
        p.mass       = buf(i, 5);
        p.rho        = 0.0;
        p.h          = buf(i, 6);
        p.pressure   = 0.0;
        p.soundVel   = 0.0;
        p.internalE  = 0.0;
        p.dinternalE = 0.0;
        p.type       = static_cast<int>(buf(i, 7));

        particles.push_back(p);
    }

    return particles;
}

PYBIND11_MODULE(initial_conditions, m) {
    py::class_<Particle>(m, "Particle")
        .def(py::init<>())
        .def_readwrite("id", &Particle::id)
        .def_readwrite("pos", &Particle::pos)
        .def_readwrite("vel", &Particle::vel)
        .def_readwrite("accel", &Particle::accel)
        .def_readwrite("mass", &Particle::mass)
        .def_readwrite("rho", &Particle::rho)
        .def_readwrite("h", &Particle::h)
        .def_readwrite("pressure", &Particle::pressure)
        .def_readwrite("soundVel", &Particle::soundVel)
        .def_readwrite("intenalE", &Particle::internalE)
        .def_readwrite("dinternalE", &Particle::dinternalE)
        .def_readwrite("neighbors", &Particle::neighbors)
        .def_readwrite("dx", &Particle::dx)
        .def_readwrite("dy", &Particle::dy)
        .def_readwrite("r", &Particle::r)
        .def_readwrite("W", &Particle::W)
        .def_readwrite("dWx", &Particle::dWx)
        .def_readwrite("dWy", &Particle::dWy)
        .def_readwrite("type", &Particle::type);

    m.def("inicializar_particulas", &inicializar_particulas,
          "Construye partículas a partir de un array NumPy");
}

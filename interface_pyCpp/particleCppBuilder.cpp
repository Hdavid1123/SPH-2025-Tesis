#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "Particle.h"

namespace py = pybind11;

/**
 * Convierte un numpy.ndarray (N,8) en un std::vector<Particle>.
 *
 * Columnas esperadas:
 *   0: id
 *   1: posx
 *   2: posy
 *   3: h
 *   4: type
 *   5: mass
 *   6: dx
 *   7: dy
 */
std::vector<Particle> inicializar_particulas(py::array_t<double> arr) {
    auto buf = arr.unchecked<2>();  
    size_t n = buf.shape(0);
    size_t m = buf.shape(1);

    if (m < 8) {
        throw std::runtime_error(
            "El array debe tener 8 columnas: id, posx, posy, h, type, mass, dx, dy"
        );
    }

    std::vector<Particle> particles;
    particles.reserve(n);

    for (size_t i = 0; i < n; i++) {
        Particle p;

        p.id   = static_cast<int>(buf(i, 0));
        p.pos  = {buf(i, 1), buf(i, 2)};
        p.h    = buf(i, 3);
        p.type = static_cast<int>(buf(i, 4));
        p.mass = buf(i, 5);

        // Guardamos dx y dy en sus vectores (aunque por ahora tengan un solo valor)
        p.dx.push_back(buf(i, 6));
        p.dy.push_back(buf(i, 7));

        // Inicializaciones por defecto
        p.vel        = {0.0, 0.0};
        p.accel      = {0.0, 0.0};
        p.rho        = 1000.0;
        p.pressure   = 0.0;
        p.soundVel   = 0.0;
        p.internalE  = 357.1;
        p.dinternalE = 0.0;

        // Vecinos y otros vectores vacíos
        p.neighbors.clear();
        p.r.clear();
        p.W.clear();
        p.dWx.clear();
        p.dWy.clear();

        particles.push_back(std::move(p));
    }

    return particles;
}

PYBIND11_MODULE(initial_particles_builder, m) {
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
        .def_readwrite("internalE", &Particle::internalE)
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

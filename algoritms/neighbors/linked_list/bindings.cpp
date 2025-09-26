#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "linkedList.h"

namespace py = pybind11;

PYBIND11_MODULE(neighbors_linked_list, m) {
    m.doc() = "Busqueda de vecinos usando linked list";

    m.def("buildGrid", &buildGrid, "Construir malla de celdas");

    m.def("assign_particles_to_cells", &assignParticlesToCells,
          "Asigna partículas a celdas para linked list");

    m.def("find_neighbors_linked", &findNeighbors,
          "Encuentra vecinos usando linked list");
}

from interface_pyCpp.initial_particles_builder import inicializar_particulas
from algoritms.kernels import cubicSplineKernel
from algoritms.neighbor_search import neighborSearch

particles = inicializar_particulas(numpy_array)
# Crear celdas y asignar vecinos
neighborSearch.findNeighbors(particles, cells, 0, h, cubicSplineKernel.cubicSplineKernel, derivative_func)

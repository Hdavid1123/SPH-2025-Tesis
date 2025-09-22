import numpy as np
import initial_conditions as simulacion

# Ejemplo de datos: id, x, y, vx, vy, mass, h, type
data = np.array([
    [0, 0.1, 0.2, 0.0, 0.0, 1.0, 0.05, 1],
    [1, 0.3, 0.4, 0.0, 0.0, 1.0, 0.05, 1],
], dtype=np.float64)

particles = simulacion.inicializar_particulas(data)

print("Cantidad:", len(particles))
print("Primera partícula:", particles[0].id, particles[0].pos, particles[0].h)

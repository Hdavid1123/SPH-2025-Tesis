#include "particleizer.h"
#include <cstdlib>

// Definición de variables estáticas
Particles* ParticleizerBase::part = nullptr;
int ParticleizerBase::nPart = 0;

void ParticleizerBase::allocate(int total) {
    if (part) {
        std::free(part);
    }
    part = static_cast<Particles*>(std::malloc(sizeof(Particles) * total));
    nPart = total;
}

Particles* ParticleizerBase::data() {
    return part;
}

int ParticleizerBase::size() {
    return nPart;
}

// Función interna para inicializar un solo Particles[i]
static void init_particle(Particles* arr, int i,
                          double x, double y,
                          double vX, double vY,
                          double h, int ptype) {
    arr[i].id = i;
    arr[i].pos[X] = x; arr[i].pos[Y] = y;
    arr[i].vel[X] = vX; arr[i].vel[Y] = vY;
    arr[i].accel[X] = arr[i].accel[Y] = 0.0;
    arr[i].rho = 1000.0;
    arr[i].mass = arr[i].rho * h * h;  // Asumiendo elemento de área h*h
    arr[i].h = h;
    arr[i].p = 0.0;
    arr[i].c = 0.0;
    arr[i].du = 0.0;
    arr[i].u = 357.1;
    arr[i].nn = nullptr;
    arr[i].nNeighbors = 0;
    arr[i].dx = arr[i].dy = arr[i].dz = nullptr;
    arr[i].r = arr[i].W = arr[i].dWx = arr[i].dWy = arr[i].dWz = nullptr;
    arr[i].type = ptype;
}

int BoundaryParticleizer::generate(
    const std::vector<std::vector<std::array<double,2>>>& segments,
    int ptype,
    double h)
{
    // Calcular número total de puntos
    int total = 0;
    for (const auto& seg : segments) {
        total += static_cast<int>(seg.size());
    }

    allocate(total);

    int idx = 0;
    for (const auto& seg : segments) {
        for (const auto& pt : seg) {
            init_particle(part, idx,
                          pt[0], pt[1],
                          0.0, 0.0,
                          h, ptype);
            ++idx;
        }
    }

    return size();
}

int FluidParticleizer::generate(
    const std::vector<std::array<double,2>>& points,
    int ptype,
    double h,
    const std::array<double,2>& velocity)
{
    int total = static_cast<int>(points.size());
    allocate(total);

    int idx = 0;
    for (const auto& pt : points) {
        init_particle(part, idx,
                      pt[0], pt[1],
                      velocity[0], velocity[1],
                      h, ptype);
        ++idx;
    }

    return size();
}

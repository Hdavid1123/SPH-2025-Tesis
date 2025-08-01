#ifndef PARTICLEIZER_H
#define PARTICLEIZER_H

#include "allvars.h"
#include <vector>
#include <array>

/**
 * Clase base que gestiona la reserva y acceso al array global de Particles.
 */
class ParticleizerBase {
public:
    virtual ~ParticleizerBase() = default;

    /// Reserva (o re-reserva) el array de Particles con capacidad `total`.
    static void allocate(int total);

    /// Devuelve puntero al inicio del array global de Particles.
    static Particles* data();

    /// Devuelve el número actual de partículas (`nPart`).
    static int size();

protected:
    static Particles* part;
    static int nPart;
};

/**
 * Genera partículas para la frontera a partir de segmentos discretizados.
 */
class BoundaryParticleizer : public ParticleizerBase {
public:
    /**
     * @param segments  Vector de segmentos, cada uno vector de {x,y}.
     * @param ptype     Tipo de partícula (entero).
     * @param h         Radio de suavizado.
     * @return Número total de partículas generadas.
     */
    int generate(const std::vector<std::vector<std::array<double,2>>>& segments,
                 int ptype,
                 double h);
};

/**
 * Genera partículas para la región de fluido a partir de un conjunto de puntos.
 */
class FluidParticleizer : public ParticleizerBase {
public:
    /**
     * @param points     Vector de {x,y} para cada partícula.
     * @param ptype      Tipo de partícula.
     * @param h          Radio de suavizado.
     * @param velocity   Velocidad inicial {vx, vy}.
     * @return Número total de partículas generadas.
     */
    int generate(const std::vector<std::array<double,2>>& points,
                 int ptype,
                 double h,
                 const std::array<double,2>& velocity);
};

#endif // PARTICLEIZER_H

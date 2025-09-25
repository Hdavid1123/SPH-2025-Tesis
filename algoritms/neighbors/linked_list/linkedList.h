#pragma once
#include <vector>
#include "interface_pyCpp/Particle.h"
#include "Cell.h"

// Asigna partículas a celdas
void assignParticlesToCells(std::vector<Cell>& cells,
                            std::vector<Particle>& particles,
                            double h);

// Busca vecinos con linked list
void findNeighbors(std::vector<Cell>& cells,
                   std::vector<Particle>& particles,
                   double kappa = 2.0);

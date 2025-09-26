#pragma once
#include <vector>
#include "particle.h"
#include "cell.h"

// Construye la malla de celdas
std::vector<Cell> buildGrid(double xmin, double xmax,
                            double ymin, double ymax,
                            double h);
                            
// Asigna partículas a celdas
void assignParticlesToCells(std::vector<Cell>& cells,
                            std::vector<Particle>& particles,
                            double h);

// Busca vecinos con linked list
void findNeighbors(std::vector<Cell>& cells,
                   std::vector<Particle>& particles,
                   double kappa = 2.0);

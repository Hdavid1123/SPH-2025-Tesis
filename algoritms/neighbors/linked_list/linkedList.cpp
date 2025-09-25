#include "linkedList.h"
#include <cmath>
#include "kernels/cubic_spline/cubicSplineKernel.h"

void assignParticlesToCells(std::vector<Cell>& cells,
                            std::vector<Particle>& particles,
                            double h) {
    for (auto& cell : cells) {
        cell.particles.clear();
        for (size_t j = 0; j < particles.size(); j++) {
            double dx = std::abs(particles[j].pos[0] - cell.center[0]);
            double dy = std::abs(particles[j].pos[1] - cell.center[1]);

            if (dx < h + 1e-5*h && dy < h + 1e-5*h) {
                cell.particles.push_back(j);
            }
        }
    }
}

void findNeighbors(std::vector<Cell>& cells,
                   std::vector<Particle>& particles,
                   double kappa) {
    for (auto& cell : cells) {
        for (int pid : cell.particles) {
            Particle& pi = particles[pid];

            pi.neighbors.clear();
            pi.dx.clear(); pi.dy.clear(); pi.r.clear();
            pi.W.clear(); pi.dWx.clear(); pi.dWy.clear();

            for (int neighborCellId : cell.neighborCells) {
                Cell& neighCell = cells[neighborCellId];
                for (int pj_id : neighCell.particles) {
                    if (pj_id == pid) continue;

                    Particle& pj = particles[pj_id];

                    double dx = pi.pos[0] - pj.pos[0];
                    double dy = pi.pos[1] - pj.pos[1];
                    double r = std::sqrt(dx*dx + dy*dy);
                    double h_ij = 0.5 * (pi.h + pj.h);

                    if (r < kappa * h_ij) {
                        pi.neighbors.push_back(pj_id);
                        pi.dx.push_back(dx);
                        pi.dy.push_back(dy);
                        pi.r.push_back(r);

                        double Wval = cubicSplineKernel(r, h_ij, kernels::TWO_D);
                        auto dWval = dCubicSplineKernel(r, dx, dy, h_ij);

                        pi.W.push_back(Wval);
                        pi.dWx.push_back(dWval[0]);
                        pi.dWy.push_back(dWval[1]);
                    }
                }
            }
        }
    }
}

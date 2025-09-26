#include "linkedList.h"
#include <cmath>
#include "kernels/cubic_spline/cubicSplineKernel.h"

std::vector<Cell> buildGrid(double xmin, double xmax,
                            double ymin, double ymax,
                            double h) {
    int nx = static_cast<int>((xmax - xmin) / h) + 1;
    int ny = static_cast<int>((ymax - ymin) / h) + 1;

    std::vector<Cell> cells;
    cells.reserve(nx * ny);

    // Crear celdas
    for (int i = 0; i < nx; i++) {
        for (int j = 0; j < ny; j++) {
            double cx = xmin + (i + 0.5) * h;
            double cy = ymin + (j + 0.5) * h;

            Cell cell;
            cell.center = {cx, cy};
            cell.id = i * ny + j;
            cells.push_back(cell);
        }
    }

    // Definir vecinos de cada celda
    for (int i = 0; i < nx; i++) {
        for (int j = 0; j < ny; j++) {
            int id = i * ny + j;
            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    int ni = i + di;
                    int nj = j + dj;
                    if (ni >= 0 && ni < nx && nj >= 0 && nj < ny) {
                        int nid = ni * ny + nj;
                        if (nid != id) {
                            cells[id].neighborCells.push_back(nid);
                        }
                    }
                }
            }
        }
    }

    return cells;
}

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

                        double Wval = kernels::cubicSplineKernel(r, h_ij, data_structures::TWO_D);
                        auto dWval = kernels::dCubicSplineKernel(r, dx, dy, h_ij);

                        pi.W.push_back(Wval);
                        pi.dWx.push_back(dWval[0]);
                        pi.dWy.push_back(dWval[1]);
                    }
                }
            }
        }
    }
}

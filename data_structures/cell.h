#pragma once
#include <vector>
#include <array>

struct Cell {
    int id;                             // identificador de la celda
    std::array<double,2> center;        // posición del centro de celda
    std::vector<int> particles;         // índices de partículas dentro de la celda
    std::vector<int> neighborCells;     // índices de celdas vecinas
};
// Estructura para representar una celda en una lista enlazada para búsqueda de vecinos
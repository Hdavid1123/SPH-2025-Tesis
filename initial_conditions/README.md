# SPH-2025-InitialTests

Este proyecto genera condiciones iniciales para simulaciones con el método de partículas SPH (Smoothed Particle Hydrodynamics). Está enfocado en construir:

- **Geometría de frontera** (trapecios personalizables con agujeros y líneas adicionales)
- **Región fluida** (relleno parcial o total dentro de una región arbitraria)
- **Visualización combinada** para verificar configuraciones iniciales
- **Filtrado automático** de solapamientos entre partículas de frontera y fluido

---

## 📦 Estructura del Proyecto

La estructura del proyecto se encuentra documentada en el archivo [`structure.txt`](structure.txt), que refleja la organización modular del código en carpetas temáticas:

- `boundaries/` → Generación de la geometría de frontera  
- `fluid/` → Generación de la región fluida  
- `data/` → Visualización combinada de frontera + fluido  
- `main.py` → Punto de entrada para pruebas  
- `README.md` → Este archivo  
- `structure.txt` → Muestra visual del árbol de directorios  

---

## 🚀 Uso Básico

Puedes importar y ejecutar las funciones de visualización desde `main.py`:

```python
from boundaries.visualizer import graficar_geometria
from fluid.visualizer import graficar_fluido
from data.visualizer import visualizar_borde_y_fluido

graficar_geometria()
graficar_fluido()
visualizar_borde_y_fluido()

# Corrección a 31 de Julio

🏗️ Módulos Principales
domains

    base.py:
    Define la interfaz Domain2D (métodos segments() y vertices()).

    utils.py:
    Funciones de bajo nivel para construir y muestrear geometrías (segmentar lados, crear trapecios, agujeros, líneas).

    quadrilateral.py:
    Clase Quadrilateral que implementa Domain2D, incorpora normalización, agujeros y líneas extra.

boundaries

    builder.py:
    Clase BoundaryBuilder, que lee boundary_conditions.json, construye el Quadrilateral, aplica agujeros/ líneas extra y genera partículas.

    particleizer.py:
    Clase BoundaryParticleizer que asigna IDs, posiciones y radios de suavizado a cada punto de frontera.

    visualizer.py:
    Función visualize_boundary(segments, ...) para trazar la frontera con matplotlib.

fluid

    builder.py:
    Clase FluidBuilder, que lee fluid_region.json y genera la malla de fluido.

    particleizer.py:
    Clase FluidParticleizer para convertir la región interior en partículas SPH.

    visualizer.py:
    Función visualize_fluid(positions, ...) para trazar la distribución de partículas de fluido.

data

    visualizer.py:
    Función visualize_combined(boundary_particles, fluid_particles, ...) para ver ambas colecciones en un solo gráfico.

Ejecutar archivo de tests/test_boundaries.py:
PYTHONPATH=. pytest tests/test_boundaries.py --disable-warnings

## El visualizer de boundaries grafica a partir de las partículas generadas en SPH y el de fluid a partir de la estructura de puntos.


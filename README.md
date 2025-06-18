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
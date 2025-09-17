# 🧊 Proyecto SPH: Condiciones Iniciales

Este módulo forma parte de un proyecto SPH (Smoothed Particle Hydrodynamics) y permite generar, exportar y visualizar **condiciones iniciales** para la simulación.  
Actualmente, incluye funcionalidades para trabajar con:

- **Partículas de frontera**.
- **Partículas de fluido**.
- **Exportación combinada** de ambos conjuntos.
- **Cálculo de estadísticas** sobre la distribución de partículas.

---

## 📁 Estructura relevante del proyecto

```
initial_conditions/
├── boundaries/                   # Generación de partículas de frontera
│   ├── builder.py
│   ├── export.py
│   ├── particleizer.py
│   ├── visualizer.py
├── domains/                      # Define las geometrías y espacio permitido
│   ├── base.py
│   ├── composite.py
│   ├── quadrilateral.py
│   ├── utils.py
├── fluid/                        # Generación de partículas de fluido
│   ├── builder.py                # Construye nube de puntos a partir de parámetros
│   ├── export.py
│   ├── filter.py                 # Filtra solapamientos con la frontera
│   ├── geometry.py               # Genera la malla base y recorta con el polígono
│   ├── particleizer.py
│   ├── stats.py
│   ├── visualizer.py
├── outputs/                      # Carpeta donde se guardan archivos generados
├── parameters/
│   ├── boundary_conditions.json  # Parámetros geométricos de la frontera
│   ├── fluid_region.json         # Parámetros de la región de fluido
├── environment.yml
├── export_all.py
├── main.py                       # Punto de entrada principal
├── README.md
├── structure.txt
```

---

## ▶️ Ejecución del sistema

### Generar partículas de frontera

```bash
python initial_conditions/main.py export_boundaries
```

- Genera partículas SPH de frontera a partir de `parameters/boundary_conditions.json`.
- Guarda en `outputs/boundary_particles.txt`.

### Generar partículas de fluido

```bash
python initial_conditions/main.py export_fluid
```

- Genera la nube de partículas de fluido usando `parameters/fluid_region.json`.
- Filtra partículas que se solapan con la frontera.
- Guarda en `outputs/fluid_particles.txt`.
- Exporta **estadísticas** a `outputs/stats_fluid.txt`.

### Generar todos los conjuntos y exportar en un solo archivo

```bash
python initial_conditions/main.py export_all --plot
```

- Construye partículas de frontera y fluido.
- Filtra solapamientos.
- Exporta todas las partículas combinadas en `outputs/all_particles.txt`.
- Guarda estadísticas del fluido.
- Si se usa `--plot`, abre la visualización.

---

## ⚙️ Argumentos disponibles

| Opción                | Tipo     | Descripción                                                                 |
|-----------------------|----------|-----------------------------------------------------------------------------|
| `export_boundaries`   | comando  | Exporta partículas de frontera.                                             |
| `export_fluid`        | comando  | Exporta partículas de fluido.                                               |
| `export_all`          | comando  | Exporta frontera + fluido en un solo archivo.                               |
| `--output NOMBRE`     | opcional | Nombre del archivo de salida (por defecto en `outputs/`).                   |
| `--plot`              | bandera  | Muestra visualización en `matplotlib`.                                      |

Ejemplos:

```bash
# Exportar fluido y visualizar
python initial_conditions/main.py export_fluid --plot

# Exportar todo en un archivo llamado escena.txt
python initial_conditions/main.py export_all --output escena.txt
```

---

## 📄 Formato de los archivos generados

### Archivos de partículas (`.txt`)

```
posx    posy    h       tipo
0.1234  0.5678  0.01    1
...
```

- `posx`, `posy`: coordenadas.
- `h`: radio de suavizado.
- `tipo`:  
  - `1` → frontera  
  - `2` → fluido

### Archivo de estadísticas (`stats_fluid.txt`)

Contiene el número de partículas por columna y por fila en la malla **después del recorte**:

```
Número de partículas por columna:
 Col  Num
   1    1
   2    5
   ...

Número de partículas por fila:
 Fil  Num
   1   20
   2   18
   ...
```

---

## 🧩 Comportamiento con polígonos no rectangulares

Cuando `flag_N` está en `"True"` en `fluid_region.json`:

1. **Se genera una malla rectangular completa** de `nx × ny` puntos, usando los límites mínimos y máximos (`min_x, max_x, min_y, max_y`) de los vértices dados.
2. **No se recalcula el espaciado**: se conserva la estructura regular de la malla original.
3. **Se recortan los puntos fuera del polígono** usando `matplotlib.path.Path.contains_points`.
4. Como resultado:
   - En las zonas centrales del polígono, las columnas y filas están completas.
   - En las zonas inclinadas, hay menos partículas por columna/fila.
   - Esto mantiene la **consistencia del espaciado** y evita distorsiones.

Ejemplo de configuración (`parameters/fluid_region.json`):

```json
{
  "nx": 20,
  "ny": 20,
  "flag_N": "True",
  "espaciado": 0.02,
  "vertices": {
    "inf-izq": [-0.41, -0.14],
    "inf-der": [-0.25, -0.14],
    "sup-der": [-0.19, 0.14],
    "sup-izq": [-0.47, 0.14]
  }
}
```

---

## 🖼️ Visualización

- Se usa `matplotlib`.
- Escala fija entre `-0.5` y `0.5` en ambos ejes.
- Puntos de frontera → color negro (`ko`).  
- Puntos de fluido → color azul (`bo`).

---

## 📁 Parámetros

- **Frontera** → `parameters/boundary_conditions.json`
- **Fluido** → `parameters/fluid_region.json`

---

## ✅ Requisitos

- Python ≥ 3.10  
- Paquetes: `matplotlib`, `numpy`

Instalar con:

```bash
pip install matplotlib numpy
```
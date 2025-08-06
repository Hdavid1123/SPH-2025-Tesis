# 🧊 Proyecto SPH: Condiciones Iniciales

Este módulo forma parte de un proyecto SPH (Smoothed Particle Hydrodynamics) y permite generar, exportar y visualizar **condiciones iniciales** para la simulación. Actualmente, incluye funcionalidades para trabajar con **partículas de frontera**.

---

## 📁 Estructura relevante del proyecto

```
initial_conditions/
├── main.py                    # Punto de entrada principal
├── boundaries/
│   ├── builder.py             # Construye partículas a partir de geometrías
│   ├── export.py              # Exporta las partículas a un archivo de texto
│   ├── visualizer.py          # Visualiza partículas SPH
├── outputs/                   # Carpeta donde se guardan archivos generados
├── parameters/
│   ├── boundary_conditions.json  # Archivo con parámetros geométricos
```

---

## ▶️ Ejecución del sistema

### Comando básico

```bash
python initial_conditions/main.py export_boundaries
```

Este comando hace lo siguiente:

- Genera partículas SPH a partir de la geometría definida en `parameters/boundary_conditions.json`.
- Las guarda en el archivo por defecto `outputs/boundary_particles.txt`.

---

## ⚙️ Argumentos disponibles

Puedes personalizar el comportamiento con los siguientes flags:

| Opción               | Tipo     | Descripción                                                                 |
|----------------------|----------|-----------------------------------------------------------------------------|
| `export_boundaries`  | comando  | Exporta las partículas de frontera en un archivo `.txt`.                    |
| `--output NOMBRE`    | opcional | Define el nombre del archivo de salida (dentro de `outputs/`).             |
| `--plot`             | bandera  | Si se activa, se abre una visualización con `matplotlib`.                  |

### 🧪 Ejemplos de uso

```bash
# Exportar con nombre personalizado
python initial_conditions/main.py export_boundaries --output frontera.txt

# Exportar y visualizar
python initial_conditions/main.py export_boundaries --plot

# Exportar con nombre personalizado y visualizar
python initial_conditions/main.py export_boundaries --output pared.txt --plot
```

---

## 📄 Formato del archivo generado

El archivo de salida (`.txt`) contiene una tabla de partículas con las siguientes columnas:

```txt
posx    posy    h       tipo
0.1234  0.5678  0.01    1
...
```

- `posx`, `posy`: coordenadas de la partícula.
- `h`: radio de suavizado.
- `tipo`: tipo de partícula (por defecto, `1` para frontera).

---

## 🖼️ Visualización

La visualización se realiza usando `matplotlib`. Las partículas se dibujan como puntos negros (`'ko'`) dentro de una caja de **dimensión fija entre `-0.5` y `0.5`** en ambos ejes (x, y), para mantener consistencia visual.

---

## 📁 Parámetros de geometría

Los datos geométricos y resolución están definidos en el archivo:

```
parameters/boundary_conditions.json
```

Ejemplo de contenido:

```json
{
  "trapecio": {
    "d1": 100,
    "d2": 100,
    "d3": 100,
    "a1": -90,
    "a2": 0,
    "a3": 90,
    "resolucion": 3
  },
  "agujeros": [...],
  "lineas_extra": [...]
}
```

La resolución **no se pasa manualmente**, sino que se lee directamente desde este archivo.

---

## ✅ Requisitos

- Python ≥ 3.10
- Paquetes: `matplotlib`

Instalar con:

```bash
pip install matplotlib
```

---

## 🗂️ Ubicación del archivo

Este archivo `README.md` debe colocarse directamente en el directorio:

```
initial_conditions/README.md
```
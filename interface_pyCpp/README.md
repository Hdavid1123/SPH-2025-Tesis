# interface_pyCpp

Este directorio contiene el **módulo en C++ integrado con Python mediante pybind11**, usado para inicializar y manipular partículas en las simulaciones SPH.

---

## 📂 Contenido

```
interface_pyCpp/
├── Particle.h                   # Definición de la estructura Particle
├── initialConditionsGenerator.cpp  # Implementación del módulo pybind11
├── setup.py                     # Script de compilación
├── part_python.py               # Script de prueba en Python
└── initial_conditions.cpython-*.so (⛔ generado al compilar)
```

---

## 🛠️ Compilación del módulo

1. Entra a la carpeta:

   ```bash
   cd interface_pyCpp
   ```

2. Ejecuta:

   ```bash
   python setup.py build_ext --inplace
   ```

   Esto generará un archivo compartido (`.so`) como:

   ```
   initial_conditions.cpython-310-x86_64-linux-gnu.so
   ```

   ⚠️ **Este archivo no se versiona en GitHub**, se debe recompilar en cada máquina.

---

## 🧩 Estructura `Particle`

Definida en `Particle.h`:

```cpp
struct Particle {
    int id;
    std::array<double, 2> pos;     // posición (x,y)
    std::array<double, 2> vel;     // velocidad
    std::array<double, 2> accel;   // aceleración

    double mass;                   // masa
    double rho;                    // densidad
    double h;                      // longitud de suavizado
    double p;                      // presión
    double c;                      // velocidad del sonido
    double u;                      // energía interna
    double du;                     // variación de energía

    std::vector<int> neighbors;
    std::vector<double> dx, dy, r, W, dWx, dWy;

    int type;                      // tipo de partícula (fluido, frontera, etc.)
};
```

---

## 🚀 Ejemplo de uso en Python

```python
import initial_conditions as ic

# Crear una partícula
p = ic.Particle()
p.id = 1
p.pos = [0.0, 0.0]
p.h = 0.1

print("Partícula creada desde C++:", p)
```

---

## 📌 Notas

- Usa siempre el mismo nombre de módulo en `setup.py` y en `PYBIND11_MODULE` dentro del `.cpp` (`initial_conditions`).
- Para limpiar antes de recompilar:

  ```bash
  rm -rf build/ *.so
  python setup.py build_ext --inplace
  ```

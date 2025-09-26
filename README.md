Para crear los ejecutables de algoritms
python algoritms/setup.py build_ext --inplace

Ejecutar los tests:
python -m pytest -v algoritms/kernels/test_all.py

Graficar los kernels:
python -m algoritms.kernels.plot_kernels

# PipeLine de SPH

1. Se calculan los vecinos de la partícula para determinar sobre cuales partículas se van a realizar los cálculos.

2. Se calcula la densidad usando el kernel de suavizado determinado, en este caso usamos primero el kernel (cubic spline).

# Orden de Creación de los archivos .o mediante setup.py

1. interface_pyCpp/setup.py

2. algoritms/kernels/setup.py

3. algoritms/neighbors/setup.py
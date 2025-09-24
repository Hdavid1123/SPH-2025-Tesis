Para crear los ejecutables de algoritms
python algoritms/setup.py build_ext --inplace

Ejecutar los tests:
python -m pytest -v algoritms/kernels/test_all.py

Graficar los kernels:
python -m algoritms.kernels.plot_kernels

from setuptools import setup, Extension
import pybind11

source_file = "bindings.cpp"

ext_modules = [
    Extension(
        "data_structures",              # Nombre del módulo Python
        [source_file],                  # Archivo C++ fuente
        include_dirs=[pybind11.get_include(), "."],  # "." porque dimension.h está en data_structures
        language="c++",
        extra_compile_args=["-O3", "-std=c++17"],    # Optimización y C++17
    ),
]

setup(
    name="data_structures",
    version="0.1",
    description="Exposición de Dimension con pybind11",
    ext_modules=ext_modules,
)

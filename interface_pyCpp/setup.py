from setuptools import setup, Extension
import pybind11
from pathlib import Path

ext_modules = [
    Extension(
        "initial_particles_builder",  # nombre del módulo importable en Python
        [str(Path("particleCppBuilder.cpp"))],
        include_dirs=[
            pybind11.get_include(),
            str(Path("."))  # Para que encuentre Particle.h si está en el mismo dir
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],  # o -std=c++14 según tu compilador
    ),
]

setup(
    name="initial_particles_builder",
    version="0.1",
    description="Módulo de inicialización de partículas (Pybind11 + C++)",
    ext_modules=ext_modules,
)
